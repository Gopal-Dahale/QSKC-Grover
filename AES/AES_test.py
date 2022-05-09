from AES import AES
import numpy as np

master_key = 'SOME 128 BIT KEY'
plaintext = 'ATTACK AT DAWN!1'

key = int(''.join(hex(ord(c))[2:] for c in master_key), 16)
msg = int(''.join(hex(ord(c))[2:] for c in plaintext), 16)

print("key:", key)
print("msg:", msg)

aes = AES(key)
c = aes.encrypt(msg, 10)
print("ciphertext:", c)
m = aes.decrypt(c, 10)
print("plaintext:", m)

if m == msg:
    print("Success!")
else:
    print("Failed!")