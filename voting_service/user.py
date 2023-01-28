import os

import requests

from flask import Flask, request

from messages import make_response
import config

app = Flask(__name__)


@app.route('/', methods=["GET"])
def health_check():
    payload = {
        "message": "User device",
        "status": "success"
    }
    return make_response(payload, 200)