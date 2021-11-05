import time
import json
import logging
import paho.mqtt.client as mqtt
from mqtt_cli import mqtt_cli


logger = logging.getLogger("GEOSCOPE.Monitoring")
logger.setLevel(logging.INFO)

def on_message(client, userdata, message):
    reply_message = json.loads(message.payload.decode("utf-8"))
    logger.info("[%s]: %s", reply_message['uuid'], reply_message['data'])

log_topics = ["geosctope/reply", "$SYS/broker/log/E", "$SYS/broker/log/W"]


def monitor_geophones():
    logger.info("# Starting Geophone Response Monitor")
    client = mqtt_cli([], client=mqtt.Client("GEOSCOPE_Monitoring",
                                             clean_session=False),
                      logger_name=logger.name, extra_topics=log_topics)
    client.mqtt_client.on_message=on_message
    client.connect()

    logger.info("Starting MQTT Loop...")
    client.mqtt_client.loop_forever()


if __name__ == "__main__":
    logger.info("## Starting program")
    monitor_geophones()
