import logging
import time
from multiprocessing import Process
from mqtt_cli import mqtt_cli
from monitoring import monitor_geophones


## Logging

logger = logging.getLogger("GEOSCOPE")
logger.setLevel(logging.INFO)
file_log_handler = logging.FileHandler(
    f"/media/hdd/log/GEOSCOPE-{time.strftime('%Y-%m-%d')}.log"
)
file_log_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s %(message)s", datefmt="%Y/%m/%d %I:%M:%S %p"
)
file_log_handler.setFormatter(formatter)

logger.addHandler(file_log_handler)
client_id_list = [
    151,
    152,
    153,
    154,
    155,
    156,
    157,
    158,
    159,
    160,
    161,
    162,
    163,
    164,
    165,
    166,
    167,
    168,
    169,
    170,
    171,
    172,
    173,
    174,
    175,
    176,
    177,
    178,
    179,
    180,
    181,
    182,
    183,
    184,
    185,
    186,
    187,
    188,
    189,
    190,
]



def datalog():
    logging.info("## Starting data logging program")
    mqtt_client = mqtt_cli(id_list=client_id_list)
    mqtt_client.start()
    logging.info("## End data capture.")

processes = []

if __name__ == "__main__":
    processes.append(Process(target=datalog))
    processes.append(Process(target=monitor_geophones))

    # spawn a subprocess
    for p in processes:
        p.start()
    for p in processes:
        p.join()
