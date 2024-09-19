import logging
from random import randint
from typing import Callable
import asyncio as aio
from datetime import datetime
import orjson as json
from aiopath import AsyncPath as Path


async def delete_bad_json(folder):
    folder = Path(folder)

    async def file_check(file):
        try:
            async with file.open(mode="r") as in_file:
                contents = await in_file.read()
                json.loads(contents)
        except ValueError:
            await file.unlink()

    async with aio.TaskGroup() as del_group:
        async for file in folder.glob("**/*.json"):
            del_group.create_task(file_check(file))


class GeoAggregator:
    payloads = {}
    save_trigger_count = {}
    bg_task_manager = None

    def __init__(
        self,
        task_group: aio.TaskGroup,
        storage_root="/mnt/hdd/PigNet/",
        log_name="GEOSCOPE.Subscriber",
        timestamp_conversion: Callable[[int], int] = None,
    ):
        self.root_path = Path(storage_root)
        self.logger = logging.getLogger(log_name)
        self.logging_sensors = False
        self.correct_timestamp = timestamp_conversion
        self.bg_task_manager = task_group

    async def save_sensor_data(self, node_id, data):
        save_time = datetime.now()
        node_name = f"GEOSCOPE_SENSOR_{node_id}"
        self.logger.debug("[%s] Trying to write file", node_name)

        folder_path = (
            self.root_path / "data" / save_time.strftime("%Y-%m-%d") / node_name
        )
        await folder_path.mkdir(parents=True, exist_ok=True)

        # Create json file
        file_path = folder_path / save_time.strftime("%Y-%m-%dT%H-%M-%S.json")
        async with file_path.open(mode="w", encoding="utf-8") as out_file:
            await out_file.write(json.dumps(data))
        self.logger.info("[%s]: %s file created", node_name, file_path.name)

    async def log_sensor(self, message, timestamp=datetime.now()):
        node_id = message.topic.split("/")[-1]

        try:
            sensor_data = json.loads(message.payload.decode("utf-8"))
        except json.JSONDecodeError:
            await self.json_error_log(message.payload)
            return
        except UnicodeDecodeError:
            await self.json_error_log(message.payload)
            return

        sensor_data["timestamp"] = int(timestamp.timestamp() * 1000)

        if node_id not in self.payloads:
            self.payloads[node_id] = []
            self.save_trigger_count[node_id] = randint(80, 120)

        self.payloads[node_id].append(sensor_data)
        self.logger.debug(
            "[%s] packet received (#%d)", node_id, len(self.payloads[node_id])
        )

        if len(self.payloads[node_id]) >= self.save_trigger_count[node_id]:
            save_this_sensor_coro = self.save_sensor_data(
                node_id, self.payloads[node_id][:]
            )
            self.payloads[node_id].clear()
            self.bg_task_manager.create_task(save_this_sensor_coro)

    async def json_error_log(self, payload: str):
        self.logger.error("Invalid JSON Packet:" "\n-----\n%s\n-----\n", payload)

    async def log_json_status(self, message):
        try:
            log_info = json.loads(message.payload.decode("utf-8"))
            self.logger.info("[%s]: %s", log_info["uuid"], log_info["data"])
        except json.JSONDecodeError:
            await self.json_error_log(message.payload)
        except UnicodeDecodeError:
            await self.json_error_log(message.payload)

    async def log_status(self, message):
        self.logger.info("[%s]: %s", message.topic, message.payload)

    async def flush(self):
        self.logger.info("Dumping In-Progress Sensor Data...")
        async with aio.TaskGroup() as write_tasks:
            for node, payload in self.payloads.items():
                save_this_sensor_coro = self.save_sensor_data(node, payload[:])
                payload.clear()
                write_tasks.create_task(aio.shield(save_this_sensor_coro))
