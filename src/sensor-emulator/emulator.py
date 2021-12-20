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

    def __init__(self, client_id: str, client: mqtt.Client):
        self.id = client_id
        self.client = client

    async def repeat_send(self, interval):
        while True:
            await aio.sleep(interval)
            await self.send_packet()


    async def startup_messages(self):
        startup = {}
        startup["uuid"] = f"GEOSCOPE-{self.id}"
        startup["sendTime"] = datetime.timestamp()
        startup["data"] = "[Device Started]"
        await self.client.publish(topic="geoscope/reply",
                            payload=json.dumps(startup))

        startup["data"] = f'[Current Gain: {payload["gain"]}'
        startup["sendTime"] = datetime.timestamp()
        await self.client.publish(topic="geoscope/reply",
                            payload=json.dumps(startup))

    async def send_packet(self):
        toSend = payload
        toSend["uuid"] = f"GEOSCOPE-{self.id}"
        toSend["sendTime"] = datetime.timestamp()
        await self.client.publish(topic=f'geoscope/node1/{self.id}',
                            payload=json.dumps(toSend))

cli_list = [ 10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 30, 31, 32, 33, 34 ]

async def emulate(client_list=[] , broker="PigServer-PiMARC.lan", port=18884):
    emulators = set()
    tasks = set()
    async with mqtt.Client(broker, port) as client:
        for node_id in client_list:
            new_sensor = sensor_emulator(node_id, client)
            emulators.add(new_sensor)
            await new_sensor.startup_messages()
            loop_task = aio.create_task(new_sensor.repeat_send())
            tasks.add(loop_task)

    await aio.gather(*tasks)

if __name__ == "__main__":
    uvloop.install()
    aio.run(emulate(cli_list))
