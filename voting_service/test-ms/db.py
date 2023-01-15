import os

from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/', methods=["GET"])
def health_check():
    payload = {
        "message": "DB service",
        "status": "success"
    }
    return jsonify(payload), 200, {"Content-Type": "application/json"}


@app.route('/user-voted', methods=["POST"])
def request_ballot():
    id =request.get_json()['id']
    payload = {
        "voted": True,
        "status": "success"
    }
    return jsonify(payload), 200, {"Content-Type": "application/json"}


if __name__ == "__main__":
    app.run(
        debug=False, host= '0.0.0.0', port=os.getenv('PORT', 8001)
    )