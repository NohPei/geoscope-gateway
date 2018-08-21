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

API_KEY = "sc-35c22783-e35e-453c-b16c-b01886308640"
API_SECRET = "eyJkYXRhIjoiSVVnVHRveWlhOE90WDNVSlNTaGd1Z2FQaXo2ZmM3X0REQjM0bEc1WkRnV0t2MlNPY0pNQ2pHZ0tTYzZDSXlxTE9xXzRBcmRoM0drSUFoQnF2TF9lRTZYNVJxSV9DelZaVWppWklIZ3NpcVVqWUZmOGQ5ZjFoQ19yX216WlFyRUNXSHBqeXR4ZnR2a0VldDZxQ09IYnlIUVV6QXpteHJwMi1aQi11X0hiMmxhVDg2VlhDSmZ1dVc0OHJ1cEczNEpfbEd0Y0MxMmhXYlVNSVlQaXpFUEpqZk40bm9ENzN3R3pueWhjNVZBNVllMlZLRGtfYWNjVXgtLXcwTnI1UzcyLUhfNzhyNHNMVmtqT3NUcWdYZG16cDJaNVQta3Z1MWxHR2pKYUZEYTN0dE1ZV1dKMDRIYTlJWmcya1BHNWVLRm4iLCJrZXkiOiJQd0Nyb0RlYnBYRlNXay1kdzBiTFJCQzV4SWE0RUFjN29SWDQwNHZTSmxIQXhLb1J2WmhuQlNxbFdicURwa212SjV5TkRia08yRm44VmprdXhUYzdwNVBfVkNFTW1leUhkUHFWeXUycm5XLTFkaDNQYU42cVJZUHRLM3ROSnZLMjFubFcxUVlpM2J4TzlXYXZpT0tXeUp4MHFWZVVzWUtwM3JrejY1dXkwS3Bpa3J6MTc4Nl9VcmRkVTNBN3RGR21uRXllUy1mNEgzLTJZUjhVZ3RNWnBqSnlJR3lmZFBRMzA4cTByY2IyeFNuVTllaDdpcjBsS1BlR2xHWVBucVhYdTd6bmc1TkJOQlV0ZllJZGh4cHNBSjBwRlpYcG82YlR2ZlRNTlh4cnFlNW9JSm9vaWZIT2JydkptcUxKQ0Z3OEVRUHNWTXZ3ck9hM2VNMXNaQUxQalE9PSJ9"

MQTT_CLIENT_ID = "GEOSCOPE_SENSOR_1"
MQTT_TOPIC = "geoscope/node1/201"
BROKER_IP = "192.168.60.60"
BROKER_PORT = 18884


def main():
    mqtt_client = mqtt_cli(ip=BROKER_IP, port=BROKER_PORT, id=MQTT_CLIENT_ID,
                           topic=MQTT_TOPIC)
    mqtt_client.start()


if __name__ == '__main__':
    main()
