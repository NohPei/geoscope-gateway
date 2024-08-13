#!/bin/python
import asyncio as aio
import geoscope_gateway


async def run_main():
    geoscope_gateway.logger.info("## Starting Capture and Timesync")

    await geoscope_gateway.maintain_mqtt(
        geoscope_gateway.pignet,
        root_dir="/path/to/store/data/and/logs/",
        broker_host="127.0.0.1",
        broker_port=18884,
    )


aio.run(run_main())
