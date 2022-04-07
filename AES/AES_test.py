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

# v = encrypted.reshape(16)
# v = ''.join(c for c in list(map(hex_fix, v)))

# Convert Hex string to ASCII string
# v = bytes.fromhex(v).decode('utf-8')

# print(cipher)

# aescode = AESCODE(int(''.join(hex(ord(c))[2:] for c in master_key), 16))
# encrypted = aescode.encrypt(int(''.join(hex(ord(c))[2:] for c in plaintext),
# 16))

# print(hex(encrypted)[2:])
# for i in range(9, 0, -1):
#     print(i)

# c7426b18d2e8e1881d578d73143538a9

# [[65 67 84 87]
#  [84 75 32 78]
#  [84 32 68 33]
#  [65 65 65 49]]