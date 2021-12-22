import json
import logging
from random import randint
import asyncio as aio
import os
from datetime import datetime
import aiofile as files

class GeoAggregator:
    payloads = {}
    background_tasks = aio.Queue()
    save_trigger_count = {}

    def __init__(self, storage_root="/mnt/hdd/PigNet/", log_name="GEOSCOPE.Subscriber"):
        self.root_path = storage_root
        self.logger = logging.getLogger(log_name)
        self.logging_sensors = False

    async def save_sensor_data(self, node_id, data):
        save_time = datetime.now()
        node_name = f"GEOSCOPE_SENSOR_{node_id}"
        self.logger.debug("[%s] Trying to write file", node_name)

        folder_path = os.path.join(self.root_path, "data",
                                   save_time.strftime("%Y-%m-%d"), node_name)
        await aio.to_thread(os.makedirs, folder_path, exist_ok=True)

        # Create json file
        file_path = os.path.join(folder_path,
                                 save_time.strftime("%Y-%m-%dT%H-%M-%S.json"))
        async with files.async_open(file_path, mode='w') as out_file:
            await out_file.write(json.dumps(data))
        self.logger.info("[%s]: %s file created", node_name,
                         os.path.basename(file_path))


    async def _background_manager(self, task_queue):
        while True:
            next_task = await task_queue.get()
            await next_task
            task_queue.task_done()


    async def log_sensors(self, messages):
        bg_write_tasks = aio.Queue()
        bg_write_handler = aio.create_task(self._background_manager(bg_write_tasks))

        async for message in messages:
            msg_time = datetime.now()
            node_id = message.topic.split('/')[-1]

            try:
                sensor_data = json.loads(message.payload.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                await self.json_error_log(message.payload)
                continue
            sensor_data["timestamp"] = round(msg_time.timestamp()*1000)

            if node_id not in self.payloads:
                self.payloads[node_id] = []
                self.save_trigger_count[node_id] = randint(80,120)

            self.payloads[node_id].append(sensor_data)
            self.logger.debug("[%s] packet received (#%d)", node_id,
                              len(self.payloads[node_id]))

            if len(self.payloads[node_id]) >= self.save_trigger_count[node_id]:
                save_this_sensor_coro = self.save_sensor_data(node_id,
                                                              self.payloads[node_id][:])
                self.payloads[node_id].clear()
                await bg_write_tasks.put(aio.create_task(save_this_sensor_coro))

        await bg_write_tasks.join()
        bg_write_handler.cancel()

    async def json_error_log(self, payload: str):
        self.logger.error("Invalid JSON Packet:" "\n-----\n%s\n-----\n",
                          payload)

    async def log_json_status(self, messages):
        async for message in messages:
            try:
                log_info = json.loads(message.payload.decode("utf=8"))
                self.logger.info("[%s]: %s", log_info["uuid"],
                                 log_info["data"])
            except json.decoder.JSONDecodeError:
                await self.json_error_log(message.payload)


    async def log_status(self, messages):
        async for message in messages:
            self.logger.info("[%s]: %s", message.topic, message.payload)

    async def flush(self):
        self.logger.info("Dumping In-Progress Sensor Data...")
        write_tasks = set()
        for node in self.payloads:
            write_tasks.add(self.save_sensor_data(node,
                                                  self.payloads[node][:]))
            self.payloads[node].clear()

        await aio.shield(aio.gather(*write_tasks))
