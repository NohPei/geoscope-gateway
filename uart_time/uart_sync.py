from datetime import datetime
import serial
import sliplib

def serialMicrosLoop(port='/dev/ttyUSB0', baudrate=256000, repeat_sec=1, **kwargs):
    out = serial.Serial(port, baudrate, **kwargs)
    try:
        while True:
            time = int(datetime.now().timestamp()*1e6)
            out.write(sliplib.encode(f'{time:x}'.encode()))
            datetime.time.sleep(repeat_sec)
    finally:
        out.close()

