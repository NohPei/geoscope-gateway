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

from mqtt_cli import mqtt_cli

API_KEY = "sc-7e52dd11-150e-4243-bfa9-e4da91ea0776"
API_SECRET = "eyJkYXRhIjoiWVRDeWtFZi1kRDRqVlM5MnRXTTZRTlNQZTNIQXB2aDZVMkY3TzJrRUc2cDVhZHJXWjNGVHNobDNBRUVwRGUwNkVZNzFKYk1RZVM0SUwyREhXUWktVUlUWHBsSUdNQkJVcGVOSU9WVWsxSmtqS2ZNRndDVm1jUTlSYTFhMXFwMndNS1diY21tcjY5aEdDUnNMV1Rodkdkd2lINDF0N3dmZDJhdnBkZWFZeklSWU5BbnhxYWhaSlRvWTRfQzBhMUxVWWVrdndHRmhCUUFlTVZUck90R2h0aVNkOUhCNGFxc0lfM0ZRV1g0TGtTUXk3b1FKZ0otRUhVWVNBUjlma2lKS0VPSVVrZXh6YmM3NC1LU296VEh6T0duTWY2bjl5VzdMRGpxZDFZS3dfT3FTblUyQU16SWVReExTRnczZUxadnMiLCJrZXkiOiJBd1lFWkNUejRLaXdHeWNrd2JyT0x2Ymw3N3BWSkFfRjhTMVBVeUVaQV9nUG5lb25oOXVGZ2k3Mi1VWDdsS0UydGFuc0xRaC1Td3REM01uSkdpTFFtOFFRRVhSVmFuSjNLSUExLWtUZGlRR1NyTE1jTWZvRld1S1Axd0pDQ0YyZFhrTEh1UzVKMl9FUDd4ZzFXaEpOTjdmYlFFNURHV1F5eGRmMGdlc2tLOTJ2Z3pjeTg0TVUwczNiWDBnWWMyTk1lMmhWN282UWRxbFpKcFZjSGtUa3FxbFFQbEcxS3NzRVY5MnZFOVVMTTVMamJmWkpwQU4zMUpocVRReWxrTlFJSHVpbnNkdUFxNmo0eWFuRExraGdveTJKRTRJem52a3NpX2FUWVZkOGVUN0JnSW9JdFJNZnR2R0FRNXhaSWc5Z3dhSzNQZ1JjUkFiSXJRam9KT1NiV3c9PSJ9"

MQTT_CLIENT_ID = "GEOSCOPE_SENSOR_4"
MQTT_TOPIC = "geoscope/node1/204"
BROKER_IP = "192.168.60.10"
BROKER_PORT = 18884


def main():
    mqtt_client = mqtt_cli(ip=BROKER_IP, port=BROKER_PORT, id=MQTT_CLIENT_ID,
                           topic=MQTT_TOPIC)
    mqtt_client.start()


if __name__ == '__main__':
    main()