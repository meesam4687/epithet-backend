from languageModel import *
import flask
from flask_cors import CORS
app = flask.Flask(__name__)
CORS(app)
from userCreationHandler import createUser
from encryptionHandler import derive_key, decrypt_token
from databaseFunctions import getUser

@app.route('/generate', methods=['POST'])
def generate():
    data = flask.request.json
    prompt = data['prompt']
    id = data['username']
    user = getUser(data["username"])
    key = derive_key(data["password"], user["password"]["salt"])
    decrypted_token = decrypt_token(user["password"]["encrypted_token"], key, user["password"]["iv"])
    if decrypted_token:
        if isinstance(decrypted_token, bytes):
            import base64
            decrypted_token = base64.b64encode(decrypted_token).decode('ascii')
        if(data["token"] == decrypted_token):
                return {"response": message(prompt, id)}
        else:
            return {"status": "failed"}
    else:
        return {"status": "failed"}

    

@app.route('/login', methods=['POST'])
def login():
    data = flask.request.json
    user = getUser(data["username"])
    key = derive_key(data["password"], user["password"]["salt"])
    try:
        decrypted_token = decrypt_token(user["password"]["encrypted_token"], key, user["password"]["iv"])
        if decrypted_token:
            if isinstance(decrypted_token, bytes):
                import base64
                decrypted_token = base64.b64encode(decrypted_token).decode('ascii')
            return {"status": "ok", "token": decrypted_token}
        else:
            return {"status": "failed"}
    except Exception as e:
        print("Error during login process:", e)
        return {"status": "failed"}
    
@app.route('/auth', methods=['POST'])
def auth():
    data = flask.request.json
    try:
        user = getUser(data["username"])
        key = derive_key(data["password"], user["password"]["salt"])
        decrypted_token = decrypt_token(user["password"]["encrypted_token"], key, user["password"]["iv"])
        if decrypted_token:
            if isinstance(decrypted_token, bytes):
                import base64
                decrypted_token = base64.b64encode(decrypted_token).decode('ascii')
            if(data["token"] == decrypted_token):
                return {"status": "ok"}
            else:
                return {"status": "failed"}
        else:
            return {"status": "failed"}
    except Exception as e:
        print("Error during auth process:", e)
        return {"status": "failed"}

@app.route('/signup', methods=['POST'])
def signup():
    data = flask.request.json
    return createUser(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1010)