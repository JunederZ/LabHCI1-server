
import hashlib

key = 'TJ.532505.a0324'
pad = hashlib.sha256(key.encode('utf-8')).hexdigest()
print(pad)

# encrypt
plaintext = 'hello world'
ciphertext = ''
for i in range(len(plaintext)):
  print(pad[i], i)
  ciphertext += chr(ord(pad[i])^ord(plaintext[i]))

print(ciphertext)
  
# decrypt
result = ''
for i in range(len(ciphertext)):
  result += chr(ord(pad[i])^ord(ciphertext[i]))

print(plaintext)

# plaintext = 'the quick brown fox jumped over.'
