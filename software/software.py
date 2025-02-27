"""Software Backend

The web backend for the software for our final project.
"""

import datetime
import threading

from flask import Flask
from flask import send_file
import requests

FIRMWARE_MOCK_ADDRESS = "http://localhost:8080"

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

@app.route("/")
def root():
  return send_file("index.html")

@app.route("/data")
def data():
  return {
    "times": time_stamps,
    "temperature": temp,
    "humidity": humidity,
    "ph": ph,
    "conductivity": conductivity
  }

@app.route("/pump")
def pump():
  req = requests.get(FIRMWARE_MOCK_ADDRESS + "/waterpump")
  return req.json()

if __name__ == "__main__":
  queryData()
  app.run(host="0.0.0.0", port=5000)

