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

API_KEY = "sc-afdb65da-a8ac-4b37-b4ff-ab025578086b"
API_SECRET = "eyJkYXRhIjoiNWcySGxkeWNtT3RkZmlURGduZV85V1V6U1NqXzFJOHQyUU5rQkJPMEJKQXduTkZkcmhPcG83amlKRVdJRzZJVExkVE95S0huR1lEczB2UmRVNF9CbkFUdEwyWUE3M3d5NHVTeXhGU2JVQVlueDZIc1Y4RnRYYW1iU19UZ2RELWNTZFljOGNWQTRyV2plUERycWpHZkdaWHVHYlBlUjNkblNoSXZTdVJIeXFJc1YtNGZVMVdjUHRFdENZRnNRMUZKa0hNNlJzWl9MdkllTEtlQUZIZTZDUm9ic0FEYXZueHRFeGY5bE5TME5CSENBX01XMFRXM253dWswY2xuVTNCMThJYUlLaktYdEc0cFNFNDZ1VHIzWFNOWXlfOFJFQjkxUFZMYzNXOE5OYU5JMXV0OVUyNkU4Vjg3YTh1R1VXQ2oiLCJrZXkiOiJIZTdUS0FzcU1mTVBNd01pMnYteE8tVS10c3FFRHZYN1Z4QXFOdDBWSExLNGROaGpsSXZVYkczUkhrLVo2Uy1jNk9Sc3ZQS2x6MDlxYkwtazY3eS1UVFhHdkUxMXlzbG1FU3h0aElvRWhYM1BTVTg1LUt3WTFEelJud2ZxMElJOThvVmlDYzFGNmxTQmFDZldXT1VWQkJRRGdzUEdPQzJzTk1zSzlrNGRIMXptZkt5WGNBS09HMXAybFR5bkEwWFhuVWtrNHpjd1U0WkxybWM5enQ1R3JpWGlGdXhCNFUwWEloYUNXZFdsUmMxTGctekdaWjlWUkZ5T095aUk4dTNzeDJIQ2NDRmdsQml5VGJzRnVGMHZZbkY1UmJoaDhXMVFDVDRIZ0xfa2NSQ3BBU1h6VHd1WkdrLU8zVDZVR1BzMWVnaVpVWHRpdTJSYWJrREk2UVdQUWc9PSJ9"

MQTT_CLIENT_ID = "GEOSCOPE_SENSOR_102"
MQTT_TOPIC = "geoscope/node1/202"
BROKER_IP = "192.168.60.60"
BROKER_PORT = 18884


def main():
    mqtt_client = mqtt_cli(ip=BROKER_IP, port=BROKER_PORT, id=MQTT_CLIENT_ID,
                           topic=MQTT_TOPIC)
    mqtt_client.start()


if __name__ == '__main__':
    main()
