import time
import json
import logging
import paho.mqtt.client as mqtt


logger = logging.getLogger("GEOSCOPE_MONITORING")
logger.setLevel(logging.DEBUG)
file_log_handler = logging.FileHandler(f"/media/hdd/log/STATUS-{time.strftime('%Y-%m-%d')}.log")
file_log_handler.setLevel(logging.DEBUG)

console_log_handler = logging.StreamHandler()
console_log_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
file_log_handler.setFormatter(formatter)
console_log_handler.setFormatter(formatter)

logger.addHandler(file_log_handler)
logger.addHandler(console_log_handler)

BROKER_IP = "127.0.0.1" # use local MQTT Broker
BROKER_PORT = 18884


def on_message(client, userdata, message):
    reply_message = json.loads(message.payload.decode("utf-8"))
    logger.info("[%s]: %s", reply_message['uuid'], reply_message['data'])


def mqtt_client():
    client = mqtt.Client("GEOSCOPE_Monitoring")
    client.on_message = on_message
    client.connect(host=BROKER_IP, port=BROKER_PORT)
    client.subscribe("geoscope/reply", 0)

    logger.info("Starting MQTT Loop...")
    client.loop_forever()


def main():
    logger.info("## Starting program")
    mqtt_client()


if __name__ == "__main__":
    main()
