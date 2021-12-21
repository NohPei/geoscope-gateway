import json
import logging
from random import randint
import asyncio as aio
from os import path as pathutil
from datetime import datetime
import aiofiles as files

class GeoAggregator:
    payloads = {}
    background_tasks = set()

    async def __init__(self, storage_root="/mnt/hdd/PigNet/", log_name="GEOSCOPE.Subscriber"):
        self.root_path = storage_root
        self.logger = logging.getLogger(log_name)

    async def save_sensor_data(self, node_id):
        save_time = datetime.now()
        node_name = f"GEOSCOPE_SENSOR_{node_id}"
        folder_path = pathutil.join(self.root_path, "data",
                                    save_time.strftime("%Y-%m-%d"), node_name)
        await files.os.makedirs(folder_path, exist_ok=True)

        saved_payloads = self.payloads[node_id]
        self.payloads[node_id].clear()

        # Create json file
        file_path = pathutil.join(folder_path, f"{save_time:'%Y-%m-%dT%H-%M-%S'}.json")
        async with files.open(file_path, mode='w') as out_file:
            await out_file.write(json.dumps(saved_payloads))
        await aio.to_thread(self.logger.info,"[%s]: %s.json file created",
                            node_name, file_path)


        this_task = aio.current_task()
        if this_task in self.background_tasks:
            self.background_tasks.remove(this_task)


    async def log_sensors(self, messages):
        async for message in messages:
            msg_time = datetime.now()
            await aio.to_thread(self.logger.debug, "[%s] packet received")
            node_id = message.topic.split('/')[-1]

            try:
                sensor_data = json.loads(message.payload.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                await self.json_error_log(message.payload)
                continue
            sensor_data["timestamp"] = round(msg_time.timestamp()*1000)

            if node_id not in self.payloads:
                self.payloads[node_id] = []

            self.payloads[node_id].append(sensor_data)

            if len(self.payloads[node_id]) >= randint(80, 120):
                save_this_sensor_task = aio.create_task(self.save_sensor_data(node_id))
                self.background_tasks.add(save_this_sensor_task)

        await aio.gather(*self.background_tasks)




    async def json_error_log(self, payload: str):
        await aio.to_thread(self.logger.error,"Invalid JSON Packet:"
                            "\n-----\n%s\n-----\n", payload)

    async def log_json_status(self, messages):
        async for message in messages:
            try:
                log_info = json.loads(message.payload.decode("utf=8"))
                await aio.to_thread(self.logger.info,"[%s]: %s", log_info["uuid"], log_info["data"])
            except json.decoder.JSONDecodeError:
                await self.json_error_log(message.payload)


    async def log_status(self, messages):
        async for message in messages:
            await aio.to_thread(self.logger.info, "[%s]: %s", message.topic, message.payload)

    async def flush(self):
        await aio.to_thread(self.logger.info,"Dumping In-Progress Sensor Data...")
        for node in self.payloads:
            await aio.shield(self.save_sensor_data(node))
