from flask import Flask, make_response
from flask import request
from flask import jsonify

import base64

import json

import cryptUtil

app = Flask(__name__)


@app.route("/register", methods=["POST"])
def register():
    jsons = request.get_json()

    ferKey = cryptUtil.createFernetKey(jsons["deviceID"], jsons["username"])

    cryptUtil.genKeys()

    with open("public.pem", mode="rb") as publicfile:
        key = publicfile.read().decode()

    returns = {
        "key": key,
        "udidKey": ferKey.decode("ascii"),
    }

    decryptedJson = cryptUtil.encodeWithUDID(json.dumps(returns))
    response = make_response(decryptedJson, 200)
    response.mimetype = "text/plain"
    response.content_type = "text/plain"

    # return decryptedJson
    return response


@app.route("/decrypt", methods=["POST"])
def hello():
    jsons = request.get_data()

    messageReturn = base64.b64decode(jsons)

    message = json.loads(cryptUtil.decode(messageReturn))

    print("decrypted message : " + message["message"])

    return "decrypted message : " + message["message"]


if __name__ == "__main__":
    app.run()
