#!/bin/python

import json
import asyncio as aio
from datetime import datetime
import uvloop
import asyncio_mqtt as mqtt

payload = {}
payload["gain"] = 100
payload["data"] = [4095 for i in range(500)]

class sensor_emulator:

    def __init__(self, client_id: str, broker="127.0.0.1", port=18884, *args, **kwargs):
        self.client_id = client_id
        self.clientargs = {"hostname": broker, "port": port, "args": args, "kwargs": kwargs}

    async def run(self, interval):
        async with mqtt.Client(self.clientargs["broker"],
                         port=self.clientargs["port"],
                         client_id=f"GEOSCOPE-{self.id}",
                         *self.clientargs["args"], **self.clientargs["kwargs"])
        as client:
            self._client = client
            await self._startup_messages()
            while True:
                await aio.sleep(interval)
                await self._send_packet()

    async def _startup_messages(self):
        startup = {}
        startup["uuid"] = f"GEOSCOPE-{self.client_id}"
        startup["sendTime"] = datetime.timestamp()
        startup["data"] = "[Device Started]"
        await self._client.publish(topic="geoscope/reply",
                            payload=json.dumps(startup))

        startup["data"] = f'[Current Gain: {payload["gain"]}'
        startup["sendTime"] = datetime.timestamp()
        await self._client.publish(topic="geoscope/reply",
                            payload=json.dumps(startup))

    async def _send_packet(self):
        toSend = payload
        toSend["uuid"] = f"GEOSCOPE-{self.client_id}"
        toSend["sendTime"] = datetime.timestamp()
        await self._client.publish(topic=f'geoscope/node1/{self.client_id}',
                            payload=json.dumps(toSend))

cli_list = [ 10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 30, 31, 32, 33, 34 ]

async def emulate(client_list=[] , broker="PigServer-PiMARC.lan", port=18884):
    emulators = set()
    tasks = set()
    for node_id in client_list:
        new_sensor = sensor_emulator(node_id, broker, port)
        emulators.add(new_sensor)
        loop_task = aio.create_task(new_sensor.run(0.5))
        tasks.add(loop_task)

    await aio.gather(*tasks)

if __name__ == "__main__":
    uvloop.install()
    aio.run(emulate(cli_list))
