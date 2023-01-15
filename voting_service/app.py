import os

import requests

from flask import Flask, request

from messages import make_response
import config

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

    sector = request.get_json()['sector']
    payload = {
        "sector": sector
    }
    response = requests.post(f'http://{config.PD_HOST}:{config.PD_PORT}/predict_disease', json=payload)
    
    return make_response(response.json())
    '''
    payload = {
        "id": request.headers['Token']
    }
    print(payload["id"])
    response = requests.post(f'http://{config.DB_HOST}:{config.DB_PORT}/user-voted', json=payload)

    
    if response.json()['voted']:
        payload = {
            "message": "User has already voted."
        }
        return make_response(payload, 400)
    
    payload = {
        "message": response.json(),
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