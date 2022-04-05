from saes import SAES

msg = int('0b1101011100101000', 2)
key = int('0b0100101011110101', 2)
res = int('0b0010010011101100', 2)
saes = SAES(key)
ans = saes.encrpyt(msg)
print(res, ans)