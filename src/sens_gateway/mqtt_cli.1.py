import sys
import paho.mqtt.client as mqtt
import time
import json
from datas import data_collection
from threading import Thread


class mqtt_cli:
    BROKER_IP = "0.0.0.0"
    BROKER_PORT = 0
    MQTT_CLIENT_ID = "GEOSCOPE"
    MQTT_TOPIC = "TOPIC"

    API_KEY = "KEY"
    API_SECRET = "SECRET"

    START_TIME = time.time()
    counter = 0
    data_counter = 0
    payloads = []

    def __init__(self, ip="192.168.60.1", port=18884, id="GEOSCOPE", topic="TOPIC", key="KEY", secret="SECRET"):
        self.BROKER_IP = ip
        self.BROKER_PORT = port
        self.MQTT_CLIENT_ID = id
        self.MQTT_TOPIC = topic

        self.API_KEY = key
        self.API_SECRET = secret

    def async_send(self, payloads):
        dc = data_collection()
        dc.setKey(self.API_KEY)
        dc.setSecret(self.API_SECRET)
        dc.send(payloads)

    def on_message(self, client, userdata, message):
        if self.data_counter == 10:
            self.data_counter = 1
            t = Thread(target=self.async_send, args=[self.payloads])
            t.daemon = True
            t.start()
            self.payloads.clear()
        else:
            self.data_counter = self.data_counter + 1

        ts = int(round(time.time() * 1000))
        upTim = time.time() - self.START_TIME
        ttopic = message.topic
        sensor_data = json.loads(str(message.payload.decode("utf-8")))
        sensor_data['ts'] = ts
        sensor_data['timestamp'] = ts
        self.payloads.append(sensor_data)
        print("On message Timestamp: {}\tTopic: {}\tcouter:{}\tUptime: {:.3f}".format(
            time.strftime('%Y-%m-%d %H:%M:%S'), ttopic, self.counter, upTim))
        self.counter = self.counter + 1

    def start(self):
        try:
            print("------------------------------------------------------")
            print("## Starting MQTT Subscibe service...")
            mqtt_client = mqtt.Client(self.MQTT_CLIENT_ID)
            mqtt_client.on_message = self.on_message
            mqtt_client.connect(host=self.BROKER_IP, port=self.BROKER_PORT)
            mqtt_client.subscribe(self.MQTT_TOPIC, 0)
            print(f"## Subscribe topic: {self.MQTT_TOPIC}")
            print(f"## MQTT Client: {self.MQTT_CLIENT_ID}")
            print("------------------------------------------------------")
            mqtt_client.loop_forever()
        except KeyboardInterrupt:
            print("------------------------------------------------------")
            print("## Exit program...")
            sys.exit(0)
