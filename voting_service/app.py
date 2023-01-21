import os
import requests
from flask import Flask, request
from messages import make_response
import aes
import config
import paillier_encryption
from phe import paillier
import codecs 
import pickle

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

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
    '''
    get user info from database
    if user has voted send error
    if not get admin sign on ballot and send it to user
    '''
    print('Ballot request received')
    # get nic and validate
    id = request.headers['id']
    nic_signature = request.headers['sign']
    payload = {
        "id": id
    }
    user_public_key = requests.post(f'http://{config.DB_HOST}:{config.DB_PORT}/user-public-key', json=payload).json()['public-key']

    public_key = RSA.import_key(user_public_key.encode())
    hashed_nic = SHA256.new(id.encode())
    try:
        pkcs1_15.new(public_key).verify(hashed_nic, bytes.fromhex(nic_signature))
    except (ValueError, TypeError):
        return make_response(payload, 401)
    print('NIC verified')
    user_voted_response = requests.post(f'http://{config.DB_HOST}:{config.DB_PORT}/user-voted', json=payload)
    print('User vote status checked')
    if user_voted_response.json()['voted']:
        print('User has already voted')
        payload = {
            "message": "User has already voted."
        }
        return make_response(payload, 400)
    
    signed_ballot_response = requests.get(f'http://{config.DB_HOST}:{config.DB_PORT}/signed-ballot', json=payload)
    print('Signed ballot requested from admin')
    payload = {
        "ballot": signed_ballot_response.json()['ballot'],
        "signature": signed_ballot_response.json()['signature'],
        "public-key": signed_ballot_response.json()['public-key'],
        "status": "success"
    }
    print('Signed ballot sent to user')
    return make_response(payload, 200)

@app.route('/request-otp', methods=["GET"])
def request_otp():
    print('OTP request received')
    # get nic and validate
    id = request.headers['id']
    nic_signature = request.headers['sign']
    payload = {
        "id": id
    }
    user_public_key = requests.post(f'http://{config.DB_HOST}:{config.DB_PORT}/user-public-key', json=payload).json()['public-key']

    public_key = RSA.import_key(user_public_key.encode())
    hashed_nic = SHA256.new(id.encode())
    try:
        pkcs1_15.new(public_key).verify(hashed_nic, bytes.fromhex(nic_signature))
    except (ValueError, TypeError):
        return make_response(payload, 401)
    print('NIC verified')
    # Genarate OTP for user
    otp = aes.get_otp() #int
    otps[id] = otp
    print('OTP sent')
    payload = {
        "otp" : otp,
    }
    return make_response(payload, 200)

@app.route('/submit-ballot', methods=["POST"])
def submit_ballot():
    print('Encrypted ballot recevied')
    # get nic and validate
    id = request.headers['id']
    nic_signature = request.headers['sign']
    payload = {
        "id": id
    }
    user_public_key = requests.post(f'http://{config.DB_HOST}:{config.DB_PORT}/user-public-key', json=payload).json()['public-key']

    public_key = RSA.import_key(user_public_key.encode())
    hashed_nic = SHA256.new(id.encode())
    try:
        pkcs1_15.new(public_key).verify(hashed_nic, bytes.fromhex(nic_signature))
    except (ValueError, TypeError):
        return make_response(payload, 401)    
    print('NIC verified')
    # Extract encrypted ballot
    ciphertext = request.get_json()["ciphertext"]
    nonce = request.get_json()["nonce"]
    cmac_received = request.get_json()["cmac"]
    print(ciphertext,nonce,cmac_received)
    print("Encrypted:",ciphertext)
    print("Received CMAC:",cmac_received)
    print("Nonce:",nonce)
    # CMAC verification
    key = aes.get_key(id,otps[id])
    cmac_generated = aes.cmac(key,ciphertext)
    print('Generated CMAC:',cmac_generated)
    if cmac_generated != cmac_received:
        payload = {
            "message": "CMAC verification failed"
        }
        return make_response(payload, 400)

    print("CMAC verified")
    # Decryption
    decrypted_ballot = aes.decrypt(key,ciphertext,nonce)
    print('Ballot decrypted')
    # Update db that the user has voted
    payload = {
        "id": id
    }
    user_db_updated = requests.post(f'http://{config.DB_HOST}:{config.DB_PORT}/user-update', json=payload)
    

    # Here decrypted ballot assumed to be a string eg: 00100
    vote_lst = list(decrypted_ballot)
   
    # Homomorphic encryption, Save vote
    homomorphic_payload = requests.get(f'http://{config.DB_HOST}:{config.DB_PORT}/homomorphic-keys')
    
    # public key and save in db
    str_bytes_public_key = homomorphic_payload.json()['public'] # used to homomorphically encrypt the voting list 
    public_key = pickle.loads(codecs.decode(str_bytes_public_key.encode(),"base64"))

    encrypted = paillier_encryption.encrypt_vote_array(public_key,vote_lst)
    encrypted_votes = pickle.dumps(encrypted)
    str_encrpypted_votes = codecs.encode(encrypted_votes,"base64").decode()
    print('Ballot homomorphically encrypted')
    # str_encrypted_votes = codecs.encode(str_encrpypted_votes,"base64").decode()
    payload = {
        "vote": str_encrpypted_votes
    }
    vote_saved = requests.post(f'http://{config.DB_HOST}:{config.DB_PORT}/vote-save', json=payload)
    print("User db updated",user_db_updated.status_code)
    print("Vote saved",vote_saved.status_code)
    
    # Response
    if (user_db_updated.status_code == 200) and (vote_saved.status_code == 200):
        del otps[id]
        print('Vote successfull, response sent')
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