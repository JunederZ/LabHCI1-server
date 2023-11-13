from flask import Flask
from flask import request
from flask import jsonify
import rsa

app = Flask(__name__)

@app.route('/register', methods=['GET'])
def encrypt():
    print("start")

    (pubkey, privkey) = rsa.newkeys(2048, poolsize=8)

    with open('private.pem', mode='rw+b') as privatefile:
        privatefile.write(privkey)
    
        key = rsa.PrivateKey.load_pkcs1(privatefile.read())

    message = 'hello Bob!'.encode('utf8')
    crypto = rsa.encrypt(message, pubkey)
    message = rsa.decrypt(crypto, key)
    print(key)

    js = request.get_json()
    return jsonify(message.decode('utf8'))  

@app.route('/hello')
def hello():
    return 'Hello, World'


# app.run()