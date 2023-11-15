import base64, hashlib
from cryptography.fernet import Fernet

my_password = 'swordfish'
key = hashlib.md5(my_password.encode()).hexdigest()
key_64 = base64.urlsafe_b64encode(key.encode()) #store this
fernetKey = Fernet(key_64)

cipher = fernetKey.encrypt(b"My dirty secrets")

print(key)
print(key_64)
print(cipher)

result = fernetKey.decrypt(cipher)

print(result)