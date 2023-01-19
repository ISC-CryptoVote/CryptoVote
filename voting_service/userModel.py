from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['crypto_vote']
userCollection=db['user']

sampleUser = {"user": "Mike","voted": True}

def addUser(user):  #user={"user": "Mike","voted": True}
    userId=userCollection.insert_one(user).inserted_id
    return userId

def findUser(userName): #userName={"user": "Mike"}
    user=userCollection.find_one(userName)
    return user

def updateVotedStatus(userName,updatedValue):#{"user": "Mike"}, { 'voted': True } 
    userId=userCollection.update_one(userName,{ "$set": updatedValue }).inserted_id
    return userId
#addUser(sampleUser)
#print(updateVotedStatus())
#print(findUser({"user": "Me"}))