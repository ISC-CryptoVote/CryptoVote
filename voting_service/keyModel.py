from pymongo import MongoClient
from phe import paillier
client = MongoClient('mongodb://localhost:27017/')
db = client['crypto_vote']
keysCollection=db['key']

#sampleKey = {"ballot": "data3", "signature": "signature","public-key": "public_key_pem.decode()","status": "success"}


def addkey(key):  #user={"user": "Mike","keyd": True}
    keyId=keysCollection.insert_one(key).inserted_id
    return keyId
def generateHomomorphicKeys():
    public_key, private_key = paillier.generate_paillier_keypair()
    payload ={"saved": True,"private": str(private_key).encode('utf-8'),"public": str(public_key).encode('utf-8'),"status":"success","type":"H"}
    addkey(payload)
    return payload

def findHomomorphicKey(): 
    key=keysCollection.find_one({"type":"H"})
    if (str(key)=="None"):
        return generateHomomorphicKeys()
    else:
        return key
    
def generateAdminKeys():
    # public_key, private_key = paillier.generate_paillier_keypair()
    # payload ={"saved": True,"private": private_key,"public": public_key,"status":"success","type":"H"}
    # addkey(payload)
    # return payload
    return


def findAdminKey(): #
    key=keysCollection.find_one({"type":"A"})
    if (str(key)=="None"):
        return generateHomomorphicKeys()
    else:
        return key
    
print(findHomomorphicKey())