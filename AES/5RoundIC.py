from AES import AES
import numpy as np
import numba
import time

master_key = 'SOME 128 BIT KEY'
plaintext = 'ATTACK AT DAWN!1'

key = int(''.join(hex(ord(c))[2:] for c in master_key), 16)
msg = int(''.join(hex(ord(c))[2:] for c in plaintext), 16)

aes = AES(key)
c = aes.encrypt(msg, 5)

n = 2**8
P = np.empty(n)


@numba.njit
def generate_pts():
    P = np.arange(0, 256)
    return P


s = time.time()
P = generate_pts()
e = time.time()
print(e - s)

s = time.time()
P = generate_pts()
e = time.time()
print(e - s)

P = np.empty(n)


def gp(P):
    P = np.arange(0, 256)
    return P


s = time.time()
P = gp(P)
e = time.time()
print(e - s)

s = time.time()
P = gp(P)
e = time.time()
print(e - s)
