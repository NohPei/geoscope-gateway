import time
import json
import logging
import paho.mqtt.client as mqtt
from mqtt_cli import mqtt_cli


logger = logging.getLogger("Monitoring")
logger.setLevel(logging.INFO)
file_log_handler = logging.FileHandler(f"/media/hdd/log/STATUS-{time.strftime('%Y-%m-%d')}.log")
file_log_handler.setLevel(logging.INFO)

console_log_handler = logging.StreamHandler()
console_log_handler.setLevel(logging.INFO)

formatter = logging.Formatter(fmt="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
file_log_handler.setFormatter(formatter)
console_log_handler.setFormatter(formatter)

logger.addHandler(file_log_handler)
logger.addHandler(console_log_handler)


def on_message(client, userdata, message):
    reply_message = json.loads(message.payload.decode("utf-8"))
    logger.info("[%s]: %s", reply_message['uuid'], reply_message['data'])


def monitor_geophones():
    logger.info("# Starting Geophone Response Monitor")
    client = mqtt_cli([], client=mqtt.Client("GEOSCOPE_Monitoring"),
                      logger_name="Monitoring.MQTT")
    client.mqtt_client.on_message=on_message
    client.connect()
    client.mqtt_client.subscribe("geoscope/reply", 0)

    logger.info("Starting MQTT Loop...")
    client.mqtt_client.loop_forever()


if __name__ == "__main__":
    logger.info("## Starting program")
    monitor_geophones()
