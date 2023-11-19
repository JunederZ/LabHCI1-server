from flask import Flask
from flask import request
from flask import jsonify

import base64

import json

import cryptUtil

app = Flask(__name__)

@app.route('/register', methods=['GET'])
def encrypt():

    cryptUtil.genKeys()
    
    with open('public.pem', mode='rb') as publicfile:
        key = publicfile.read().decode()
        
    returns = {'key' : key}

    return json.dumps(returns)

@app.route('/decrypt', methods=['POST'])
def hello():

    jsons = request.get_data()

    messageReturn = base64.b64decode(jsons)

    message = json.loads(cryptUtil.decode(messageReturn))

    print('decrypted message : ' + message["message"])

    return 'decrypted message : ' + message['message']

if __name__ == "__main__":
    app.run()