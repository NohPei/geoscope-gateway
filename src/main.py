from mqtt_cli import mqtt_cli
from threading import Thread

import time

## Logging
import logging

logger = logging.getLogger("GEOSCOPE")
logger.setLevel(logging.DEBUG)
file_log_handler = logging.FileHandler(
    f"/media/hdd/log/GEOSCOPE-{time.strftime('%Y-%m-%d')}.log"
)
file_log_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt="%(asctime)s %(message)s", datefmt="%Y/%m/%d %I:%M:%S %p")
file_log_handler.setFormatter(formatter)

logger.addHandler(file_log_handler)
client_id_list = [151, 152, 153, 154, 155, 156, 157, 158, 159, 160]


def main():
    logging.info("## Starting program")
    mqtt_client = mqtt_cli(id_list=client_id_list)
    mqtt_client.start()
    logging.info("## End.")


if __name__ == "__main__":
    main()
