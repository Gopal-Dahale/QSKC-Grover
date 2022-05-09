import numpy as np


# AES class for implementing different AES operations
class AES:
    # class methods

    def __init__(self, main_key):
        self.main_key = self.encode(main_key)

        # mix column matrix
        self.mix_col = np.array([[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3],
                                 [3, 1, 1, 2]])
        self.inv_mix_col = np.array([[14, 11, 13, 9], [9, 14, 11, 13],
                                     [13, 9, 14, 11], [11, 13, 9, 14]])

        # list of some round constants
        self.round_constants = [
            0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47
        ]

        # AES Substitution box
        self.sbox = [
            0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
            0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
            0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
            0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
            0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
            0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
            0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
            0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
            0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
            0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
            0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
            0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
            0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
            0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
            0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
            0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
            0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
            0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
            0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
            0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
            0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
            0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
            0x54, 0xbb, 0x16
        ]

        # AES Inverse substitution box
        self.sbox_inv = [
            0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3,
            0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f,
            0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54,
            0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b,
            0x42, 0xfa, 0xc3, 0x4e, 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24,
            0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8,
            0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d,
            0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
            0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab,
            0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3,
            0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1,
            0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41,
            0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
            0x73, 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9,
            0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d,
            0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
            0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,
            0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07,
            0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 0x60,
            0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f,
            0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5,
            0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b,
            0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55,
            0x21, 0x0c, 0x7d
        ]

        self.round_keys = self.generate_round_keys()

    def generate_round_keys(self):
        """
        It takes the main key and generates the round keys by using the new_round_key function
        
        Returns:
          The round keys are being returned.
        """
        round_keys = []
        prev_key = self.main_key
        for i in range(len(self.round_constants) - 1):
            new_key = self.new_round_key(prev_key, i + 1)
            round_keys.append(new_key)
            prev_key = new_key
        return round_keys
        
    def encode(self, num):
        """
        It takes a number and converts it into a 4x4 matrix of bytes
        
        Args:
          num: the number to be encoded
        
        Returns:
          A 4x4 matrix of the binary representation of the number.
        """
        mat = np.zeros((4, 4)).astype(int)
        for i in range(4):
            for j in range(4):
                mat[j][i] = num >> (8 * (15 - (j + 4 * i))) & 0xFF
        return mat

    def shiftRows(self, mat):
        """
        It takes a 4x4 matrix and shifts the rows by the row number
        
        Args:
          mat: The matrix to be shifted
        
        Returns:
          the shifted matrix.
        """
        temp_state = np.zeros((4, 4)).astype(int)
        for i in range(4):
            for j in range(4):
                temp_state[i][j] = mat[i][(i + j) % 4]
        return temp_state

    def invShiftRows(self, mat):
        """
        It takes a 4x4 matrix and shifts the rows to the right by the row number
        
        Args:
          mat: The matrix to be shifted
        
        Returns:
          the matrix after the inverse shift rows operation has been performed.
        """
        temp_state = np.zeros((4, 4)).astype(int)
        for i in range(4):
            for j in range(4):
                temp_state[i][(i + j) % 4] = mat[i][j]
        return temp_state

    def subBytes(self, mat):
        """
        It takes a matrix of bytes and returns a matrix of bytes where each byte is replaced by the
        corresponding byte in the S-box.
        
        Args:
          mat: The matrix to be operated on.
        
        Returns:
          The subBytes function is returning the state matrix after the subBytes operation has been
        performed.
        """
        temp_state = np.array([[self.sbox[j] for j in i] for i in mat])
        return temp_state

    def invSubBytes(self, mat):
        """
        It takes a matrix as input, and returns a matrix where each element is the inverse of the
        corresponding element in the input matrix
        
        Args:
          mat: the matrix to be operated on
        
        Returns:
          the inverse of the sbox matrix.
        """
        temp_state = np.array([[self.sbox_inv[j] for j in i] for i in mat])
        return temp_state

    
    def __galoisMult(self, b, a):
        """
        It takes two bytes, multiplies them together, and returns the result
        
        Args:
          b: the byte to multiply
          a: The byte to be multiplied.
        
        Returns:
          The result of the multiplication of two numbers in the Galois field.
        """
        p = 0
        hiBitSet = 0
        for i in range(8):
            if b & 1 == 1:
                p ^= a
            hiBitSet = a & 0x80
            a <<= 1
            if hiBitSet == 0x80:
                a ^= 0x1b
            b >>= 1
        return p % 256

    def mixColumns(self, mat):
        """
        For each row in the matrix, multiply the row by the mix column matrix and XOR the results
        together
        
        Args:
          mat: the matrix to be multiplied
        
        Returns:
          The result of the mixColumns function is a 4x4 matrix.
        """
        res = np.zeros((4, 4)).astype(int)

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    res[i][j] ^= self.__galoisMult(self.mix_col[i][k],
                                                   mat[k][j])

        return res

    def invMixColumns(self, mat):
        """
        For each row in the matrix, multiply the row by the inverse mix column matrix and XOR the
        results together
        
        Args:
          mat: the matrix to be multiplied
        
        Returns:
          The result of the matrix multiplication.
        """
        res = np.zeros((4, 4)).astype(int)

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    res[i][j] ^= self.__galoisMult(self.inv_mix_col[i][k],
                                                   mat[k][j])

        return res

    def addKey(self, mat, key):
        """
        It takes a matrix and a key, and returns the matrix XORed with the key
        
        Args:
          mat: The matrix to be encrypted
          key: The key to be used for encryption.
        
        Returns:
          the bitwise XOR of the matrix and the key.
        """
        return np.bitwise_xor(mat, key)

    def new_round_key(self, previous_round_key, round):
        """
        The new round key is the previous round key with the last column rotated by 1, the last column
        sboxed, and the first column xored with the round constant
        
        Args:
          previous_round_key: The key from the previous round.
          round: the current round number
        
        Returns:
          The new round key is being returned.
        """
        key = previous_round_key.copy()
        col = key[:, 3].copy()  # last column of key
        col = np.append(col[1:], [col[0:1]])  # rotating last column by 1

        # apply sbox to column
        for i in range(4):
            col[i] = self.sbox[col[i]]

        # apply round constant
        col[0] = (self.round_constants[round] ^ col[0])

        # get the first column of new round key
        key[:, 0] = np.bitwise_xor(key[:, 0], col)

        # remaining columns of new round key
        for i in range(1, 4):
            key[:, i] = np.bitwise_xor(key[:, i], key[:, i - 1])

        return key

    def encrypt(self, msg, n):
        """
        We take the message, add the main key, then we do the subBytes, shiftRows, mixColumns, and
        addKey functions n times, then we do the subBytes and shiftRows functions, and finally we add
        the last key
        
        Args:
          msg: the message to be encrypted
          n: number of rounds
        
        Returns:
          The encrypted message.
        """
        state = self.encode(msg)
        state = self.addKey(state, self.main_key)

        for i in range(1, n):
            state = self.subBytes(state)
            state = self.shiftRows(state)
            state = self.mixColumns(state)
            state = self.addKey(state, self.round_keys[i])

        state = self.subBytes(state)
        state = self.shiftRows(state)
        state = self.addKey(state, self.round_keys[n])

        state = state.transpose().reshape(16)
        state = list(map(lambda a: hex(a)[2:].zfill(2), state))
        state = ''.join(state)
        return int(state, 16)

    def decrypt(self, cipher, n):
        """
        We start with the ciphertext, and then we apply the inverse of the encryption function to it,
        starting with the last round key and working our way back to the main key
        
        Args:
          cipher: The ciphertext to be decrypted.
          n: the number of rounds
        
        Returns:
          The decrypted message.
        """
        state = self.encode(cipher)

        state = self.addKey(state, self.round_keys[n])
        state = self.invShiftRows(state)
        state = self.invSubBytes(state)

        for i in range(n - 1, 0, -1):
            state = self.addKey(state, self.round_keys[i])
            state = self.invMixColumns(state)
            state = self.invShiftRows(state)
            state = self.invSubBytes(state)

        state = self.addKey(state, self.main_key)

        state = state.transpose().reshape(16)
        state = list(map(lambda a: hex(a)[2:].zfill(2), state))
        state = ''.join(state)
        return int(state, 16)