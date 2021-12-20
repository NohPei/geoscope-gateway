import logging
import logging.handlers
import time
import atexit
import asyncio as aio
from contextlib import AsyncExitStack
from queue import SimpleQueue
import uvloop
import asyncio_mqtt as mqtt
from sensor_logger import GeoAggregator


## Logging

logger = logging.getLogger("GEOSCOPE")
logger.setLevel(logging.INFO)
file_log_handler = logging.handlers.TimedRotatingFileHandler(
    f"/mnt/hdd/PigNet/log/GEOSCOPE-{time.strftime('%Y-%m-%d')}.log",
    when='midnight', delay=True)
file_log_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s:%(name)s %(message)s", datefmt="%d%b%Y %H:%M:%S"
)
file_log_handler.setFormatter(formatter)

log_queue = SimpleQueue()
logger.addHandler(logging.handlers.QueueHandler(log_queue))

log_writer = logging.handlers.QueueListener(log_queue, file_log_handler,
                                            respect_handler_level=True)
atexit.register(log_writer.stop())
log_writer.start()

async def pignet():
    async with AsyncExitStack as stack:
        tasks = set()
        aggregator = GeoAggregator(storage_root="/mnt/hdd/PigNet", log_name=logger.name+".Aggregator")

        stack.push_async_callback(aggregator.flush) # during stack unwind, flush all in-progress data last

        client_logger = logging.getLogger(logger.name + ".Client")

        client = mqtt.Client("127.0.0.1", "18884", logger=client_logger, clean_session=False)
        await stack.enter_async_context(client)

        log_topics = ["$SYS/broker/log/E", "$SYS/broker/log/W"]
        json_log_topics = ["geoscope/reply"]
        sensor_topic_filter = "geoscope/node1/+"

        for topic in log_topics:
            manager = client.filtered_messages(topic)
            messages = await stack.enter_async_context(manager)
            task = aio.create_task(aggregator.log_status(messages))
            tasks.add(task)
            await client.subscribe(topic)

        for topic in json_log_topics:
            manager = client.filtered_messages(topic)
            messages = await stack.enter_async_context(manager)
            task = aio.create_task(aggregator.log_json_status(messages))
            tasks.add(task)
            await client.subscribe(topic)

        sensor_manager = client.filtered_messages(sensor_topic_filter)
        sensor_messages = stack.enter_async_context(sensor_manager)
        sensor_task = aio.create_task(aggregator.log_sensors(sensor_messages))
        tasks.add(task)
        await client.subscribe(sensor_topic_filter)

        await aio.gather(*tasks)




async def maintain_mqtt(main_func):
    reconnect_interval = 0.5
    while True:
        try:
            await main_func()
        except mqtt.MqttError as error:
            await aio.to_thread(logger.critical,"Client Error \"%s\". Retrying in %f s.", error, reconnect_interval)
        finally:
            await aio.sleep(reconnect_interval)


if __name__ == "__main__":
    logger.info("## Starting full capture system")
    uvloop.install()
    aio.run(maintain_mqtt(pignet))
