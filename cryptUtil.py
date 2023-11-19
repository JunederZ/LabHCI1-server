import os
import rsa

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
    keyUID = username + UID 
    key = hashlib.sha256(keyUID.encode()).digest()

    key_64 = base64.b64encode(key) #store this #why, why don't we call it directly to udid encryption

    with open('/home/veen/LabHCI1-server/fernet.pem', mode='wb') as fernet:
        fernet.write(key_64)

    return key_64


def getFernetKey():

    if not (os.path.exists("/home/veen/LabHCI1-server/fernet.pem")):
        print("can't find the Fernet keys!")
        return

    with open('/home/veen/LabHCI1-server/fernet.pem', mode='rb') as fernet:
        byteKey = fernet.read()
    
    return byteKey

def encodeWithUDID(message : str, UDID: str) -> str:

    # fernetKey = Fernet(getFernetKey()) 
    # sori ga bikin branch baru
    fernetKey = Fernet(base64.b64encode(hashlib.sha256(UDID.encode()).digest()))

    cipher = fernetKey.encrypt(message.encode())

    return base64.b64encode(cipher).decode('ascii')

# print(encodeWithUDID("{\"key\":\"-----BEGIN RSA PUBLIC KEY-----\\nMIICCgKCAgEAg/7OX+k1GIkE+3EYvMzBgeTvBLkkGAHqes2EzFmHPBpPWERuo34I\\nrpAf4oXdh5gHnnUgP5lm6LGj83NvN9azZm+uxeL2XnDAe5OgSf6IHHmhQ+5ABrmR\\nYy7TI838xeC6Kb0r8/Xh4aDL82tduZNRcQp8TPBiSae7CBQ8GczNsx2vXYHRia0d\\nRdzFGxSHSrEHXfiD0p6NWdX9OmXzEUM8fVDwELPF6T0+KIH6vOr9bwem/43BL/Na\\n9hAeEzpiFfoakwLrHxvXziw4G3yKnq2/BkXDt/IMpfjIg0TXiN4+NTFdkJ3U4IxG\\nk6hNsbzjVK7mU+iWwf3ijb7wXH02q9t4qGVHT1AjaNfRuHs2mPFTiw9txUgr7JMB\\n3joBwHVkMOJa3+r45yJBcOhAVbA5BJ1kTegb6yrd6Vf7h7NmQxw85/vqSreDf51i\\n8/fBATcN22wLbU7iI1hecCO4END41t1vaPCPK9PQqtGnQgaGF4z6cftmGyyf2+T3\\nhQQZg+/eP5bEiCUiafDindjwrxM7r7V9/6m07/++yVo1u4ti1CbaNFKuVyvrETZ3\\nRhBusM2lpSyvElBmod70Bql4HsWjjopAXHAgATbtNbZWEflPW3j4+kAjQOXgoq+b\\n0XJIZvlSqGfF6Xuf3BX4noARv4Hu+Q4YKkuQEAwO8OxCGIQ3z1RiUYMCAwEAAQ==\\n-----END RSA PUBLIC KEY-----\\n\"}", "KAISAN"))
# print(decode(base64.b64decode("ktsabit")))