import os

import requests
import jwt

from flask import Flask, request

from messages import make_response
import config

otps = {}  # global dictionary to store OTPs generated
app = Flask(__name__)


@app.route('/', methods=["GET"])
def health_check():
    payload = {
        "message": "Voting process service",
        "status": "success"
    }
    return make_response(payload, 200)


@app.route('/request-ballot', methods=["GET"])
def request_ballot():
    # input id, # encrypted with system public key
    # output 
    '''
    get user info from database
    if user has voted send error
    if not get admin sign on ballot and send it to user
    '''
    # should get the secret here
    secret_key = "5bd44771b6531c12c8354aec3e27a8eeeba049cc0423c9208532eb96491c3335"

    # decode the JWT token
    decoded_token = jwt.decode(request.headers['Token'], secret_key, algorithms='HS256')
    

    payload = {
        "id": decoded_token['id']
    }
    user_voted_response = requests.post(f'http://{config.DB_HOST}:{config.DB_PORT}/user-voted', json=payload)

    if user_voted_response.json()['voted']:
        payload = {
            "message": "User has already voted."
        }
        return make_response(payload, 400)
    
    signed_ballot_response = requests.get(f'http://{config.DB_HOST}:{config.DB_PORT}/signed-ballot', json=payload)

    payload = {
        "ballot": signed_ballot_response.json()['ballot'],
        "public-key": signed_ballot_response.json()['public-key'],
        "status": "success"
    }
    
    return make_response(payload, 200)

@app.route('/request-otp', methods=["GET"])
def request_otp():
    # input 
    # output response "otp sent"
    '''
    generate otp
    get user mobile no from database and send generated otp
    save otp until voting is done
    '''


    id = request.args.get("id")
    payload = {
        "message": "Requesting ballot"+id,
        "status": "success"
    }
    return make_response(payload, 200)

if __name__ == "__main__":
    app.run(
        debug=config.DEBUG_MODE, host=config.MASTER_HOST, port=os.getenv('PORT', config.MASTER_PORT)
    )