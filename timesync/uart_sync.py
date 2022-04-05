from datetime import datetime
from contextlib import AsyncExitStack
from io import IOBase
import asyncio as aio
import sliplib
import periphery
import asyncio_mqtt as mqtt


async def pulse_gpio(gpio_dev, pulse_sec):
    await aio.to_thread(gpio_dev.write, True)
    await aio.sleep(pulse_sec)
    await aio.to_thread(gpio_dev.write, False)

async def send_timestamp(destination: IOBase):
    time = int(datetime.now().timestamp()*1e6)
    time_msg = sliplib.encode(time.to_bytes(8, byteorder='little'))
    await aio.to_thread(destination.write, time_msg)

async def serialMicrosLoop(port='/dev/ttyUSB0', baudrate=256000, **kwargs):
    serial = periphery.Serial(port, baudrate)
    await timestampMicrosLoop(serial, **kwargs)

async def mqttMicrosLoop(topic='geoscope/micros', broker_host='127.0.0.1', broker_port='18884', **kwargs):
    pass

async def timestampMicrosLoop(output_context_mgr, repeat_sec=1, interrupt_pin=None):
    async with AsyncExitStack() as stack: # Manages device cleanup for us
        tasks = set()
        output = stack.enter_context(output_context_mgr) # Activate whatever our output is
        gpio = None
        if interrupt_pin is not None: # if we've been told to run both, also set up the GPIO device
            gpio = stack.enter_context(periphery.GPIO("/dev/gpiochip0", interrupt_pin, direction="out"))

        # main loop
        while True:
            if gpio is not None: # if GPIO is set up, also pulse the interrupt pin
                tasks.add(pulse_gpio(gpio, repeat_sec/10))
            tasks.add(send_timestamp(output))
            await aio.gather(*tasks) # start both tasks roughly simultaneously
            tasks.clear()
            await aio.sleep(repeat_sec)
