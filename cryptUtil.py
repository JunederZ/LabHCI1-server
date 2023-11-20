import os
import rsa
from warnings import warn

import base64, hashlib
from cryptography.fernet import Fernet

def genKeys(overwrite = False) -> None:
    if os.path.exists("/home/veen/LabHCI1-server/private.pem") and os.path.exists("/home/veen/LabHCI1-server/public.pem"):
        print("Public and Private Key already generated! (use genKeys(True) for overwrite)")
        return
    if not os.path.exists("/home/veen/LabHCI1-server/private.pem"):
        # Saving new pubkey and privkey in file
        (pubkey, privkey) = rsa.newkeys(4096, poolsize=8)
        print("create")
        with open('/home/veen/LabHCI1-server/private.pem', mode='wb') as privatefile:
            bytepriv = privkey.save_pkcs1()
            privatefile.write(bytepriv)
        with open('/home/veen/LabHCI1-server/public.pem', mode='wb') as publicfile:
            bytepub = pubkey.save_pkcs1()
            publicfile.write(bytepub)

def decode(message) -> str:
    if not (os.path.exists("/home/veen/LabHCI1-server/private.pem") and os.path.exists("/home/veen/LabHCI1-server/public.pem")):
        print("can't find the keys!")
        return

    #get private key
    with open('/home/veen/LabHCI1-server/private.pem', mode='rb') as privatefile:
        key = privatefile.read()
        keyPriv = rsa.PrivateKey.load_pkcs1(key)

    decrypted = rsa.decrypt(message, keyPriv)
    return decrypted.decode()

def createFernetKey(UID : str, username : str):
    warn("This function is is deprecated.", DeprecationWarning, stacklevel=2)
    keyUID = username + UID 
    key = hashlib.sha256(keyUID.encode()).digest()
    key_64 = base64.b64encode(key) 
    return key_64

def getFernetKey():
    if not (os.path.exists("/home/veen/LabHCI1-server/fernet.pem")):
        print("can't find the Fernet keys!")
        return
    with open('/home/veen/LabHCI1-server/fernet.pem', mode='rb') as fernet:
        byteKey = fernet.read()
    return byteKey

def encodeWithUDID(message : str, UDID: str) -> str:
    fernetKey = Fernet(base64.b64encode(hashlib.sha256(UDID.encode()).digest()))
    cipher = fernetKey.encrypt(message.encode())
    return base64.b64encode(cipher).decode('ascii')