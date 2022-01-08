import logging
import time
import atexit
import asyncio as aio
from logging.handlers import ( QueueHandler,
                              TimedRotatingFileHandler,
                              QueueListener )
from contextlib import AsyncExitStack
from queue import SimpleQueue
from aiopath import AsyncPath
import asyncio_mqtt as mqtt
from .logger import GeoAggregator


## Logging

logger = logging.getLogger("GEOSCOPE")
logger.setLevel(logging.INFO)
log_queue = SimpleQueue()
logger.addHandler(QueueHandler(log_queue))
log_file_base = f"GEOSCOPE-{time.strftime('%Y-%m-%d')}.log"


LOG_TOPICS = ["$SYS/broker/log/E", "$SYS/broker/log/W"]
JSON_LOG_TOPICS = ["geoscope/reply"]
SENSORS_TOPIC = "geoscope/node1/+"


log_format = logging.Formatter( fmt="%(asctime)s %(levelname)s:%(name)s"
                               " %(message)s", datefmt="%d%b%Y %H:%M:%S")

async def pignet(root_dir="/mnt/hdd/PigNet/", broker_host="127.0.0.1",
                 broker_port=18884):
    log_dir = AsyncPath(root_dir) / "logs" # convert to path object

    await log_dir.mkdir(parents=True, exist_ok=True)

    file_log_handler = TimedRotatingFileHandler(log_dir / log_file_base,
                                                when='midnight', delay=True)
    file_log_handler.setFormatter(log_format)

    log_writer = QueueListener(log_queue, file_log_handler,
                               respect_handler_level=True)

    log_writer.start() # start saving logs to file
    atexit.register(log_writer.stop)
    # during a shutdown, flush the log buffer
    async with AsyncExitStack() as stack:
        tasks = set()
        aggregator = GeoAggregator(storage_root=root_dir, log_name=logger.name+".Aggregator")

        stack.push_async_callback(aggregator.flush)
        # during stack unwind, flush all in-progress data

        client = mqtt.Client(hostname=broker_host, port=broker_port,
                             logger=logging.getLogger(logger.name+".Client "),
                             client_id=logger.name+"_Gateway",
                             clean_session=False)

        await stack.enter_async_context(client)

        for topic in LOG_TOPICS:
            messages = await stack.enter_async_context(client.filtered_messages(topic))
            tasks.add(aio.create_task(aggregator.log_status(messages)))
            await client.subscribe(topic)

        for topic in JSON_LOG_TOPICS:
            manager = client.filtered_messages(topic)
            messages = await stack.enter_async_context(manager)
            tasks.add(aio.create_task(aggregator.log_json_status(messages)))
            await client.subscribe(topic)

        sensor_messages = await stack.enter_async_context(client.filtered_messages(SENSORS_TOPIC))
        tasks.add(aio.create_task(aggregator.log_sensors(sensor_messages)))
        await client.subscribe(SENSORS_TOPIC)

        await aio.gather(*tasks)




async def maintain_mqtt(main_func, *args, **kwargs):
    reconnect_interval = 0.5
    while True:
        try:
            await main_func(*args, **kwargs)
        except mqtt.MqttError as error:
            logger.critical("Client Error \"%s\". Retrying" "in %f s.", error,
                            reconnect_interval)
        finally:
            await aio.sleep(reconnect_interval)
