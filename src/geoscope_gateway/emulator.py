#!/bin/python

import asyncio as aio
from datetime import datetime
import ujson as json
import asyncio_mqtt as mqtt
from .pignet import maintain_mqtt

payload = {}
payload["gain"] = 100
payload["data"] = [4095 for i in range(500)]


class GeoEmulator:
    def __init__(self, client_id: str, broker="127.0.0.1", port=18884):
        self.client_id = client_id
        self.broker_host = broker
        self.broker_port = port

    async def run(self, interval):
        await maintain_mqtt(self._client_loop, interval)

    async def _client_loop(self, interval):
        async with mqtt.Client(
            hostname=self.broker_host,
            port=self.broker_port,
            client_id=f"GEOSCOPE_{self.client_id}",
            clean_session=True,
        ) as client:
            await self._startup_messages(client)
            while True:
                await aio.sleep(interval)
                await self._send_packet(client)

    async def _startup_messages(self, client):
        startup = {}
        startup["uuid"] = f"GEOSCOPE_{self.client_id}"
        startup["data"] = "[Device Started]"
        await client.publish(topic="geoscope/reply", payload=json.dumps(startup))

        startup["data"] = f'[Current Gain]: {payload["gain"]}'
        await client.publish(topic="geoscope/reply", payload=json.dumps(startup))

    async def _send_packet(self, client):
        toSend = payload
        toSend["uuid"] = f"GEOSCOPE_{self.client_id}"
        toSend["sendTime"] = int(datetime.now().timestamp() * 1e6)
        await client.publish(
            topic=f"geoscope/node1/{self.client_id}", payload=json.dumps(toSend)
        )


DEFAULT_CLIENT_LIST = [10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 30, 31, 32, 33, 34]


async def emulate_sensors(
    client_list=[], broker="PigServer-USMARC.pignet", port=18884, interval=0.5
):
    emulators = set()
    tasks = set()
    for node_id in client_list:
        new_sensor = GeoEmulator(node_id, broker, port)
        emulators.add(new_sensor)
        loop_task = aio.create_task(new_sensor.run(interval))
        tasks.add(loop_task)

    await aio.gather(*tasks)


if __name__ == "__main__":
    aio.run(emulate_sensors(DEFAULT_CLIENT_LIST))
