import os
import rsa


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
    return decrypted

# def encodeWithUDI(message, UID) -> str:


