import base64
from flask import Flask, make_response, request, jsonify
import json
import cryptUtil
from argon2 import PasswordHasher

from db_util import DBUtil

app = Flask(__name__)
@app.route('/register', methods=['POST'])
def register():
    pass

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
        return "ga terdaftar" 
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
        return "password salah"
    body = {
        "msg": msg,
    }
    encrypted_resp = cryptUtil.encodeWithUDID(body, udid)
    resp = make_response(encrypted_resp, 200)
    resp.mimetype = "text/plain"
    resp.content_type = "text/plain"
    return resp
    

if __name__ == "__main__":
    app.run()