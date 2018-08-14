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

API_KEY = "sc-bd99486e-57c9-44ab-ae5f-80dccab22032"
API_SECRET = "eyJkYXRhIjoiQ0JWam5RN0h3aTJFWUwyYl9VSENWSktLcHkwaGRIVk9Ram5pVFRDOWtlczZSbVlORmJEQUM2QUVEOEt0YnVDT2NJeTlNMWJuSUstbHE4TVd3d1hmbE5OOUY1WDJyQWNuNUxJb2c1bWZUSkpvR3BmcEZqNmZndmVGVnB4TVl2MlNBMndnenRVNUZMa3lfczNLUUNlTkdiRElBZlZaNXo2Ylc4M3V4UllvNk0yLWNzaTJSdkoteFAwX25KTE1FLThLMWowTG5CNlJadURXbWR2ZjROTk5NS201MkFueHNfODB3YUpUQXJ1dkpUWEd1a3NIaERzZjItSklJekNzU0dNUWgwemE2ekVla1ZDUmsySF83OEtEcjFzdm5PeXhnSnlfMUs3bmo4QU9qZlUwMzQzUXBjUVE3LVFyRE5naWFUdjEiLCJrZXkiOiJHT2t3UkNtVnBfRXlleG42MVhkbFh2YkJQbWFjeFJXSTI2TjFKcDQ4U0xxb3d2cnVEaXFDYUhhcFAwWDFOU1Fta3Y0WWQ5aTlmdUcyM05mbDExbmdqek1BR0FOdkdMS0ZaUXRlRklQU1VaV0RKNDRRaUZEa3d3cVFsNURhS3NFTVpwVXVtc2RGU2lDLW82WUR3SXdmREtWQzJCeE5aNzRNZlNkMWQxZ1VOMGZ2RWlPcmk2Y3gzbExwUXdlZS1DS2llOFBQdzE2ZWI4UVNPaUktVkxZYlR1d1NvUGhCQnkyc2F5RFBzS25FRmkwWm9VLUUxM08xMzV2MGE5aFl4TWc1Uk1RY0lnVVdYakxpQ0ZEOFNOdEZlSFhtUzBSVnZsVmNMTkoxMmtfeUZvVVNnUm10LThrckt1Rm5PWXVZOTJ1SHpfYW43NWQ4NVliZHEtTmJjWnZiQ2c9PSJ9"

DEVICE_IP = "192.168.60.132"


def main():
    socket_serv = socket_server(ip=DEVICE_IP)
    socket_serv.start()


if __name__ == '__main__':
    main()
