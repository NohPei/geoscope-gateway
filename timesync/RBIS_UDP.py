import asyncio as aio
import socket

class UDPCountBroadcaster(aio.DatagramProtocol):
    counter = 0

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
        self.transport.sendto(self.counter.to_bytes(1, 'little'))
        self.counter = (self.counter + 1) % 256
            # increment self.counter, but keep it to one byte


async def RBIS_loop(target_address='10.244.0.255', port = 2323, rep_sec = 1):
    loop = aio.get_running_loop()
    broadcaster_done = loop.create_future()
    await loop.create_datagram_endpoint(lambda:
                                                              UDPCountBroadcaster(rep_sec, loop, broadcaster_done),
                                                              remote_addr=(target_address,
                                                                           port),
                                                              allow_broadcast=True)
    await broadcaster_done




