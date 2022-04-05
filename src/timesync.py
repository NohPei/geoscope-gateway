from datetime import datetime
from contextlib import AsyncExitStack
from io import IOBase
import asyncio as aio
import sliplib
import periphery
import socket
from .pignet import maintain_mqtt


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

async def mqttMicrosLoop(topic='geoscope/micros', broker_host='127.0.0.1',
                         broker_port='18884', **kwargs):
    def run_client():
        client = mqtt.Client(hostname=broker_host, port=broker_port,
                             clean_session=False,
                             client_id="PigNet Timestamp Source")


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


class UDPTimestampBroadcaster(aio.DatagramProtocol):
    def __init__(self, repeat_sec, loop, disconn_future):
        self.loop = loop
        self.dead_flag = disconn_future
        self.repeat_time = repeat_sec

    def connection_made(self, transport):
        self.transport = transport

        # configure the underlying socket for broadcasting
        raw_sock = transport.get_extra_info("socket")
        raw_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.send()

    def connection_lost(self, exc):
        self.dead_flag.set_result(True)

    def send(self):
        self.loop.call_later(self.repeat_time, self.send)
        current_time = int(datetime.now().timestamp() * 1e6) % (2**64)
            # get the current time as as 64-bit microseconds count
        self.transport.sendto(current_time.to_bytes(8, byteorder='little'))
        # send that timestamp as a 64b little-endian int

async def UDPMicrosLoop(target_address='10.244.0.255', port = 2323, rep_sec = 1):
    loop = aio.get_running_loop()
    broadcaster_done = loop.create_future()
    try:
        endpoint_coro = loop.create_datagram_endpoint(lambda:
                                                      UDPTimestampBroadcaster(rep_sec,
                                                                              loop,
                                                                              broadcaster_done),
                                                      remote_addr=(target_address,
                                                                   port),
                                                      allow_broadcast=True)
        transport, protocol = await endpoint_coro
        await broadcaster_done
    finally:
        transport.close()
