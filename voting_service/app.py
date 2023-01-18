import os

import requests
import jwt

from flask import Flask, request

from messages import make_response
import aes
import config

otps = {}  # global dictionary to store OTPs generated
app = Flask(__name__)
# should get the secret here
secret_key = "5bd44771b6531c12c8354aec3e27a8eeeba049cc0423c9208532eb96491c3335"

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
    # decode the JWT token
    decoded_token = jwt.decode(request.headers['Token'], secret_key, algorithms='HS256')

    # Genarate OTP for user
    otp = 73967897100972511069414005 #aes.get_otp() #int
    print('otp gennerated',otp)
    otps[decoded_token['id']] = otp
    print('otp saved')
    payload = {
        "otp" : otp,
    }
    return make_response(payload, 200)

@app.route('/submit-ballot', methods=["POST"])
def submit_ballot():
    # decode the JWT token
    decoded_token = jwt.decode(request.headers['Token'], secret_key, algorithms='HS256')    

    # Extract encrypted ballot
    ciphertext = request.get_json()["ciphertext"]
    nonce = request.get_json()["nonce"]
    cmac_received = request.get_json()["cmac"]
    print(ciphertext,nonce,cmac_received)

    # Decryption
    key = int(decoded_token['id']).to_bytes(5,'big') + otps[decoded_token['id']].to_bytes(11,'big')
    decrypted_ballot = aes.decrypt(key,ciphertext,nonce)
    cmac_generated = aes.cmac(key,ciphertext)
    print("decrypted:", decrypted_ballot)
    print("generated cmac:",cmac_generated)

    # CMAC verification
    if cmac_generated != cmac_received:
        print("CMAC verified")
        payload = {
            "message": "Sign verification failed"
        }
        return make_response(payload, 400)

    # Update db that the user has voted
    payload = {
        "id": decoded_token['id']
    }
    user_db_updated = requests.post(f'http://{config.DB_HOST}:{config.DB_PORT}/user-update', json=payload)
    print("user db updated",user_db_updated.status_code)

    # Homomorphic encryption, Save vote
    encrypted = 'blabla' #homomorphic.encrypt(decrypted_ballot)
    payload = {
        "vote": encrypted
    }
    vote_saved = requests.post(f'http://{config.DB_HOST}:{config.DB_PORT}/vote-save', json=payload)
    print("vote saved",vote_saved.status_code)
    
    # Response
    if (user_db_updated.status_code == 200) and (vote_saved.status_code == 200):
        del otps[decoded_token['id']]
        payload = {
            "message": "Vote successful"
        }
        return make_response(payload, 200)
    payload = {
            "message": "Vote failed"
        }
    return make_response(payload, 400)

if __name__ == "__main__":
    app.run(
        debug=config.DEBUG_MODE, host=config.MASTER_HOST, port=os.getenv('PORT', config.MASTER_PORT)
    )