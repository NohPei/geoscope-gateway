import time
import json
import logging
import paho.mqtt.client as mqtt
from mqtt_cli import mqtt_cli


logger = logging.getLogger("GEOSCOPE.Monitoring")
logger.setLevel(logging.INFO)

def on_message(client, userdata, message):
    if message.topic.startswith("geoscope"):
        try:
            reply_message = json.loads(str(message.payload))
            logger.info("[%s]: %s", reply_message['uuid'],
                        reply_message['data'])
        except json.decoder.JSONDecodeError:
            logger.error("Invalid JSON Packet on [%s]: \n-----\n%s\n-----\n",
                         message.topic, message.payload);
    else:
        logger.info("[%s]: %s", message.topic, message.payload)


log_topics = ["geoscope/reply", "$SYS/broker/log/E", "$SYS/broker/log/W"]


def monitor_geophones():
    logger.info("# Starting Geophone Response Monitor")
    paho_client = mqtt.Client("GEOSCOPE_Monitoring", clean_session=False)
    client = mqtt_cli([], client=paho_client, logger_name=logger.name, extra_topics=log_topics)
    client.mqtt_client.on_message=on_message
    client.connect()

    logger.info("Starting MQTT Loop...")
    client.mqtt_client.loop_forever()


if __name__ == "__main__":
    logger.info("## Starting program")
    monitor_geophones()
