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

API_KEY = "sc-ea61d0b6-c66e-40d8-9371-81271f6907cb"
API_SECRET = "eyJkYXRhIjoiSzQ1d3h2Q0hQTy15T0o3MVBQR2tUbmJmQlR4TkNyLTdmblRPOUszQkQ4bjR3dXpPVVhjbDNFWFhod0wzb2RjS3BlYjBHV29MNXZQaXJrMUZQbUN0R0tURUlBLVdNWjdrWHVVNXRrT2VyUktBTFdQNFczekJwX1BKa3BHWm1ZT0c0X3hiNElDcnM4VWVnWjJoU0pYYWtHV3lIV0V4My1ndGJuSGItcHJUNU5pazh0SUlpSUp5WUVsbkU0V29EV3FZdndrUXdiSGNFYlJBbnJ5VXI0LWtNZ05ZS2pDRVliS1BSZ2o2aF9rS3NLMlhPcGlDaW03QlNLRGVQWjJUX1RFY1IzVHFSMGlNZGk0al9VS1d2akR2cF9INERuWFZxY1lEaWtXYzdxcGlsNW12eVJlVlRid2xGTjVMQTRJQms3OW4iLCJrZXkiOiJEa0xpeS0yYVA1cDdlSmVveXFVNTZIN05weVNDWkNCeFNjQUtWN0JXSTRqLUVpSGt1V1V3TjhCS3piUUpueUlva3NrYjdjdlZPU0hrWFFIN2huN3hDNWhRU0tjQi1VX1B4TkItek9kdVNRU3BmRUVZRy11UUIwMmlrU0VQcmJONmlaZWpqTGgtV3dlQ05DWl95S29BQUJMOHcyVVByUGRESGJLU3VRay15WUdDbGxlNndtMVJoX3o0dVFvTTUzUTdKZ19WQmJoOUNMUjhwSkw1T0EzeUk1NV9La2g4MlZob1VtMWNtMmZVTFhsMEllN3N1bmNpdkpUN1A0dExFTnZ3cEtZcjZvSmlZcW9QU0xhb2l4dnEyZExKZGZ0SHY0Q282ZGM5WkxIT096MW5aZ3JOYVg3Yk1xM1lxSG1JSFdtVUJHdUdQWDgzZ1NzNXBVbklLY2I4YXc9PSJ9"

DEVICE_IP = "192.168.60.133"


def main():
    socket_serv = socket_server(ip=DEVICE_IP)
    socket_serv.start()


if __name__ == '__main__':
    main()
