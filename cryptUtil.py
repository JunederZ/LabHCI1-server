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
    key = hashlib.sha256(keyUID.encode()).digest()

    key_64 = base64.b64encode(key) #store this #why, why don't we call it directly to udid encryption

    with open('fernet.pem', mode='wb') as fernet:
        fernet.write(key_64)

    return key_64


def getFernetKey():

    if not (os.path.exists("fernet.pem")):
        print("can't find the Fernet keys!")
        return

    with open('fernet.pem', mode='rb') as fernet:
        byteKey = fernet.read()
    
    return byteKey

def encodeWithUDID(message : str, UDID: str) -> str:

    # fernetKey = Fernet(getFernetKey()) 
    # sori ga bikin branch baru
    fernetKey = Fernet(base64.b64encode(hashlib.sha256(UDID.encode()).digest()))

    cipher = fernetKey.encrypt(message.encode())

    return base64.b64encode(cipher).decode('ascii')

# print(encodeWithUDID("{\"key\":\"-----BEGIN RSA PUBLIC KEY-----\\nMIICCgKCAgEAg/7OX+k1GIkE+3EYvMzBgeTvBLkkGAHqes2EzFmHPBpPWERuo34I\\nrpAf4oXdh5gHnnUgP5lm6LGj83NvN9azZm+uxeL2XnDAe5OgSf6IHHmhQ+5ABrmR\\nYy7TI838xeC6Kb0r8/Xh4aDL82tduZNRcQp8TPBiSae7CBQ8GczNsx2vXYHRia0d\\nRdzFGxSHSrEHXfiD0p6NWdX9OmXzEUM8fVDwELPF6T0+KIH6vOr9bwem/43BL/Na\\n9hAeEzpiFfoakwLrHxvXziw4G3yKnq2/BkXDt/IMpfjIg0TXiN4+NTFdkJ3U4IxG\\nk6hNsbzjVK7mU+iWwf3ijb7wXH02q9t4qGVHT1AjaNfRuHs2mPFTiw9txUgr7JMB\\n3joBwHVkMOJa3+r45yJBcOhAVbA5BJ1kTegb6yrd6Vf7h7NmQxw85/vqSreDf51i\\n8/fBATcN22wLbU7iI1hecCO4END41t1vaPCPK9PQqtGnQgaGF4z6cftmGyyf2+T3\\nhQQZg+/eP5bEiCUiafDindjwrxM7r7V9/6m07/++yVo1u4ti1CbaNFKuVyvrETZ3\\nRhBusM2lpSyvElBmod70Bql4HsWjjopAXHAgATbtNbZWEflPW3j4+kAjQOXgoq+b\\n0XJIZvlSqGfF6Xuf3BX4noARv4Hu+Q4YKkuQEAwO8OxCGIQ3z1RiUYMCAwEAAQ==\\n-----END RSA PUBLIC KEY-----\\n\"}", "KAISAN"))
# print(decode(base64.b64decode("LjmKnDXt5EF0kZt+59kb5n6bt9bD7feSeDfEEf3zRvXGYLsQllWj4kMjx8MPL4a0ZZy49GUM5kl6N1j2fOueRTv+XczkteThkoMJyEQtGqNGBs04BArnsxXMQ74J0AfgknKX5SxL97JRpP4mcjlW1TbDg29rSVgxrvj3JQ785mo3cNpeh9zK6sMMrPSCWJNZGl8UximyEhpiLs/MgeYB2vIUqR38lY2zq6y37hHXOSxKHXyorXD8prCjhfA635giCRGR9HLAfbycKcd/SkVJrDU06JAj6NEcUKyw7iYE4Pgq12peGSiyjbGoWvuQVt9whGxdBcqAhh3LQ3wswZbKLX1esOuiO/aektLvHqhrOIScOvavgyGND3y6+uwzllJXGnS2yR+Q+2m8gwh1wxhSbxooahIExn23lIZfsnN0KjaUI2EpCipvL83Mo6LHExrzV0FP2uuUfuqNIH79UM70z706ZJfyE1QKpqogjGoWcoAaLWYKh+LNs7vXQW6AFMSFqDYUQ8d2Saz30bkSy1NtagE+JUINvlpaHq7sv0yo+UGCt7gxmh8acAqkNxAlRNiM7ckuHBMuL515eQMrvlklgV3U/8g13IkOlwuLqayllWnAXw7R9py4StcBY8so3Appbs1GvFIhBlKdudKVNvCVe3wK/WVuwH0tl/3ywKBFVFc=")))