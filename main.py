from languageModel import *
import flask
from flask_cors import CORS
app = flask.Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    data = flask.request.json
    prompt = data['prompt']
    id = data['userID']
    return {"response": message(prompt, id)}

if __name__ == '__main__':
    app.run(debug=True)