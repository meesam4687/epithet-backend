from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
client = MongoClient( os.getenv("MONGO_URL") )
db = client["EpithetUserData"]

contextCollection = db["ModelContextRange"]
userInfo = db["UserInformation"]

def pushContext(data, id):
    document = {"userID":id, "inputText": data}
    return contextCollection.insert_one(document)
def getContext(data):
    return contextCollection.find_one({"userID": data})
def deleteContext(id):
    return contextCollection.delete_one({"userID": id})
def updateContext(data, id):
    return contextCollection.update_one({"userID": id}, {"$set": {"inputText": data}})

def pushUsers(userObject):
    return userInfo.insert_one(userObject)
def getUser(username):
    return userInfo.find_one({"username": username})