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

API_KEY = "sc-de23b154-222e-42b1-b612-acc3c9fe6e30"
API_SECRET = "eyJkYXRhIjoidnJzUHhSbnp2RW82VGJESnpzV0E3XzQyXzNTX081dHlMRzhraUo3SWs3NDVUNUwxcmp4N0VoY0owaVJGUWt3ck5OMVhNeEJFT3gxdV83WU8zTW8zc3h6N0M5T2ZoTmctR1g5cW5RNDRGNHY0TmJid0l6bDRaWktmai16MnB6cDhjOE1Kd3AxeTRiX2R3cElRR0VPWkZqanpXRURWOGdfeG5QSk5GbGdlU3Y5SFl2TmNiaEp2Q09mM1cyMTVlcXJTZ0VUbHFNM1Bsb3hiRGNkRE9GS3p6QkdNZGZETmpXb2FxTHFnLUlEQUttYl9KZXk1bFJvUDlla0cwWDhqRmtGYkVXTnlDVldPdXJmOE9pU0F6bGg2UkZjQ21raVJPSGRxZVlDRV83VkctNFZIa3ZwMEgzdnlHQ3pBVVFtcE1fbkwiLCJrZXkiOiJBUmZWSjdWQmFaRk91Q0lkeU9Dd2lmTk9EaWp3Tmt6YWg1d1NxSXltdEktZE55V2FOd2daTDg2cDFlQzhyQUZFbEEyNWcwTm5jRDNrRTdnV0gzcjU0Q09WMnFYYTlPaFh3X0ZKMlFHdlhSUzhJQjh2bG5tVWYxcWo2U3d6cFE3Z0toRkN5ZVVIQ3IyUndPVVN6b1oySXd4VWpfcnZDV1hsSm1haWdxZ1R6OGhwakNwV1dneHd5RlN0Z18xUEJROHZhYUNTNE5nQ2VOTnVQRmV4bVdINXRaLV9YeDNlSHU4SWFxcFh3bVYyUDdhSk1JWk1MMlNWb0U5V09OX1VURDZfWFNjVmF2VGNTUFROYm10dUZHNlg5RXVwcUstU3ZPLWRlRVc2SnZGWndzUHpLUGgyeGtCT0lUNGx6N2RYOC1QSGFwMTJ4SXc1Umo4ODRRSnUxZU4wbmc9PSJ9"

DEVICE_IP = "192.168.60.122"


def main():
    socket_serv = socket_server(ip=DEVICE_IP)
    socket_serv.start()


if __name__ == '__main__':
    main()
