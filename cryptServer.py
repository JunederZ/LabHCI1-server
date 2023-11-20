from flask import Flask, make_response
from flask import request
from flask import jsonify
from argon2 import PasswordHasher
import logging

import base64

import json

import cryptUtil
from db_util import DBUtil

app = Flask(__name__)
file_handler = logging.FileHandler('/var/log/flaskapp.log')
app.logger.addHandler(file_handler)


@app.route("/register", methods=["POST"])
def register():
    jsons = request.get_json()

    # ferKey = cryptUtil.createFernetKey(jsons["deviceID"], jsons["username"])

    # cryptUtil.genKeys()

    with open("/home/veen/LabHCI1-server/public.pem", mode="rb") as publicfile:
        key = publicfile.read().decode()

    db = DBUtil()
    username = jsons.get('username')
    password = jsons.get('password')
    deviceId = jsons.get('deviceId')
    full_name = jsons.get('fullName')
    res = db.addUser(username, password, deviceId, full_name)
    returns = {
        "key": key,
        "status": res,
        # "udidKey": ferKey.decode("ascii"),
    }

    decryptedJson = cryptUtil.encodeWithUDID(json.dumps(returns), deviceId)
    response = make_response(decryptedJson, 200)
    response.mimetype = "text/plain"
    response.content_type = "text/plain"

    # return decryptedJson
    return response

@app.route("/ping", methods=['POST'])
def higuys():
    data = request.get_data()
    rawdata = base64.b64decode(data)
    decrypted_data = json.loads(cryptUtil.decode(rawdata))
    resp['serverMsg'] = "get some help"
    encrypted_res = cryptUtil.encodeWithUDID(json.dumps(returns), decrypted_data['deviceId'])
    response = make_response(encrypted_res, 200)
    response.mimetype = "text/plain"
    response.content_type = "text/plain"
    return response

@app.route("/decrypt", methods=["POST"])
def hello():
    jsons = request.get_data()

    messageReturn = base64.b64decode(jsons)

    message = json.loads(cryptUtil.decode(messageReturn))

    print("decrypted message : " + message["message"])

    return "decrypted message : " + message["message"]

@app.route('/login', methods=['POST'])
def login():
    data = request.get_data()
    data_bytes = base64.b64decode(data)
    decrypted_json = json.loads(cryptUtil.decode(data_bytes))
    udid = decrypted_json.get('udid')
    password = decrypted_json.get('password')
    user = DBUtil().getByUDID(udid)
    msg = "success"
    if not user: 
        msg = "ga terdaftar" 
        '''kalo belum terdaftar otomatis ga bisa login dong? 
        kan belum dapet pubkey? udid juga belum ada di server'''
        # resp = make_response(decryptedJson, 200)
        # resp.mimetype = "text/plain"
        # resp.content_type = "text/plain"
        # return resp
    username, pw_hash, udid, full_name = user
    try:
        ph=PasswordHasher()
        ph.verify(pw_hash, password)
    except Exception as e:
        msg = "password salah"
    body = {
        "msg": msg,
    }

    encrypted_resp = cryptUtil.encodeWithUDID(json.dumps(body), udid)
    resp = make_response(encrypted_resp, 200)
    resp.mimetype = "text/plain"
    resp.content_type = "text/plain"
    return resp
    

if __name__ == "__main__":
    app.run()
