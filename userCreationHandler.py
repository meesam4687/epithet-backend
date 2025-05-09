from encryptionHandler import createPassword
from databaseFunctions import pushUsers

def createUser(data):
    passwd = createPassword(data["password"])
    userObject = {
        "username": data["username"],
        "password": passwd
    }
    try:
        pushUsers(userObject)
        return {"status": "ok"}
    except:
        return {"status": "failed"}