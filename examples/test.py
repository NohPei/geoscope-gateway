#!/bin/python
import asyncio as aio
import geoscope_gateway

INTERVAL = 0.5
ID_LIST = [f"E-{j}" for j in range(5)]


async def run_main():
    geoscope_gateway.logger.info("## Starting Test with Local Emulators")
    async with aio.TaskGroup() as tg:
        geoscope_gateway.logger.info("## Starting MQTT Loop")
        tg.create_task(
            geoscope_gateway.maintain_mqtt(
                geoscope_gateway.pignet, root_dir="./test-store/"
            )
        )

        geoscope_gateway.logger.info("## Starting Emulated Sensors")
        emulators = set()
        for client_id in ID_LIST:
            new_sensor = geoscope_gateway.GeoEmulator(client_id)
            emulators.add(new_sensor)
            tg.create_task(new_sensor.run(INTERVAL))
            geoscope_gateway.logger.info(f'# Started emulator "{client_id}" ')


aio.run(run_main())
