import sysimport sys
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

API_KEY = "sc-d3bc30c7-a773-409c-875a-3cbd79afdcc1"
API_SECRET = "eyJkYXRhIjoidm92RnhjZEYxd2syWDhvNFJsaUZWWWR6VlV5REZJakw0dTR1WmZlTy1mUzhUakM4ekF2VHZUYlVxcWlUdkJYaXN4UGt1bHhXTmFnWkVMS3oyWFdEblpIVkdObnJqZlJOVVMxelpNd00yRFFKVTZjaUZPRW40MkFZVVBxa1lPSkJpNjJEcUhVVjU1TThUSlNMaDRvamxGT3Jwempnd0ZmUVZWWm5WcWRhS0R1a3RQRDRxZmM2MkxtZUtkVm9wc0RfU1BBTnJ0cW5xQk9oUWtUdWJmNFdWeUZIZFpSZ3lyTmtSRU1xeFhCdGliNF83T0s2anFlYzFOVFFFZ1UxSVQtMy1zVFpHeWx4Z1pESEtRb0lCMmRnOVBJYmpHLUpGRnplU1JFbnhkZENodXRqbnRGbzlKanNTdm9TelFlYVpWdGciLCJrZXkiOiJLakhORE1YaHc3VzJSd1VPTVVSMVZuMmI3cmZya1l5Y21ra1JMdm1TMC03VTk1SzA3Zkc3TEd4akt4LUIxOTFGell3czQwMERrV0NxZmZ5V1F1em9Hck1YWGV3MGRUSEFuaDZLdGRMS0V2ZDB0WVA3TFpLLTZzdWNVa2xVSkVYRTJxOTJoSmR0T2JiQmNKTDJlTTdwNWh3U01ockFBSW1sTjhFb0ZpOW9LcENWMHBXaXUyT0JvcTJHUTdFQmZDejVqT01UdkhMaEFwUjZCWjFNbm50aW5aLUo0eU40YWVFSWltZ2N1UzQwejl2b2R2cjRFbDhyTnBITzZsc09VRWN0YnR1WVZhQUFfT3dDQ0tUMV96TDMyYWFwNHd4WlZISWtBdTdGU0pkSlRsU0lrYW5IWHAtZEwwLTlnaHZHWFc5c2E2cWp6Qld4cXV6Ymx5eHp1RW1XUXc9PSJ9"

DEVICE_IP = "192.168.60.105"


def main():
    socket_serv = socket_server(ip=DEVICE_IP)
    socket_serv.start()


if __name__ == '__main__':
    main()
