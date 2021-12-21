import logging
import time
import os
import asyncio as aio
from logging.handlers import ( QueueHandler,
                              TimedRotatingFileHandler,
                              QueueListener )
from contextlib import AsyncExitStack
from queue import SimpleQueue
import uvloop
import asyncio_mqtt as mqtt
from sensor_logger import GeoAggregator


## Logging

logger = logging.getLogger("GEOSCOPE")
logger.setLevel(logging.INFO)
log_queue = SimpleQueue()
logger.addHandler(QueueHandler(log_queue))
log_file_base = f"GEOSCOPE-{time.strftime('%Y-%m-%d')}.log"


LOG_TOPICS = ["$SYS/broker/log/E", "$SYS/broker/log/W"]
JSON_LOG_TOPICS = ["geoscope/reply"]
SENSOR_TOPIC_FILTER = "geoscope/node1/+"


log_format = logging.Formatter( fmt="%(asctime)s %(levelname)s:%(name)s"
                              "%(message)s", datefmt="%d%b%Y %H:%M:%S")

async def pignet(root_dir="/mnt/hdd/PigNet"):
    os.makedirs(os.path.join(root_dir, "logs"), exist_ok=True)
    file_log_handler = TimedRotatingFileHandler(os.path.join(root_dir, "logs",
                                                             log_file_base),
                                                when='midnight', delay=True)
    file_log_handler.setLevel(logging.INFO)
    file_log_handler.setFormatter(log_format)

    log_writer = QueueListener(log_queue, file_log_handler,
                               respect_handler_level=True)
    async with AsyncExitStack as stack:
        tasks = set()
        aggregator = GeoAggregator(storage_root=root_dir, log_name=logger.name+".Aggregator")

        log_writer.start() # start saving logs to file
        stack.push_async_callback(aio.to_thread(log_writer.stop()))
        # during a shutdown, flush the log buffer

        stack.push_async_callback(aggregator.flush)
        # during stack unwind, flush all in-progress data

        client = mqtt.Client("127.0.0.1", port=18884,
                             logger=logging.getLogger(logger.name + ".Client"),
                             client_id=logger.name+"_Gateway",
                             clean_session=False)

        await stack.enter_async_context(client)

        for topic in LOG_TOPICS:
            manager = client.filtered_messages(topic)
            messages = await stack.enter_async_context(manager)
            task = aio.create_task(aggregator.log_status(messages))
            tasks.add(task)
            await client.subscribe(topic)

        for topic in JSON_LOG_TOPICS:
            manager = client.filtered_messages(topic)
            messages = await stack.enter_async_context(manager)
            task = aio.create_task(aggregator.log_json_status(messages))
            tasks.add(task)
            await client.subscribe(topic)

        sensor_manager = client.filtered_messages(SENSOR_TOPIC_FILTER)
        sensor_messages = stack.enter_async_context(sensor_manager)
        sensor_task = aio.create_task(aggregator.log_sensors(sensor_messages))
        tasks.add(sensor_task)
        await client.subscribe(SENSOR_TOPIC_FILTER)

        await aio.gather(*tasks)




async def maintain_mqtt(main_func):
    reconnect_interval = 0.5
    while True:
        try:
            await main_func()
        except mqtt.MqttError as error:
            await aio.to_thread(logger.critical,"Client Error \"%s\". Retrying"
                                "in %f s.", error, reconnect_interval)
        finally:
            await aio.sleep(reconnect_interval)


if __name__ == "__main__":
    logger.info("## Starting full capture system")
    uvloop.install()
    aio.run(maintain_mqtt(pignet))
