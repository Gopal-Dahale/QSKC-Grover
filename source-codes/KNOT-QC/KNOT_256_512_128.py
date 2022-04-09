
from projectq.ops import H, CNOT, Measure, Toffoli, X, All , Swap
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator

from projectq.meta import Loop, Compute, Uncompute, Control

def KNOT(eng):

    key = eng.allocate_qureg(256)
    nonce = eng.allocate_qureg(256)

    Round_constant_XOR2(eng, key, 0x1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100)
    Round_constant_XOR2(eng, nonce, 0x1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100)

    AD_size = 32  # Multiples of 8-qubit
    P_size = 32  # Multiples of 8-qubit

    input_AD = eng.allocate_qureg(AD_size)
    input_P = eng.allocate_qureg(P_size)

    Round_constant_XOR2(eng, input_AD, 0x03020100)
    Round_constant_XOR2(eng, input_P, 0x03020100)

    # Padding
    u = UPad(eng, AD_size)
    v = UPad(eng, P_size)

    # Allocate C according to P_size
    if(v!= 0):
        C = eng.allocate_qureg((v-1)*128 + (P_size%128))

    # Initialization
    print('Initialization')
    S = []
    for i in range(256):
        S.append(nonce[i])
    for i in range(256):
        S.append(key[i])

    Round100(eng, S)

    # Processing Associated Data
    print('Processing AD')
    if (u != 0):
        Processing_AD(eng, S, input_AD, u, AD_size)
    else:
        X | S[-1]

    #Encryption
    if (v != 0):
        print('Encryption')
        Encryption(eng, input_P, S, C, v, P_size)

    #Finalization
    print('Finalization')
    Round56(eng, S) # S[0~127] becomes Tag

    #Print
    All(Measure) | S

    print('------------Ciphertext---------------')
    for i in range(256):
        print(int(S[255 - i]), end=' ')

    if (v != 0):
        All(Measure) | C
        for i in range((v-1)*128 + (P_size%128)):
            print(int(C[(v-1)*128 + (P_size%128)-1 - i]), end=' ')

def UPad(eng, size):

    padsize = 0

    if(size > 0):
        padsize  = 128 - (size % 128)

    return int((size + padsize) / 128)


# nr0 : 100, nr : 52,  nrf : 56

def Round100(eng, b):

    rc = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x41, 0x03, 0x06,
        0x0c, 0x18, 0x30, 0x61, 0x42, 0x05, 0x0a, 0x14, 0x28, 0x51, 0x23, 0x47,
        0x0f, 0x1e, 0x3c, 0x79, 0x72, 0x64, 0x48, 0x11, 0x22, 0x45, 0x0b, 0x16,
        0x2c, 0x59, 0x33, 0x67, 0x4e, 0x1d, 0x3a, 0x75, 0x6a, 0x54, 0x29, 0x53,
        0x27, 0x4f, 0x1f, 0x3e, 0x7d, 0x7a, 0x74, 0x68, 0x50, 0x21, 0x43, 0x07,
        0x0e, 0x1c, 0x38, 0x71, 0x62, 0x44, 0x09, 0x12, 0x24, 0x49, 0x13, 0x26,
        0x4d, 0x1b, 0x36, 0x6d, 0x5a, 0x35, 0x6b, 0x56, 0x2d, 0x5b, 0x37, 0x6f,
        0x5e, 0x3d, 0x7b, 0x76, 0x6c, 0x58, 0x31, 0x63, 0x46, 0x0d, 0x1a, 0x34,
        0x69, 0x52, 0x25, 0x4b, 0x17, 0x2e, 0x5d, 0x3b, 0x77, 0x6e, 0x5c, 0x39,
        0x73, 0x66, 0x4c, 0x19, 0x32, 0x65, 0x4a, 0x15, 0x2a, 0x55, 0x2b, 0x57,
        0x2f, 0x5f, 0x3f, 0x7f, 0x7e, 0x7c, 0x78, 0x70, 0x60, 0x40]

    for i in range(100):
        Round_constant_XOR(eng, b, rc[i])
        SubColumn(eng, b)
        ShiftRow(eng, b)
        print('Round',i)

def Round52(eng, b):

    rc = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x41, 0x03, 0x06,
        0x0c, 0x18, 0x30, 0x61, 0x42, 0x05, 0x0a, 0x14, 0x28, 0x51, 0x23, 0x47,
        0x0f, 0x1e, 0x3c, 0x79, 0x72, 0x64, 0x48, 0x11, 0x22, 0x45, 0x0b, 0x16,
        0x2c, 0x59, 0x33, 0x67, 0x4e, 0x1d, 0x3a, 0x75, 0x6a, 0x54, 0x29, 0x53,
        0x27, 0x4f, 0x1f, 0x3e, 0x7d, 0x7a, 0x74, 0x68, 0x50, 0x21, 0x43, 0x07,
        0x0e, 0x1c, 0x38, 0x71, 0x62, 0x44, 0x09, 0x12, 0x24, 0x49, 0x13, 0x26,
        0x4d, 0x1b, 0x36, 0x6d, 0x5a, 0x35, 0x6b, 0x56, 0x2d, 0x5b, 0x37, 0x6f,
        0x5e, 0x3d, 0x7b, 0x76, 0x6c, 0x58, 0x31, 0x63, 0x46, 0x0d, 0x1a, 0x34,
        0x69, 0x52, 0x25, 0x4b, 0x17, 0x2e, 0x5d, 0x3b, 0x77, 0x6e, 0x5c, 0x39,
        0x73, 0x66, 0x4c, 0x19, 0x32, 0x65, 0x4a, 0x15, 0x2a, 0x55, 0x2b, 0x57,
        0x2f, 0x5f, 0x3f, 0x7f, 0x7e, 0x7c, 0x78, 0x70, 0x60, 0x40]

    for i in range(52):
        Round_constant_XOR(eng, b, rc[i])
        SubColumn(eng, b)
        ShiftRow(eng, b)
        print('Round',i)

def Round56(eng, b):

    rc = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x41, 0x03, 0x06,
        0x0c, 0x18, 0x30, 0x61, 0x42, 0x05, 0x0a, 0x14, 0x28, 0x51, 0x23, 0x47,
        0x0f, 0x1e, 0x3c, 0x79, 0x72, 0x64, 0x48, 0x11, 0x22, 0x45, 0x0b, 0x16,
        0x2c, 0x59, 0x33, 0x67, 0x4e, 0x1d, 0x3a, 0x75, 0x6a, 0x54, 0x29, 0x53,
        0x27, 0x4f, 0x1f, 0x3e, 0x7d, 0x7a, 0x74, 0x68, 0x50, 0x21, 0x43, 0x07,
        0x0e, 0x1c, 0x38, 0x71, 0x62, 0x44, 0x09, 0x12, 0x24, 0x49, 0x13, 0x26,
        0x4d, 0x1b, 0x36, 0x6d, 0x5a, 0x35, 0x6b, 0x56, 0x2d, 0x5b, 0x37, 0x6f,
        0x5e, 0x3d, 0x7b, 0x76, 0x6c, 0x58, 0x31, 0x63, 0x46, 0x0d, 0x1a, 0x34,
        0x69, 0x52, 0x25, 0x4b, 0x17, 0x2e, 0x5d, 0x3b, 0x77, 0x6e, 0x5c, 0x39,
        0x73, 0x66, 0x4c, 0x19, 0x32, 0x65, 0x4a, 0x15, 0x2a, 0x55, 0x2b, 0x57,
        0x2f, 0x5f, 0x3f, 0x7f, 0x7e, 0x7c, 0x78, 0x70, 0x60, 0x40]

    for i in range(56):
        Round_constant_XOR(eng, b, rc[i])
        SubColumn(eng, b)
        ShiftRow(eng, b)
        print('Round',i)

def Round_constant_XOR(eng, k, rc):
    for i in range(7):
        if(rc >> i & 1):
             X | k[i]

def SubColumn(eng, b):
    b_column = []

    for i in range(128):
        b_column.append(b[i])
        b_column.append(b[128 + i])
        b_column.append(b[256+i])
        b_column.append(b[384+i])

    for i in range(128):
        Sbox_LIGHTER_R(eng, b_column[i*4:(i*4)+4])

def Sbox_LIGHTER_R(eng, b):

    X | b[0]
    Toffoli | (b[0], b[1], b[2])
    Toffoli | (b[1], b[2], b[0])

    CNOT | (b[2], b[3])
    CNOT | (b[3], b[1])
    CNOT | (b[1], b[0])

    Toffoli | (b[0], b[2], b[1])
    Toffoli | (b[0], b[1], b[2])

    #b2 = b0
    #b1 = b2
    #b0 = b1

    Swap | (b[2], b[0])
    Swap | (b[0], b[1])

# 127~0
# 255~128
# 383~256
# 511~384

def ShiftRow(eng, b):

    for j in range(1):  # Row1 ≪ 1
        for i in range(127):
            Swap | (b[255-i], b[254-i])

    for j in range(16):  # Row2 ≪ 16
        for i in range(127):
            Swap | (b[383-i], b[382-i])

    for j in range(25):  # # Row3 ≪ 25
        for i in range(127):
            Swap | (b[511-i], b[510-i])


def Processing_AD(eng, S, AD, u, AD_size):

    # AD -> 128-bit i.e (1 block case)
    for i in range(u):
        if(i == u-1):
            for z in range(AD_size % 128):
                CNOT | (AD[i * 128 + z], S[z])
            X | S[(AD_size) % 128]
        else :
            for j in range(128):
                CNOT | (AD[i*128 + j], S[j])
        Round52(eng, S)

    X | S[-1]

def Encryption(eng, P, S, C, v, P_size):

    for j in range(v-1):
        for i in range(128):
            CNOT | (P[128*j + i], S[i])
        # Copy C
        for i in range(128):
            CNOT | (S[i], C[128*j + i])

        Round52(eng, S)

    #last
    for i in range(P_size % 128):
        CNOT | (P[128*(v-1) + i], S[i])
    X | S[(P_size) % 128]

    # Copy C
    for i in range(P_size % 128):
        CNOT | (S[i], C[128*(v-1) + i])



def Round_constant_XOR2(eng, k, rc):
    for i in range(256):
        if(rc >> i & 1):
             X | k[i]

def Round_constant_XOR3(eng, k, rc):
    for i in range(16):
        if(rc >> i & 1):
             X | k[i]

################ Encryption ###############
Simulate = ClassicalSimulator()
eng = MainEngine(Simulate)
(KNOT(eng))

eng.flush()
