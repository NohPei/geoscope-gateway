#!/bin/python
import asyncio as aio
from contextlib import AsyncExitStack
from periphery import Serial, GPIO
import geoscope_gateway


interrupt_pin_num = (ord('E')-ord('A'))*32 + 0
    # for pin PE0

gpio_pin = GPIO("/dev/gpiochip0", interrupt_pin_num, "out")
serial_port = Serial('/dev/ttyUSB0', 115200)

async def run_main():
    geoscope_gateway.logger.info("## Starting Capture and Timesync")
    async with AsyncExitStack() as stack:
        stack.callback(serial_port.close)
        stack.callback(gpio_pin.close)


        time_manager = geoscope_gateway.timesync.ESPSerialTime(serial_port, gpio_pin, buf_len=1000)
        geoscope_gateway.logger.info("## Starting Serial Timesync")
        await time_manager.start()
        geoscope_gateway.logger.info("## Starting MQTT Loop")
        await geoscope_gateway.maintain_mqtt(geoscope_gateway.pignet, time_sync=time_manager)

aio.run(run_main())
