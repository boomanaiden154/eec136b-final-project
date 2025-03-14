"""Software Backend

The web backend for the software for our final project.
"""

import datetime
import threading

from flask import Flask
from flask import send_file
import requests

FIRMWARE_MOCK_ADDRESS = "http://192.168.1.106:80"

app = Flask(__name__)

time_stamps = []
ph = []
temp =[]
humidity = []
conductivity = []

def queryData():
  threading.Timer(10.0, queryData).start()

  time_stamps.append(str(datetime.datetime.now()))
  req_ph = requests.get(FIRMWARE_MOCK_ADDRESS + "/ph")
  ph.append(req_ph.json()['ph'])
  req_temp = requests.get(FIRMWARE_MOCK_ADDRESS + "/temp")
  temp.append(req_temp.json()['temperature'])
  humidity.append(req_temp.json()['humidity'])
  req_conductivity = requests.get(FIRMWARE_MOCK_ADDRESS + "/do")
  conductivity.append(req_conductivity.json()['do'])

@app.route("/leds")
def toggleLEDs():
  led_1 = requests.get(FIRMWARE_MOCK_ADDRESS + "/led?led=1")
  led_2 = requests.get(FIRMWARE_MOCK_ADDRESS + "/led?led=2")
  return [led_1.json(), led_2.json()]

@app.route("/")
def root():
  return send_file("index.html")

@app.route("/data")
def data():
  return {
    "times": time_stamps[-20:],
    "temperature": temp[-20:],
    "humidity": humidity[-20:],
    "ph": ph[-20:],
    "conductivity": conductivity[-20:]
  }

@app.route("/pump")
def pump():
  req = requests.get(FIRMWARE_MOCK_ADDRESS + "/waterpump")
  return req.json()

if __name__ == "__main__":
  queryData()
  app.run(host="0.0.0.0", port=5000)

