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

API_KEY = "sc-80c9fedd-c1bf-4ba8-954a-2bececdbebef"
API_SECRET = "eyJkYXRhIjoiWW9NcDh5Q2hobkljd1ZrbDFhRW5qNDNrYk9MS1NSSkNjZVZtNFNSc3dtQWFxSnJydDRpVDY2THRqa0ljZ2FUWmpTTktvZTVlRHppeWJQbGFDd1NKUm9PbWFIR0dWdHpnLWtqRzFtZGZOcERKNDNpb0ppeTkydXNXNHA2VmxqMWVFTWZvOV9IRE91VXdEOXZYaHhBVUpYQXpGYnJKaEhQSlhhMXdnM0Q3el9aX010NjM5Vk5jdXViTnByUDQ1QTVhS2ZkX0hpQ0hCZUJqUmROdU9kU2k5bHFLZndUcWNONVFDMjQxTTJzekdKckpxVEI5VWZaODdfank5cUZXVkNaanctb3Y2YjdHcllCYnVDU1RFWXUxcUdpeDB1bUUxOUNCS202dXJhY196ejdBSGh3S3Z6a1VpNzNWZkVlSWxOOEkiLCJrZXkiOiJnTDBnSDkxeUNiYUtfRlJ2MkJPWkh3RUREemFiZlhsc0k1VHhvT0RSaHBVVGRzX181aUxvSFFIby0xN19pc3VEbktNUDZxSEI0U0xZc19BWmlLTm9VRzhvT1lCaW1JZG9rMF94alhfRldJNDlUY09oUTVPOWNhSlZVblE4bTZabE9LeDltc3BzY1ZwVmY5NlVfWUJDczBnWlIteDd2T0JIWV9HWUNONnBFUnZ0WENMazhPSHhsNjVza25GVFhUbmJYaEhQRVcwTVJvQzJmZWk5b09KbEVUdlZoVWxQZHQzeTZtS3VrV1FoS0syMHJrSzU4ZDNZSnVpZWRaS3kxMWV4THJkQW14clo3YVhMXzMteFBQOGpxWndJMjBjU1MzTFRsekViS20tcjFJb0dYaUl4SHNhZUlUMEt0RUhGdUd2YVo3NGtjOFdzMlZSRVBsd1JNQ0o0Zmc9PSJ9"

MQTT_CLIENT_ID = "GEOSCOPE_SENSOR_3"
MQTT_TOPIC = "geoscope/node1/203"
BROKER_IP = "192.168.60.10"
BROKER_PORT = 18884


def main():
    mqtt_client = mqtt_cli(ip=BROKER_IP, port=BROKER_PORT, id=MQTT_CLIENT_ID,
                           topic=MQTT_TOPIC)
    mqtt_client.start()


if __name__ == '__main__':
    main()