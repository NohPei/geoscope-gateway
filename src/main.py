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

from sens_gateway.mqtt_cli import mqtt_cli
from threading import Thread

import time

## Logging
import logging

logger = logging.getLogger("GEOSCOPE")
logger.setLevel(logging.DEBUG)

file_log_handler = logging.FileHandler(
    f"GEOSCOPE-{time.strftime('%Y-%m-%dT%H-%M-%S')}.log"
)
file_log_handler.setLevel(logging.DEBUG)

console_log_handler = logging.StreamHandler()
console_log_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
file_log_handler.setFormatter(formatter)
console_log_handler.setFormatter(formatter)

logger.addHandler(file_log_handler)
logger.addHandler(console_log_handler)

## MQTT Broker [ip, port]
BROKER_IP = "192.168.60.60"
BROKER_PORT = 18884

## GEOSCOPE List [ip number]
mqtt_threads = []
client_id_list = [151, 152, 153, 154]


def spawn_geoscope(MQTT_CLIENT_ID, MQTT_TOPIC):
    ## spawn mqtt client
    logging.info(f"## [SPAWN]: {MQTT_CLIENT_ID}")
    mqtt_client = mqtt_cli(ip=BROKER_IP, port=BROKER_PORT, id=MQTT_CLIENT_ID, topic=MQTT_TOPIC)
    mqtt_client.start()


def main():
    logging.info("## Starting program")
    for c_id in client_id_list:
        client_id = f"GEOSCOPE_SENSOR_{str(c_id)}"
        topic = f"geoscope/node1/{str(c_id)}"
        t = Thread(target=spawn_geoscope, args=(client_id, topic))
        mqtt_threads.append(t)
        t.start()


if __name__ == "__main__":
    main()
