from pymongo import MongoClient

client = MongoClient("mongodb+srv://meesam4687:bonton7266epithet@epithet.nbkmp.mongodb.net/?retryWrites=true&w=majority&appName=Epithet")
db = client["EpithetUserData"]
contextCollection = db["ModelContextRange"]

def pushContext(data, id):
    document = {"userID":id, "inputText": data}
    return contextCollection.insert_one(document)
def getContext(data):
    return contextCollection.find_one({"userID": data})
def deleteContext(id):
    return contextCollection.delete_one({"userID": id})
def updateContext(data, id):
    return contextCollection.update_one({"userID": id}, {"$set": {"inputText": data}})