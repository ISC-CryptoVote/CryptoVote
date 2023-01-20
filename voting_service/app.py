import os
import requests
import jwt
from flask import Flask, request
from messages import make_response
import aes
import config
import paillier_encryption
from phe import paillier
import codecs 
import pickle

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
        "signature": signed_ballot_response.json()['signature'],
        "public-key": signed_ballot_response.json()['public-key'],
        "status": "success"
    }
    
    return make_response(payload, 200)

@app.route('/request-otp', methods=["GET"])
def request_otp():
    # decode the JWT token
    decoded_token = jwt.decode(request.headers['Token'], secret_key, algorithms='HS256')

    # Genarate OTP for user
    otp = aes.get_otp() #int
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

    # Here decrypted ballot assumed to be a string eg: 00100
    vote_lst = list(decrypted_ballot)
    # Homomorphic encryption, Save vote
    homomorphic_payload = requests.get(f'http://{config.DB_HOST}:{config.DB_PORT}/homomorphic-keys', json=payload)
    status = homomorphic_payload.json()['saved']
    # public key and save in db
    str_bytes_public_key = homomorphic_payload.json()['public'] # used to homomorphically encrypt the voting list 
    public_key = pickle.loads(codecs.decode(str_bytes_public_key.encode(),"base64"))

    encrypted = paillier_encryption.encrypt_vote_array(public_key,vote_lst)
    encrypted_votes = pickle.dumps(encrypted)
    str_encrpypted_votes = codecs.encode(encrypted_votes,"base64").decode()
    # encrypted = 'blabla' #homomorphic.encrypt(decrypted_ballot)
    # str_encrypted_votes = codecs.encode(str_encrpypted_votes,"base64").decode()
    payload = {
        "vote": str_encrpypted_votes
    }
    print(str_encrpypted_votes)
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