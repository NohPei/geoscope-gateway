import sys
import paho.mqtt.client as mqtt
import time
import json
from put_data import datas
from threading import Thread
import matplotlib.pyplot as pyplot

API_ENDPOINT = "https://api.smartcity.kmitl.io/api/v1/collections/sc-739aeac3-b37e-4c57-aaa7-119e400637d8"
API_KEY = "eyJkYXRhIjoiOUVIT25kVFpvRVEtVzRDcDFLc2tKejlzdFFqZnNvTm9Lb3FRaEZLcDVLUy12bldXeGpBcXd0eW5qNWJydTV2TWJFYmYyYllWM1p2eFdzQmhabU1HTm9ILW1QanAzbzRVLTBOX28waDBTWTNQVnJmNlZRdjhWRkd5d1p4VGliMlpwai1qY1dDUEdtZXlsWTEtYl8wQVJ4SFJsbWNyczVPRUM2Qko0dmk3eExBQXNlUGIzYlhzX25hRFNJZXJMOV80N0ItclRQUV9YbElyUWhfUlZWVzFWWGlTOEw0WTBoRXluWW90aFVfdHRqMGZBMEhvbHNZeXhuNnZuR3ZHdVRXaFRkVjdLQ3RwZy1NMzBYYWRkTFZMc2ppd011UXIyY2xJMEZXTl9zWG9ZUlJxemlvcks2MjlRSTJ1ellRd08tSVMiLCJrZXkiOiJMd0p1R2tMXzZfb1E0VXpxLUpZbGd5bW15d1RDUzBXbG56TzdPVTV0MU01aGN1cUFoUkdBTXYwSXlLcFgtQkM4M2VLcXhEdlFEQ1hISzhST0l5QTlQVWdHNGZmSjFpWXhRcl8xRWl2YWZxQkpNa2Nob09HRDFCOFotQjJoU0JYNFJaY2d0ZXZpdXo2TmxEUEJKdzlsVmFRdnZ2TmgxeklFSzBKSWRoN3h4c0RPRHdTd3lQb2NYWG5oY0ZtbXFQTzNYRy1VdldsS196RW1YenZoQWluczhwbmlPMnNYMkFDbkQtUUQ2YUxPQTlwT2NfT0lkVXM4RkNpZHFsQjF1eTMwam5IT0xfbC1YRnIxZDdVWFV2cmh6WS12TVRhQVUtZ0paRS1IaG9XYktzSXFTdFRlVDVsbDRhc09pYi1wVXNfLXdaakRmc1FVNmpncThDWnpBWW40Q1E9PSJ9"


BROKER_IP = "192.168.60.60"
BROKER_PORT = 18884

tim = time.time()
tim2 = 0
counter = 0
data = []

payload = []
data_counter = 0

x = []

for index in range(0, 501):
    x.append(index)

fig = pyplot.gcf()
fig.show()
fig.canvas.draw()


def convert_data(data_array):
    data_integer = []
    leng = int(len(data_array) / 2)
    for i in range(0, leng):
        data_integer.append(int.from_bytes(
            data_array[i * 2:i * 2 + 2], byteorder='little', signed=False))
    return data_integer


def async_send(payload):
    data_collection = datas()
    data_collection.setKey(API_KEY)
    data_collection.setEndpoint(API_ENDPOINT)
    data_collection.send(payload)


def on_message(client, userdata, message):
    # print("message received: ", str(message.payload.decode("utf-8")))
    # print("message topic=", message.topic)
    global counter
    global tim
    global tim2
    global data

    counter = counter + 1
    tim2 = time.time() - tim + tim2
    ttopic = message.topic
    tmp_data_array = json.loads(str(message.payload.decode("utf-8")))
    tmp_data_array['ts'] = time.time()
    data = json.loads(tmp_data_array['data'])
    print("On message timestamp:{:.3f}\ttopic:{}\tcouter:{}\t| {:.3f}".format(
        time.time(), ttopic, counter, tim2))
    tim = time.time()


def mqtt_cli():
    mqtt_client = mqtt.Client("GEOSCOPE_GATEWAY101")
    mqtt_client.on_message = on_message
    mqtt_client.connect(host=BROKER_IP, port=BROKER_PORT)
    mqtt_client.subscribe("geoscope/node1/201", 0)
    mqtt_client.loop_forever()


def main():
    t = Thread(target=mqtt_cli)
    try:
        t.start()
        # startT = time.time()
        print("test")

        time.sleep(2)
        while(True):
            pyplot.plot(x, data)
            pyplot.ylim([0, 4200])
            fig.canvas.draw()
            pyplot.pause(0.1)
            fig.clear()
            #     if time.time() - startT > 1:
            #         startT = time.time()
            #         print(counter)
    except KeyboardInterrupt:
        t._stop()
        sys.exit(0)


if __name__ == '__main__':
    main()
