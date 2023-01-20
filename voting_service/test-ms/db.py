import os

from flask import Flask, request, jsonify
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from phe import paillier
import pickle
import codecs 

# dummy keys for ballet signing
private_key = RSA.generate(2048)
public_key = private_key.publickey()

private_key_pem = private_key.export_key()
public_key_pem = public_key.export_key()

# user public key
user_public_key = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDF4hI9s0Mem349YzSu3r+ZvuQl\nx7Zmr2LNWXaeeR+m8xbnX9cqIeeFCRdxBfXNzoYgexbnG2hW+1JFbg4OQiFpoLi9\nKJEoyRYZR8dgzrUUFgm0DjpHreiuu/Cr0GvkzBscV0LwBHCoUUJlGLWW6vMQmwGH\nBRV8/tsRtQVy0yB4ZQIDAQAB\n-----END PUBLIC KEY-----'
app = Flask(__name__)


@app.route('/', methods=["GET"])
def health_check():
    payload = {
        "message": "DB service",
        "status": "success"
    }
    return jsonify(payload), 200, {"Content-Type": "application/json"}


@app.route('/user-public-key', methods=["POST"])
def get_user_public_key():
    id =request.get_json()['id']
    payload = {
        "public-key": user_public_key,
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
    hashed_data = SHA256.new(data.encode())
    signature = pkcs1_15.new(private_key).sign(hashed_data)
    payload = {
        "ballot": data, 
        "signature": signature.hex(),
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

# Simulate retriving the homomorphic priavte and public keys from DB

@app.route('/homomorphic-keys', methods=["GET"])
def get_public_key():
    public_key, private_key = paillier.generate_paillier_keypair()
    bytes_key = pickle.dumps(public_key)
    str_public_key = codecs.encode(bytes_key,"base64").decode()
    payload = {
        "public": str_public_key,
        "status": "success"
    }
    return jsonify(payload), 200, {"Content-Type": "application/json"}

if __name__ == "__main__":
    app.run(
        debug=False, host= '0.0.0.0', port=os.getenv('PORT', 8001)
    )