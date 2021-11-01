import logging
import logging.handlers
import time
from multiprocessing import Process
from mqtt_cli import mqtt_cli
from monitoring import monitor_geophones


## Logging

logger = logging.getLogger("GEOSCOPE")
logger.setLevel(logging.INFO)
file_log_handler = logging.handlers.TimedRotatingFileHandler(
    f"/mnt/hdd/PigNet/log/GEOSCOPE-{time.strftime('%Y-%m-%d')}.log",
    when='midnight', delay=True)
file_log_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s:%(name)s %(message)s", datefmt="%Y/%m/%d %I:%M:%S %p"
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
    sublog = logging.getLogger("GEOSCOPE.Subscriber")

    sublog.info("## Starting data logging program")
    mqtt_client = mqtt_cli(id_list=client_id_list, logger_name=sublog.name)
    mqtt_client.start()
    sublog.info("## End data capture.")

if __name__ == "__main__":
    logger.info("## Starting full capture system")
    monitor = Process(target=monitor_geophones)
    monitor.start()
    datalog()
    monitor.join()
