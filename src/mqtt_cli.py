import os
import json
import logging
from threading import Thread, Lock
import paho.mqtt.client as mqtt
from datetimes import date_time

class mqtt_cli:
    payloads = {}
    folder_lock = Lock()
    list_locks = {}

    def __init__(self, id_list, ip="127.0.0.1", port=18884,
                 client=mqtt.Client("GEOSCOPE_Subscriber",
                                    clean_session=False),
                 logger_name="GEOSCOPE.MQTT_CLIENT", extra_topics=[]):
        self.BROKER_IP = ip
        self.BROKER_PORT = port
        self.timer = date_time()
        self.id_list = id_list
        self.topics = extra_topics
        self.logger = logging.getLogger(logger_name)
        self.mqtt_client = client
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.enable_logger(logger=logging.getLogger(logger_name+".client"))

    def async_push(self, cli_id, payload):

        folder_name = self.timer.date
        file_name = self.timer.time
        client_id = f"GEOSCOPE_SENSOR_{cli_id}"
        path = f"/mnt/hdd/PigNet/data/{folder_name}/{client_id}"
        path_w_filename = f"{path}/{file_name}.json"

        if (self.folder_lock.acquire(timeout=5)): #this will block until the lock is available
            # Create file directory, the only operation that needs to be atomicized
            os.makedirs(path, exist_ok=True)
            # Release Lock now that files are unique
            self.folder_lock.release()
        else: # if we couldn't get the lock
            self.logger.critical("Couldn't get lock to create '%s', restarting", path)
            raise RuntimeError("Folder Creation Deadlocked")
            # crash. Most likely a thread was killed while holding the lock


        # Create json file
        with open(path_w_filename, "w") as out_file:
            json.dump(payload, out_file)
            out_file.close()
        self.logger.info("[%s]: %s.json file created", client_id, file_name)

    def on_message(self, client, userdata, message):
        self.timer.now()
        cli_id = message.topic.replace("geoscope/node1/", "")

        sensor_data = json.loads(message.payload.decode("utf-8"))
        sensor_data["timestamp"] = self.timer.timestamp
        self.list_locks[cli_id].acquire()
        self.payloads[cli_id].append(sensor_data)
        self.list_locks[cli_id].release()
        # self.logger.info(f"[GEOSCOPE_SENSOR_{cli_id}]: data recieved {self.counter[cli_id]}")

        if len(self.payloads[cli_id]) >= 100:
            # push
            self.list_locks[cli_id].acquire()
            payload = self.payloads[cli_id]
            t = Thread(target=self.async_push, args=(cli_id, payload))
            t.start()
            self.payloads[cli_id] = []
            self.list_locks[cli_id].release()

    def on_disconnect(self, client, userdata, rc):
        self.logger.warning("Subscriber Client Disconnected")
        if rc != 0: # for unexpected disconnects
            self.mqtt_client.reconnect()
            # try to reconnect

    CONNECT_RESTART_CODES = {2,3,5}
        # 2: invalid client ID
        # 3: server unavailable
        # 5: not authorized
    CONNECT_OK_CODES = {0}
        # 0: Connection Successful
    def on_connect(self, client, userdata, flags, rc):
        if rc in self.CONNECT_RESTART_CODES: # on a server error
            self.logger.warning("Connection Failed, Re-trying")
            self.mqtt_client.reconnect()
            # try to reconnect
        elif rc in self.CONNECT_OK_CODES:
            self.logger.info("Subscriber Client Connected")
            self.subscribe()
        else:
            self.logger.error("Can't Connect to Broker on %s:%i", self.BROKER_IP, self.BROKER_PORT)
            raise ConnectionError(client)

    def connect(self):
        self.mqtt_client.connect(host=self.BROKER_IP, port=self.BROKER_PORT,
                                 keepalive=300)

    def subscribe(self):
        for cli_id in self.id_list:
            client_id = f"GEOSCOPE_SENSOR_{cli_id}"
            topic = f"geoscope/node1/{str(cli_id)}"
            self.mqtt_client.subscribe(topic, 0)
            self.logger.info("[%s]: Subscribed", client_id)

        for topic in self.topics:
            self.mqtt_client.subscribe(topic, 0)
            self.logger.info("[%s]: Subscribed", topic)

    def start(self):
        self.logger.info("Starting MQTT Subscibe service...")
        self.connect()

        for cli_id in self.id_list:
            self.payloads[str(cli_id)] = []
            self.list_locks[str(cli_id)] = Lock()

        self.logger.info("Starting MQTT Loop...")
        self.mqtt_client.loop_forever()

    def __del__(self):
        self.logger.info("Dumping In-Progress Files")
        dumping_threads = []

        for cli_id in self.id_list: # start a thread dumping each sensor's data
            t = Thread(target=self.async_push, args=(cli_id,
                                                     self.payloads[cli_id]))
            t.start()
            dumping_threads.append(t)

        for thread in dumping_threads:
            thread.join() # wait for them all to finish

        self.logger.info("Exit MQTT Subscibe service...")
