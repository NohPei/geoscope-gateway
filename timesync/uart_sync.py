from datetime import datetime
import asyncio as aio
import serial_asyncio as aio_serial
import sliplib

class SerialMicrosSender(aio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def send_timestamp(self):
        time = int(datetime.now().timestamp()*1e6)
        self.transport.write(sliplib.encode(f'{time:x}'.encode()))


async def serialMicrosLoop(port='/dev/ttyUSB0', baudrate=256000, repeat_sec=1):
    loop = aio.get_running_loop()
    transport, protocol = await aio_serial.create_serial_connection(loop, SerialMicrosSender, port, baudrate=baudrate)
    try:
        while True:
            protocol.send_timestamp()
            await aio.sleep(repeat_sec)
    finally:
        transport.close()

