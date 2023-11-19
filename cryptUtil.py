import os
import rsa

import base64, hashlib
from cryptography.fernet import Fernet

def genKeys(overwrite = False) -> None:

    if os.path.exists("private.pem") and os.path.exists("public.pem"):
        print("Public and Private Key already generated! (use genKeys(True) for overwrite)")
        return

    if not os.path.exists("private.pem"):
        # Saving new pubkey and privkey in file
        (pubkey, privkey) = rsa.newkeys(4096, poolsize=8)
        
        print("create")
        with open('private.pem', mode='wb') as privatefile:
            bytepriv = privkey.save_pkcs1()
            privatefile.write(bytepriv)
        with open('public.pem', mode='wb') as publicfile:
            bytepub = pubkey.save_pkcs1()
            publicfile.write(bytepub)

def decode(message) -> str:

    if not (os.path.exists("private.pem") and os.path.exists("public.pem")):
        print("can't find the keys!")
        return
    
    #get private key
    with open('private.pem', mode='rb') as privatefile:
        key = privatefile.read()
        keyPriv = rsa.PrivateKey.load_pkcs1(key)
    
    decrypted = rsa.decrypt(message, keyPriv)
    return decrypted.decode()

def createFernetKey(UID : str, username : str):
    keyUID = username + UID 
    key = hashlib.md5(keyUID.encode()).hexdigest()
    key_64 = base64.urlsafe_b64encode(key.encode()) #store this

    with open('fernet.pem', mode='wb') as fernet:
        fernet.write(key_64)

def getFernetKey():

    if not (os.path.exists("fernet.pem")):
        print("can't find the Fernet keys!")
        return

    with open('fernet.pem', mode='rb') as fernet:
        byteKey = fernet.read()
    
    return byteKey

def encodeWithUDID(message : str, UID : str, username : str) -> str:

    keyUID = username + UID 
    key = hashlib.md5(keyUID.encode()).hexdigest()
    key_64 = base64.urlsafe_b64encode(key.encode()) #store this
    fernetKey = Fernet(key_64)
