from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['crypto_vote']
votesCollection=db['vote']

sampleVote = {"ballot": "data3", "signature": "signature","public-key": "public_key_pem.decode()","status": "success"}

def addVote(vote):  #user={"user": "Mike","voted": True}
    voteId=votesCollection.insert_one(vote).inserted_id
    return voteId

def getVotes():
    votesLi=[]
    votes=votesCollection.find()
    for x in votes:
        votesLi.append(x)

    return votesLi
#addVote(sampleVote)
#print(getVotes())