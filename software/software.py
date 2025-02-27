"""Software Backend

The web backend for the software for our final project.
"""

from flask import Flask
from flask import send_file

app = Flask(__name__)

@app.route("/")
def root():
  return send_file("index.html")

@app.route("/data")
def data():
  return {
    "times": [1,2,3],
    "temperature": [1,2,3],
    "humidity": [1,2,3],
    "ph": [1,2,3],
    "conductivity": [1,2,3]
  }
    
