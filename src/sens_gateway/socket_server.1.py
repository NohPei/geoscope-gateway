import sys
import websocket
from threading import Thread
import time
from datas import data_collection


class socket_server:
    SENSOR_WS_ENPOINT = "ws://ENDPOINT"

    API_KEY = "KEY"
    API_SECRET = "SECRET"

    START_TIME = time.time()
    counter = 0
    data_counter = 0
    payloads = []
    payload = {}
    payload["uuid"] = ""
    payload["lat"] = 13.727277
    payload["lng"] = 100.777404

    is_first_time = False
    START_TIME = time.time()

    def __init__(self, ip="192.168.60.1", key="KEY", secret="SECRET"):
        self.SENSOR_WS_ENPOINT = f'ws://{ip}:81/geophone'
        self.API_KEY = key
        self.API_SECRET = secret

    def convert_data(self, data_array):
        data_converted = '['
        leng = int(len(data_array) / 2) - 1
        for i in range(0, leng):
            data_int = int.from_bytes(
                data_array[i * 2:i * 2 + 2], byteorder='little', signed=False)
            data_converted = data_converted + str(data_int) + ","
        data_int = int.from_bytes(
            data_array[len(data_array) - 2:len(data_array)], byteorder='little', signed=False)
        data_converted = data_converted + str(data_int) + ']'
        return data_converted

    def async_send(self, payloads):
        dc = data_collection()
        dc.setKey(self.API_KEY)
        dc.setEndpoint(self.API_ENDPOINT)
        dc.send(payloads)

    def on_message(self, ws, message):
        if self.data_counter == 10:
            self.data_counter = 1
            t = Thread(target=self.async_send, args=[self.payloads])
            t.daemon = True
            t.start()
            self.payloads.clear()
        else:
            self.data_counter = self.data_counter + 1

        ts = int(round(time.time() * 1000))
        if not self.is_first_time:
            print(f"> GEOSCOPE UUID: {message}")
            self.payload["uuid"] = message
            self.is_first_time = True
        else:
            self.counter = self.counter + 1
            tstr = time.strftime('%Y-%m-%d %H:%M:%S')
            print(
                f'> On message Timestamp:{tstr}\tCounter:{self.counter}\tUptime: {time.time()-self.START_TIME}')
            data_bytes = bytes(message)
            self.payload["data"] = self.convert_data(data_bytes)
            self.payload["ts"] = ts
            self.payload["timestamp"] = ts
            self.payloads.append(self.payload)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        self.is_first_time = False
        print("## WebSocket Closed.")

    def start(self):
        ws = websocket.WebSocketApp(self.SENSOR_WS_ENPOINT,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        websocket.setdefaulttimeout = 5
        while(True):
            try:
                print("------------------------------------------------------")
                print("## Starting Socket Sever service...")
                print(f"## Socket Device: {self.SENSOR_WS_ENPOINT}")
                print("------------------------------------------------------")
                ws.run_forever()
            except Exception as e:
                print("> Somethins went wrong!!!")
                print("> Restart socket...")
                print("------------------------------------------------------")
            except KeyboardInterrupt:
                print("------------------------------------------------------")
                print("## Exit program...")
                sys.exit(0)


def main():
    device_ip = "192.168.60.130"
    API_KEY = "sc-739aeac3-b37e-4c57-aaa7-119e400637d8"
    API_SECRET = "eyJkYXRhIjoiOXp5VnFpWFNpOEc0YnBXNWxlRXJWeGlCUk81TG50cVBLU0pOOEh6WmM4cWxYbnQ0SlJGSHRzTm9VUEhmUnN4WWZNYXBpUG96QmNDUTlPQXFJRHVjLXRiTFFwNGx1VVYwRl94UGE3QnUtVVJCS0dXbVdKSVg4OWkzWmNYUjY3elFyVFZOZHBYZENzektPT05RaGJCbW5HY3lydUV0dFEtOUlxcUVrTEhLbGlDMUlRcGRmMUFiR1lvX2hkMGY1VnFsbmRaMmd3dG81YWVTYTRqQXdzZDhRZUtETnp6V1RFTkh4aFdLM05mMnAtamdyLXgxUlBFWVdkb0tWV0EwRDIwZUZJVmhYLVZZZnJUUGtBT3NER1hfamJaQ094enlodE5CZFUzMG94WjZRUHVBcVVMOE1RaXQwT2VJdXlTNmktX0QiLCJrZXkiOiJKam9zYjVuSTU3OHlSdGljMlN5R3VZYUdPZWJjbUxSTXlNcmxvN2R4UWQ3QnFBaU9wdldSTXhDOHA0ZG5DaXg1TDdnc05GSUNQSF9CMXdKZFRZTldnQWFkckdxbkIyQXVoUG0zS2FtTzRRT0t2NHNXbURZMm5oalJZekZ2bEVsbmhOeVRUOVlQOUk0eDZVLVVDNXh1WF9nZ1FSN3cwVnRuM2JaVlRZTUs3bUxDQlY2LUpRR3RUa0dKQy1aYTRTdGdHVGU5UGZwUVY2Uld1c250TklsUVpNTnp4VFI5Y2xQcTc1RGFKTVg2ZHhkblczSG4yRDZKYy1KM0NONkU5UElZV0RSRDdXQk4ycVlaVjF4cl9Ub2RfcVVpT0xPSHl0X2gyRVE5ckR5aGxZd0lFVHFLa0I4QW5GLUhGYTFoSzZ3MVdvYXBZTk5HMTVFS056NjhaR2NmX2c9PSJ9"
    test_socket = socket_server(ip=device_ip, key=API_KEY, secret=API_SECRET)
    test_socket.start()


if __name__ == '__main__':
    main()
