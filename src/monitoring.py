import time
import json
import paho.mqtt.client as mqtt
import logging


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

BROKER_IP = "192.168.60.60"
BROKER_PORT = 18884


def on_message(client, userdata, message):
    reply_message = json.loads(message.payload.decode("utf-8"))
    logger.info(f"[{reply_message['uuid']}]: {reply_message['data']}")


def mqtt_client():
    mqtt_client = mqtt.Client("GEOSCOPE_Monitoring")
    mqtt_client.on_message = on_message
    mqtt_client.connect(host=BROKER_IP, port=BROKER_PORT)
    mqtt_client.subscribe("geoscope/reply", 0)

    logger.info("Starting MQTT Loop...")
    mqtt_client.loop_forever()


def main():
    logger.info("## Starting program")
    mqtt_client()


if __name__ == "__main__":
    main()
