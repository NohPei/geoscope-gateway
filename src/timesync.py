from datetime import datetime
from contextlib import AsyncExitStack
from io import IOBase
import asyncio as aio
import sliplib
import periphery
import socket
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from dvg_ringbuffer import RingBuffer


def system_micros_timestamp():
    return round(datetime.now().timestamp()*1e6) % 2**63

async def pulse_gpio(gpio_dev: IOBase, pulse_sec=0.1):
    await aio.to_thread(gpio_dev.write, True)
    pulse_time = system_micros_timestamp()
    await aio.sleep(pulse_sec)
    await aio.to_thread(gpio_dev.write, False)
    return pulse_time

async def send_timestamp(destination: IOBase):
    time = system_micros_timestamp()
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

class ESPSerialTime():
    model = None
    loop = None

    def __init__(self, serial_port: periphery.Serial, gpio_port: periphery.GPIO, interval_sec=2.0, poly_order=2, buf_len=500):
        self.serial = serial_port
        self.gpio = gpio_port
        self.repeat_sec = interval_sec
        self.degree = poly_order
        self.local_buf = RingBuffer(buf_len, allow_overwrite=True)
        self.esp_buf = RingBuffer(buf_len, allow_overwrite=True)
        pass

    def __del__(self):
        self.serial.close()
        self.gpio.close()

    async def start(self):
        self.loop = aio.get_running_loop()
        await self.timestamp_update()

    async def stop(self):
        self.loop = None

    async def __get_ts_from_serial(self):
        while (await aio.to_thread(self.serial.poll, 0)):
            bytes_to_read = await aio.to_thread(self.serial.input_waiting)
            await aio.to_thread(self.serial.read, length=bytes_to_read,
                                timeout=0)
        await aio.to_thread(self.serial.write, b't')
        ts_bytes = await aio.to_thread(self.serial.read(length=8))
        return int.from_bytes(ts_bytes, byteorder='little', signed=True)

    async def timestamp_update(self):
        if self.loop is not None: # still running if we have a loop
            self.loop.call_later(self.repeat_sec, self.timestamp_update)

        async def get_ts_pair():
            self.local_buf.append(await pulse_gpio(self.gpio))
            self.esp_buf.append(await self.__get_ts_from_serial())


        if self.model is None:
            for i in np.arange(self.degree + 1):
                await get_ts_pair()
        else:
            await get_ts_pair()

        self.model = Polynomial.fit(np.array(local_buf), np.array(esp_buf),
                                    deg=self.degree)


    def __call__(self, timestamp: int):
        if self.model is None:
            return timestamp
        return round(self.model(timestamp))

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
        current_time = system_micros_timestamp()
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
