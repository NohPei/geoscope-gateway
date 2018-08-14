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

from socket_server import socket_server

API_KEY = "sc-c5a897d6-3d29-49cf-b0ef-e82b495ce864"
API_SECRET = "eyJkYXRhIjoibjJOZXAzZ08tQnFpOHRZc2pKS3VNeEp0RFA3SVVRVmpqSGM0M00zbi1QeVpOSGNzVGg5ZUtnRXhuRGRFQVdoYXZ3aUdaNVpqc3lmMkJwZnJzY3B5Vm9HYnJvbHRWcVFhaDB5cTFPVUZLUHYtejl6QlpYaTVlc19YZjAwdXdGVkdweWhXZU1ibnBFNlBrbmNQLVdpSi1yY1VNUHBYS2pFaW9LVzhjcUNxUXJaV28zdjlmV2ZDSkQ1NnV1aDRlb2tBbWhaT1c1aEYtYzRSMFZfSGtqVnlfRTl1dGFmXzg3NV9IWDFiazJTa1VoMWpuS0E0cTNzUU1FemJoWE1COTFSWGEyTVRoV3pRbFdZRF9lUkNZTzRKQTlwb3VQMlpUcEZVSEhPdVpkOWFqS1JVRDNsb2tuejhUX2FlaXJudDZ0Wk4iLCJrZXkiOiJMTW1GUnRHUE5EU1dzUkpTMTBJVHZqUGN4UzlfNldLYTc1amhxUzlhaXBqMHBaQk9ISWxHamF0cDNJZE13anZrUkpURUtHQVd0Ul9vODNQVXF4YmhDSDI1YXozN1RfQnE0RGdRdkJWejNxRlk0LU9WM3BRN21HY3JqaEhSLTZYNmlhdnBfek81bkF5Mk5jTEhSX05NeTBRT3NrcE5wREZ6U1dOUTNFOWp0R0pqVE16SGlkZWl6MWhJUVExby1kczhYNEZaZkVJZkpNQ0twdjg5ODFPdVBWclE5R01qRHJveTl4ZmotXzhxVG1PMEFqNnMyVlN3QzVteDRrZFJoNmctSkRpZ1JTU2RkS0VYd3RkTHdBSW8zem00WjRFeVAyNlJXZ09lMHpmWkdWTWdLczZFLS1GbFhJLXU4RVhSTmpsZ0dBNkp4R3M4QjJTX1lCUGZxX1loTmc9PSJ9"

DEVICE_IP = "192.168.60.130"


def main():
    socket_serv = socket_server(ip=DEVICE_IP)
    socket_serv.start()


if __name__ == '__main__':
    main()
