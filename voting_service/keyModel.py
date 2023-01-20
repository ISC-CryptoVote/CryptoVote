from pymongo import MongoClient
from phe import paillier
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


client = MongoClient('mongodb://localhost:27017/')
db = client['crypto_vote']
keysCollection=db['key']

#sampleKey = {"ballot": "data3", "signature": "signature","public-key": "public_key_pem.decode()","status": "success"}


def addkey(key):  #user={"user": "Mike","keyd": True}
    keyId=keysCollection.insert_one(key).inserted_id
    return keyId
def generateHomomorphicKeys():
    public_key, private_key = paillier.generate_paillier_keypair()
    payload ={"saved": True,"private": str(private_key).encode(),"public": str(public_key).encode(),"status":"success","type":"H"}
    addkey(payload)
    return payload

def findHomomorphicKey(): 
    key=keysCollection.find_one({"type":"H"})
    if (str(key)=="None"):
        return generateHomomorphicKeys()
    else:
        return key
    
def generateAdminKeys():
    print("Creating a new  admin key")
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    private_key_pem = private_key.export_key()
    public_key_pem = public_key.export_key()
    payload ={"saved": True,"private": private_key_pem.decode(),"public": public_key_pem.decode(),"status":"success","type":"A"}
    
    addkey(payload)
    print("new admin key saved")
    return payload


def findAdminKey(): #
    key=keysCollection.find_one({"type":"A"})
    if (str(key)=="None"):
        return generateAdminKeys()
    else:
        print("Already generated a key")
        return key
    
#print(findHomomorphicKey())