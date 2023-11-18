from flask import Flask
from flask import request
from flask import jsonify
import os
import rsa

import cryptUtil

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def encrypt():

    # request.get_json()

    print(request.get_json())
    
    with open('private.pem', mode='rb') as privatefile:
        key = privatefile.read().decode()
        keyPriv = rsa.PrivateKey.load_pkcs1(key)

    key = key.replace("-----BEGIN RSA PRIVATE KEY-----\n", "")
    key = key.replace("\n-----END RSA PRIVATE KEY-----\n", "")

    returns = {"key" : key}

    return returns

    # if not os.path.exists("private.pem"):
    #     # Saving new pubkey and privkey in file

    #     (pubkey, privkey) = rsa.newkeys(2048, poolsize=8)
        
    #     print("create")
    #     with open('private.pem', mode='wb') as privatefile:
    #         bytepriv = privkey.save_pkcs1()
    #         privatefile.write(bytepriv)
    #     with open('public.pem', mode='wb') as publicfile:
    #         bytepub = pubkey.save_pkcs1()
    #         publicfile.write(bytepub)
    
    # with open('private.pem', mode='rb') as privatefile:
    #     key = privatefile.read()
    #     keyPriv = rsa.PrivateKey.load_pkcs1(key)
    # with open('public.pem', mode='rb') as publicfile:
    #     key = publicfile.read()
    #     keyPub = rsa.PublicKey.load_pkcs1(key)

    # message = 'hello Bob!'.encode('utf8')
    # crypto = rsa.encrypt(message, keyPub)
    # message = rsa.decrypt(crypto, keyPriv)

    # js = request.get_json()
    # return jsonify(message.decode('utf8'))  

@app.route('/hello')
def hello():
    return 'Hello, World'

if __name__ == "__main__":
    app.run()