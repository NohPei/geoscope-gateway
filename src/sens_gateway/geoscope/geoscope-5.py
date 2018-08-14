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

API_KEY = "sc-8a872821-39bf-470a-9eec-6824467cccb3"
API_SECRET = "eyJkYXRhIjoiUnBHd3NFeF9Wa1Q1T0JWcmJYZDhibWJRbzFlWVhNVEpfVW5XVFZ5QS1BYUJFZTZQbmRLcGNzTWhPUG0zN2hZSFpSQ1Byd19nblNmb0E2aDduVWRzanhsX2tSenp2TW9ud1lpa2RFUTZ3bEd4U29RSE12bzhscUtFaU8wMHZ5MGtNQk1DaS1RMURkMlFGRm04X0U0a2FrVGZCTGNDdnVTZTBOaFdBT2oxOGJKZFcwZThZNGpua1p2MmpvYUNGajdCemNzY1libV81UHRIVDlTREVuSGVHWF9oS09jWHRGSXhvU24xOEhpdFY3OUJmbldJVTBJWmZCcnhYSVk2UXJUZGRndTUyY1dsOHhCMTZaSmZpOWs4VWZRQ0M5RlBlT01XOTVFX3Q5SGdSRGVDRGlRZktOSnYzRl9uZ0czdWNwQlIiLCJrZXkiOiJUNTZad0Rld0V2VTNVQUs5Y2VpU3B3VklOTmFueDc4QXNkeVJoQjUyUmdtNlJCSWJTa01iY1VyVFZGTXgyMFIyeVo5R1ZTUzR2ZzIwYnFhQjA1SlV4V2ZqYUhBX293emlteGgtY1BtN0NCMC11TmFmNGlmMHU2Wm1CcVphVGczMEhtUTUxQWE3a0lqUjZkYUpLY192UWFFZTk2TTZLMlZJU0Foa2ZZc29QWmgwMm5lZFhrNGhLMzd3Z3NCdC1DUlVab0NyQ0U0Vm91dzVtMFVLNWFYUUlzLXVfZ0R1dDQtZDBvSy1KaENUQW5USTdHMDdvVFB5cFVTRG5FY0dXdDFuYVFHZTFqNW1uTTMwTVkyQ0lOYW82WjJTSkJRc3FZQk5VNjRGTkZDTDRqX3E3NnV3eFptLUdjMkctMVpPcVZHNWxDcVMyaDBHQUdLdVNuT3d0TlctbVE9PSJ9"

MQTT_CLIENT_ID = "GEOSCOPE_GATEWAY5"
MQTT_TOPIC = "geoscope/node1/205"
BROKER_IP = "192.168.60.60"
BROKER_PORT = 18884


def main():
    mqtt_client = mqtt_cli(ip=BROKER_IP, port=BROKER_PORT, id=MQTT_CLIENT_ID,
                           topic=MQTT_TOPIC)
    mqtt_client.start()


if __name__ == '__main__':
    main()
