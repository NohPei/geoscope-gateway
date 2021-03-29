#!/bin/python

import json
import time
from threading import Timer
import paho.mqtt.client as mqtt

payload = {}
payload["gain"] = 100
payload["data"] = [4095 for i in range(500)]

class sensor_emulator:

    def __init__(self, client_id, addr="127.0.0.1", port=18884):
        self.id = client_id
        self.client = mqtt.Client(f"GEOSCOPE_SENSOR_{self.id}")
        self.client.connect(host=addr, port=port, keepalive=300)

        startup = {}
        startup["uuid"] = f"GEOSCOPE-{self.id}"
        startup["data"] = "[Device Started]"
        self.client.publish(topic="geoscope/reply",
                            payload=json.dumps(startup))

        startup["data"] = f'[Current Gain: {payload["gain"]}'
        self.client.publish(topic="geoscope/reply",
                            payload=json.dumps(startup))

        self.timer = loopingTimer(1, self.send_packet)
        self.start()


    def start(self):
        self.client.loop_start()
        self.timer.start()


    def stop(self):
        self.timer.stop()
        self.client.loop_stop()

    def send_packet(self):
        toSend = payload
        toSend["uuid"] = f"GEOSCOPE-{self.id}"
        self.client.publish(topic=f'geoscope/node1/{self.id}',
                            payload=json.dumps(toSend))

class loopingTimer():
    def __init__(self, interval, handler):
        self.hFunc = handler
        self.interval = interval
        self.thread = Timer(self.interval, self.handle_timer)
        self.thread.daemon = True
        self.running = False

    def handle_timer(self):
        self.hFunc()
        if self.running:
            self.thread = Timer(self.interval, self.handle_timer)
            self.thread.daemon = True
            self.thread.start()

    def start(self):
        self.running = True
        if not self.thread.is_alive():
            self.thread.start()

    def stop(self):
        self.running = False

    def cancel(self):
        self.stop()
        self.thread.cancel()

cli_list = [ 10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 30, 31, 32, 33, 34 ]

def emulate(broker="PigServer-PiMARC.lan"):
    sensors = []
    for id in cli_list:
        new_sensor = sensor_emulator(id, addr=broker)
        sensors.append(new_sensor)

    while True:
        time.sleep(5)

if __name__ == "__main__":
    emulate()
