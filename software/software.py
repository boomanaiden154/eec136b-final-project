"""Software Backend

The web backend for the software for our final project.
"""

from flask import Flask
from flask import send_file

app = Flask(__name__)

@app.route("/")
def root():
  return send_file("index.html")

