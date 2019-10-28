import sys
import os
import time
import json
import paho.mqtt.client as mqtt
from threading import Thread, Lock
from datetimes import date_time
from file_handler import file_manager
import logging

global_lock = Lock()


class mqtt_cli:
    counter = {}
    payloads = {}

    def __init__(self, id_list, ip="192.168.60.60", port=18884):
        self.BROKER_IP = ip
        self.BROKER_PORT = port
        self.timer = date_time()
        self.id_list = id_list
        self.logger = logging.getLogger(f"GEOSCOPE.MQTT_CLIENT")

    def async_push(self, client_id, payload):
        global global_lock
        while global_lock.locked():
            continue

        global_lock.acquire()

        folder_name = self.timer.date
        file_name = self.timer.time
        path = f"/media/hdd/data/{folder_name}/{client_id}"
        path_w_filename = f"{path}/{file_name}.json"
        # Create file directory
        os.makedirs(path, exist_ok=True)
        # Create json file
        with open(path_w_filename, "w") as out_file:
            json.dump(payload, out_file)
            out_file.close()
        self.logger.info(f"[{client_id}]: {file_name}.json file created")
        # self.logger.info(f"[{client_id}]: Starting upload data...")

        # cli_id = client_id
        # try:
        #     file_mng = file_manager(root_folder_name="Mixed pen")
        #     file_mng.create_date_folder(folder_name)
        #     file_mng.set_sensor_name(cli_id)
        #     file_mng.push_data(file_name=file_name, date=folder_name)
        #     self.logger.info(f"[{client_id}]: Finish upload data.")
        # except:
        #     self.logger.warning(f"[{client_id}]: Upload data failed.")
        # finally:
        global_lock.release()

    def on_message(self, client, userdata, message):
        self.timer.now()
        cli_id = message.topic.replace("geoscope/node1/", "")

        sensor_data = json.loads(message.payload.decode("utf-8"))
        sensor_data["timestamp"] = self.timer.timestamp
        self.payloads[cli_id].append(sensor_data)
        # self.logger.info(f"[GEOSCOPE_SENSOR_{cli_id}]: data recieved {self.counter[cli_id]}")
        self.counter[cli_id] = self.counter[cli_id] + 1

        if self.counter[cli_id] == 100:
            # push
            payload = self.payloads[cli_id]
            client_id = f"GEOSCOPE_SENSOR_{cli_id}"
            t = Thread(target=self.async_push, args=(client_id, payload))
            t.start()
            self.payloads[cli_id] = []
            self.counter[cli_id] = 0

    def start(self):
        try:
            self.logger.info(f"Starting MQTT Subscibe service...")
            mqtt_client = mqtt.Client("GEOSCOPE_Subsciber")
            mqtt_client.on_message = self.on_message
            mqtt_client.connect(
                host=self.BROKER_IP, port=self.BROKER_PORT, keepalive=300
            )
            for cli_id in self.id_list:
                client_id = f"GEOSCOPE_SENSOR_{cli_id}"
                topic = f"geoscope/node1/{str(cli_id)}"
                mqtt_client.subscribe(topic, 0)
                self.logger.info(f"[{client_id}]: Subscribed")
                self.counter[str(cli_id)] = 0
                self.payloads[str(cli_id)] = []

            self.logger.info("Starting MQTT Loop...")
            mqtt_client.loop_forever()
        except KeyboardInterrupt:
            self.logger.info(f"Exit MQTT Subscibe service...")
            sys.exit(0)
