from saes import SAES
import numpy as np

msg = int('0b1101011100101000', 2)
key = int('0b0100101011110101', 2)
res = int('0b0010010011101100', 2)

print('msg:', msg)
print('key:', key)

saes = SAES(key)
ans = saes.encrpyt(msg, 2)
print(res, ans)
print(saes.decrypt(ans, 2))
# ans = saes.decrpyt(ans, 2)
print(ans)

# mix_col = np.array([[1, 4], [4, 1]])
# inv_mix_col = np.array([[9, 2], [2, 9]])

# def mix_colf(state):
#     res = np.zeros((2, 2)).astype(int)
#     for i in range(2):
#         for j in range(2):
#             for k in range(2):
#                 res[i][j] ^= galoisMult(mix_col[i][k], state[k][j])
#     return res

# def inv_mix_colf(state):
#     res = np.zeros((2, 2)).astype(int)
#     for i in range(2):
#         for j in range(2):
#             for k in range(2):
#                 res[i][j] ^= galoisMult(inv_mix_col[i][k], state[k][j])
#     return res

# def galoisMult(b, a):
#     p = 0
#     hiBitSet = 0
#     for i in range(4):
#         if b & 1 == 1:
#             p ^= a
#         a <<= 1
#         hiBitSet = a & 0x10
#         if hiBitSet:
#             a ^= 0x13
#         b >>= 1
#     return p

# a = np.array([[1, 2], [4, 3]])
# b = mix_colf(a)
# c = inv_mix_colf(b)
# print(a)
# print(b)
# print(c)