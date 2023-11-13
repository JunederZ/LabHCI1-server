from flask import Flask
from flask import request
from flask import jsonify
import rsa

app = Flask(__name__)

@app.route('/register', methods=['GET'])
def encrypt():
    print("start")

    (pubkey, privkey) = rsa.newkeys(2048, poolsize=8)



    with open('private.pem', mode='wb') as privatefile:
        bytepriv = privkey.save_pkcs1()
        privatefile.write(bytepriv)
    with open('public.pem', mode='wb') as publicfile:
        bytepub = pubkey.save_pkcs1()
        publicfile.write(bytepub)
    
    with open('private.pem', mode='rb') as privatefile:
        # privatefile.write(file)
        key = privatefile.read()

    keyPriv = rsa.PrivateKey.load_pkcs1(key)

    message = 'hello Bob!'.encode('utf8')
    crypto = rsa.encrypt(message, pubkey)
    message = rsa.decrypt(crypto, keyPriv)
    print(keyPriv)

    js = request.get_json()
    return jsonify(message.decode('utf8'))  

@app.route('/hello')
def hello():
    return 'Hello, World'


# app.run()