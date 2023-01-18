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
def user_voted():
    id =request.get_json()['id']
    payload = {
        "voted": False,
        "status": "success"
    }
    return jsonify(payload), 200, {"Content-Type": "application/json"}

@app.route('/signed-ballot', methods=["GET"])
def get_signed_ballot():
    payload = {
        "ballot": "signed ballot object",
        "public-key": "public key",
        "status": "success"
    }
    return jsonify(payload), 200, {"Content-Type": "application/json"}

@app.route('/user-update', methods=["POST"])
def user_update():
    id =request.get_json()['id']
    payload = {
        "status": "success"
    }
    return jsonify(payload), 200, {"Content-Type": "application/json"}

@app.route('/vote-save', methods=["POST"])
def vote_save():
    encrypted_vote = request.get_json()['vote']
    payload = {
        "status": "success"
    }
    return jsonify(payload), 200, {"Content-Type": "application/json"}

if __name__ == "__main__":
    app.run(
        debug=False, host= '0.0.0.0', port=os.getenv('PORT', 8001)
    )