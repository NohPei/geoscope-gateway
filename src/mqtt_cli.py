import sys
import os
import time
import json
import logging
import random
import signal
from threading import Thread, Lock
import paho.mqtt.client as mqtt
from datetimes import date_time

class mqtt_cli:
    payloads = {}
    folder_lock = Lock()

    def __init__(self, id_list, ip="127.0.0.1", port=18884):
        self.BROKER_IP = ip
        self.BROKER_PORT = port
        self.timer = date_time()
        self.id_list = id_list
        self.logger = logging.getLogger(f"GEOSCOPE.MQTT_CLIENT")

    def async_push(self, cli_id, payload):

        folder_name = self.timer.date
        file_name = self.timer.time
        client_id = f"GEOSCOPE_SENSOR_{cli_id}"
        path = f"/media/hdd/data/{folder_name}/{client_id}"
        path_w_filename = f"{path}/{file_name}.json"

        self.folder_lock.acquire() # this will block until the lock is available
        # Create file directory, the only operation that needs to be atomicized
        os.makedirs(path, exist_ok=True)
        # Release Lock now that files are unique
        self.folder_lock.release()
        # Create json file
        with open(path_w_filename, "w") as out_file:
            json.dump(payload, out_file)
            out_file.close()
        self.logger.info(f"[{client_id}]: {file_name}.json file created")

    def on_message(self, client, userdata, message):
        self.timer.now()
        cli_id = message.topic.replace("geoscope/node1/", "")

        sensor_data = json.loads(message.payload.decode("utf-8"))
        sensor_data["timestamp"] = self.timer.timestamp
        self.payloads[cli_id].append(sensor_data)
        # self.logger.info(f"[GEOSCOPE_SENSOR_{cli_id}]: data recieved {self.counter[cli_id]}")

        if len(self.payloads[cli_id]) >= 100:
            # push
            payload = self.payloads[cli_id]
            t = Thread(target=self.async_push, args=(cli_id, payload))
            t.start()
            self.payloads[cli_id].clear()

    def start(self):
        self.logger.info("Starting MQTT Subscibe service...")
        mqtt_client = mqtt.Client("GEOSCOPE_Subsciber")
        mqtt_client.on_message = self.on_message
        mqtt_client.connect( host=self.BROKER_IP, port=self.BROKER_PORT,
                            keepalive=300)
        for cli_id in self.id_list:
            client_id = f"GEOSCOPE_SENSOR_{cli_id}"
            topic = f"geoscope/node1/{str(cli_id)}"
            mqtt_client.subscribe(topic, 0)
            self.logger.info(f"[{client_id}]: Subscribed")
            self.payloads[str(cli_id)] = []

            # set up signal handlers for clean shutdown
            signal.signal(signal.SIGTERM, self.exit)
            signal.signal(signal.SIGINT, self.exit)
            signal.signal(signal.SIGABRT, self.exit)

            self.logger.info("Starting MQTT Loop...")
        try:
            mqtt_client.loop_forever()
        except KeyboardInterrupt:
            self.exit()

    def exit(self):
        self.logger.info("MQTT Subscribe Service Dumping In-Progress Files")
        dumping_threads = []

        for cli_id in self.id_list: # start a thread dumping each sensor's data
            t = Thread(target=self.async_push, args=(cli_id,
                                                     self.payloads[cli_id]))
            t.start()
            dumping_threads.append(t)

            for thread in dumping_threads:
                thread.join() # wait for them all to finish


            self.logger.info("Exit MQTT Subscibe service...")
            sys.exit(0)
