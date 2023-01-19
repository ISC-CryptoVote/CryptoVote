import os

from flask import Flask, request, jsonify
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

# dummy keys for ballet signing
private_key = RSA.generate(2048)
public_key = private_key.publickey()

private_key_pem = private_key.export_key()
public_key_pem = public_key.export_key()

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
    data = "ballot object"
    private_key = RSA.import_key(private_key_pem)
    signature = 'sasasa'# pkcs1_15.new(private_key).sign(data.encode())
    payload = {
        "ballot": data, 
        "signature": signature,
        "public-key": public_key_pem.decode(),
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