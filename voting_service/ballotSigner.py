from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import keyModel
import random

def generateBallotId(userName):
    randomNumber = random.getrandbits(128)
    return  str(randomNumber)+userName["user"]



def getBallot(userName): #{"user":"Sam"}
    data = generateBallotId(userName)
    keyData=keyModel.findAdminKey()
    private_key = RSA.import_key(keyData["private"])
    hashed_data = SHA256.new(data.encode())
    signature = pkcs1_15.new(private_key).sign(hashed_data)
    payload ={"ballot": hashed_data, "signature": signature.hex(),"public-key": keyData["public"],"status":"success"}
    return payload








print(getBallot({"user":"Sam"}))