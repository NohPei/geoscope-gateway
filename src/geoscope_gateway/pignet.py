import asyncio as aio
import atexit
import logging
from datetime import datetime
from contextlib import AsyncExitStack
from logging.handlers import QueueHandler, QueueListener, TimedRotatingFileHandler
from queue import SimpleQueue

import aiomqtt as mqtt
from aiopath import AsyncPath

from .logger import GeoAggregator

__all__ = [
    "logger",
    "geophonePriorityQueue",
    "pignet",
    "maintain_mqtt",
]

## Logging

logger = logging.getLogger("GEOSCOPE")
logger.setLevel(logging.INFO)
log_queue = SimpleQueue()
logger.addHandler(QueueHandler(log_queue))
log_file_base = f"GEOSCOPE-{datetime.now().astimezone().strftime('%Y-%m-%d')}.log"


LOG_TOPICS = ["$SYS/broker/log/E", "$SYS/broker/log/W"]
JSON_LOG_TOPICS = ["geoscope/reply"]
SENSORS_TOPIC = "geoscope/node1/+"


log_format = logging.Formatter(
    fmt="%(asctime)s %(levelname)s:%(name)s" " %(message)s", datefmt="%d%b%Y %H:%M:%S"
)


class geophonePriorityQueue(aio.PriorityQueue):
    @staticmethod
    def _matches_any(item: mqtt.Message, topic_list: list):
        for topic in topic_list:
            if item.topic.matches(topic):
                return True
        return False

    def _put(self, item: mqtt.Message):
        if item.topic.matches(SENSORS_TOPIC):
            priority = 1
        elif self._matches_any(item, JSON_LOG_TOPICS):
            priority = 2
        else:
            priority = 3
        super()._put((priority, item))

    def _get(self):
        return super()._get()[1]


async def pignet(
    root_dir="/mnt/hdd/PigNet/", broker_host="127.0.0.1", broker_port=18884
):
    log_dir = AsyncPath(root_dir) / "logs"  # convert to path object

    await log_dir.mkdir(parents=True, exist_ok=True)

    file_log_handler = TimedRotatingFileHandler(
        log_dir / log_file_base, when="midnight", delay=True
    )
    file_log_handler.setFormatter(log_format)

    global log_queue
    log_writer = QueueListener(log_queue, file_log_handler, respect_handler_level=True)

    log_writer.start()  # start saving logs to file
    atexit.register(log_writer.stop)
    # during a shutdown, flush the log buffer
    async with AsyncExitStack() as stack:
        tasks = await stack.enter_async_context(aio.TaskGroup())
        aggregator = GeoAggregator(
            task_group=tasks,
            storage_root=root_dir,
            log_name=logger.name + ".Aggregator",
        )

        stack.push_async_callback(aggregator.flush)
        # during stack unwind, flush all in-progress data

        mqtt_mgr = mqtt.Client(
            hostname=broker_host,
            port=broker_port,
            logger=logging.getLogger(logger.name + ".Client "),
            identifier=logger.name + "_Gateway",
            clean_session=False,
            queue_type=geophonePriorityQueue,
        )

        client = await stack.enter_async_context(mqtt_mgr)

        for topic in LOG_TOPICS:
            await client.subscribe(topic)

        for topic in JSON_LOG_TOPICS:
            await client.subscribe(topic)

        await client.subscribe(SENSORS_TOPIC)

        async for message in client.messages:
            if message.topic.matches(SENSORS_TOPIC):
                recv_time = datetime.now().astimezone()
                tasks.create_task(aggregator.log_sensor(message, recv_time))
            else:
                for topic in JSON_LOG_TOPICS:
                    if message.topic.matches(topic):
                        tasks.create_task(aggregator.log_json_status(message))
                for topic in LOG_TOPICS:
                    if message.topic.matches(topic):
                        await tasks.create_task(aggregator.log_status(message))


async def maintain_mqtt(main_func, *args, **kwargs):
    reconnect_interval = 0.5
    while True:
        try:
            await main_func(*args, **kwargs)
        except mqtt.MqttError as error:
            logger.critical(
                'Client Error "%s". Retrying' "in %f s.", error, reconnect_interval
            )
        finally:
            await aio.sleep(reconnect_interval)
