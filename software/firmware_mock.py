"""Mock of the firmware.

This file implements a web server that mocks the firmware by returning
semi-random reasonable data and holding the relevant state. This is intended
for use when hacking on the software.
"""

import random

from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
  return "testing"

@app.route("/temp")
def temp():
  temp = random.gauss(70, 10)
  humidity = random.gauss(30, 5)
  return {
    "temperature": temp,
    "humidity": humidity
  }

@app.route("/ph")
def ph():
  ph = random.gauss(7, 0.5)
  return {
    "ph": ph
  }

@app.route("/do")
def do():
  do = random.gauss(1000,100)
  return {
    "do": do
  }

water_pump_state = False

@app.route("/waterpump")
def water_pump():
  global water_pump_state
  previous_state = water_pump_state
  water_pump_state = not water_pump_state
  return {
    "previous_state": "on" if previous_state else "off",
    "new_state": "on" if water_pump_state else "off"
  }

