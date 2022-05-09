from saes import SAES
import numpy as np

msg = int('0b1101011100101000', 2)
key = int('0b0100101011110101', 2)
res = int('0b0010010011101100', 2)

print('msg:', msg)
print('key:', key)

saes = SAES(key)
ans = saes.encrpyt(msg, 2)
print(res, bin(ans)[2:].zfill(16))
ans = saes.decrypt(ans, 2)
print(ans)
print(bin(ans)[2:].zfill(16))