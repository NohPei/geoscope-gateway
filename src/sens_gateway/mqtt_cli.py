import sys
from pathlib import Path  # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError:  # Already removed
    pass

import sys
import os
import paho.mqtt.client as mqtt
import time
import json
from threading import Thread
from datetimes import date_time
from file_handler import file_manager


class mqtt_cli:
    BROKER_IP = "0.0.0.0"
    BROKER_PORT = 0
    MQTT_CLIENT_ID = "GEOSCOPE"
    MQTT_TOPIC = "TOPIC"

    START_TIME = time.time()
    counter = 0
    data_counter = 0
    payloads = []

    def __init__(self, ip="192.168.60.1", port=18884, id="GEOSCOPE", topic="TOPIC"):
        self.BROKER_IP = ip
        self.BROKER_PORT = port
        self.MQTT_CLIENT_ID = id
        self.MQTT_TOPIC = topic

        self.timer = date_time()

    def asyn_data_push(self, payloads):
        folder_name = self.timer.date
        file_name = self.timer.time
        path = f"data/Mixed pen/{folder_name}/{self.MQTT_CLIENT_ID}"
        path_w_filename = f"{path}/{file_name}.json"
        # Create file directory
        os.makedirs(path, exist_ok=True)
        # Create json file
        with open(path_w_filename, 'w') as out_file:
            json.dump(payloads, out_file)
        print(f"> Created file: {file_name}.json")

        file_mng = file_manager(
            root_folder_name="Mixed pen", sensor_name=self.MQTT_CLIENT_ID)

        file_mng.create_date_folder(folder_name)
        file_mng.set_sensor_name(self.MQTT_CLIENT_ID)
        file_mng.push_data(
            payloads=payloads, file_name=file_name, date=folder_name)

    def on_message(self, client, userdata, message):
        self.timer.now()
        if self.data_counter == 100:
            self.data_counter = 1
            tmp_payloads = self.payloads.copy()
            t = Thread(target=self.asyn_data_push,
                       kwargs=dict(payloads=tmp_payloads))
            # t.daemon = True
            t.start()
            self.payloads.clear()
        else:
            self.data_counter = self.data_counter + 1

        upTim = time.time() - self.START_TIME
        ttopic = message.topic
        try:
            sensor_data = json.loads(message.payload.decode("utf-8"))
            sensor_data['ts'] = self.timer.timestamp
            sensor_data['timestamp'] = self.timer.timestamp
            self.payloads.append(sensor_data)
            print("On message Timestamp: {}\tTopic: {}\tcouter:{}\tUptime: {:.3f}".format(
                self.timer.date, ttopic, self.counter, upTim))
            self.counter = self.counter + 1
        except:
            if self.data_counter > 1:
                self.data_counter = self.data_counter - 1

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
