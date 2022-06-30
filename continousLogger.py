import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from collections import defaultdict
import os
import datetime
from pytz import timezone
import pytz
import queue


from_zone = pytz.timezone("UTC")
to_zone = pytz.timezone("US/Eastern")

class Datum:
    def __init__(self, timestamp, catagory, value):
        self.timestamp = timestamp
        self.catagory = catagory
        self.value = value
        self.process_value()

    def process_value(self):
        chars = ".0123456789"
        self.value = "".join([i for i in self.value if i in chars])

    def logable(self):
        return f"{self.timestamp},{self.catagory},{self.value}\n"

topics = ["Heardbeat","/temp/03","/temp/04","/temp/11"]
messages = queue.Queue()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for i in topics:
        client.subscribe(i)

def on_message(client, userdata, msg):
    #print(msg.topic, msg.payload)
    ts = time.time()
    topic = msg.topic
    info = str(msg.payload, 'utf-8')
    lv = Datum(ts, topic, info)
    messages.put(lv)

def log_message(filename="log.csv"):
    file = open(filename,'a+')
    msgs = 0
    while True:
        try:
            message = messages.get(block=False)
        except queue.Empty:
            break
        file.write(message.logable())
        msgs += 1
    file.close()
    print(f"Logged {msgs} lines")

server_address = "maxli.gay"
client = mqtt.Client()
#client.username_pw_set("maxli", password="mellon")
client.tls_set(ca_certs="/home/maxli/cacert.pem")
#client.tls_set(ca_certs="C:\\Users\\Maxli\\Documents\\cacert.pem")

client.on_connect = on_connect
client.on_message = on_message
client.connect(server_address, 8883)
client.loop_start()
scroll = 0

if __name__ == "__main__":
    while True:
        time.sleep(15)
        log_message()
