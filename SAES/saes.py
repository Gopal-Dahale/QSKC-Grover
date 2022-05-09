import numpy as np


class SAES:

    def __init__(self, key):
        self.key = key
        self.sbox = np.array(
            [9, 4, 10, 11, 13, 1, 8, 5, 6, 2, 0, 3, 12, 14, 15, 7])
        self.inv_sbox = np.array(
            [10, 5, 9, 11, 1, 7, 8, 15, 6, 0, 2, 3, 12, 4, 13, 14])

        self.rcon = [0x40, 0x80, 0x30, 0x60, 0xc0, 0xb0, 0x50, 0x90]
        self.round_keys = self.__generate_round_keys()

        self.mix_col = np.array([[1, 4], [4, 1]])
        self.inv_mix_col = np.array([[9, 2], [2, 9]])

    def __rot_nibbles(self, x):
        """
        It rotates the nibbles of a byte
        
        Args:
          x: The value to rotate.
        
        Returns:
          the value of the left shifted 4 bits and the right shifted 4 bits.
        """
        return ((x << 4) & 0xf0) | ((x >> 4) & 0x0f)

    def __generate_round_keys(self):
        """
        The function takes the key and generates the round keys
        
        Returns:
          The subkeys are being returned.
        """

        K = [0] * 2 * len(self.rcon)
        B0 = self.key >> 8
        B1 = self.key & 0xff
        K[0] = B0
        K[1] = B1

        for i in range(2, 2 * len(self.rcon)):
            if i & 1 == 0:
                rot_nibbles = self.__rot_nibbles(K[i - 1])
                upper_nibble = self.sbox[(rot_nibbles >> 4) & 0x0f]
                lower_nibble = self.sbox[rot_nibbles & (0x0f)]
                nibble = (upper_nibble << 4 | lower_nibble)
                K[i] = (K[i - 2] ^ nibble ^ self.rcon[i // 2])
            else:
                K[i] = (K[i - 2] ^ K[i - 1])

        subkeys = []
        for i in range(0, 2 * len(self.rcon), 2):
            subkeys.append(self.__encode(K[i] << 8 | K[i + 1]))

        return subkeys

    def __add_round_key(self, state, round_key):
        """
        The function takes the state and the round key as input, and returns the state after the round
        key has been added
        
        Args:
          state: the current state of the cipher
          round_key: The round key for the current round.
        
        Returns:
          The state is being returned.
        """
        return np.bitwise_xor(state, round_key)

    def __sub_nibbles(self, state):
        """
        It takes a 4x4 matrix and returns a 4x4 matrix where each element is the result of the sbox
        function applied to the corresponding element in the original matrix
        
        Args:
          state: The current state of the cipher.
        
        Returns:
          The return value is a numpy array of the same shape as the input state.
        """
        return np.array([[self.sbox[j] for j in i] for i in state])

    def __inv_sub_nibbles(self, state):
        return np.array([[self.inv_sbox[j] for j in i] for i in state])

    def __shift_rows(self, state):
        return np.array([[state[0][0], state[0][1]], [state[1][1],
                                                      state[1][0]]])

    def __inv_shift_rows(self, state):
        return np.array([[state[0][0], state[0][1]], [state[1][1],
                                                      state[1][0]]])

    def __mix_col(self, state):
        res = np.zeros((2, 2)).astype(int)
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    res[i][j] ^= self.__galoisMult(self.mix_col[i][k],
                                                   state[k][j])
        return res

    def __inv_mix_col(self, state):
        res = np.zeros((2, 2)).astype(int)
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    res[i][j] ^= self.__galoisMult(self.inv_mix_col[i][k],
                                                   state[k][j])
        return res

    def __encode(self, msg):
        mat = np.zeros((2, 2)).astype(int)
        mat[0][0] = (msg >> 12 & 0xf)
        mat[1][0] = (msg >> 8 & 0xf)
        mat[0][1] = (msg >> 4 & 0xf)
        mat[1][1] = (msg & 0xf)
        return mat

    # helper function to perform galois field multiplication
    def __galoisMult(self, b, a):
        p = 0
        hiBitSet = 0
        for i in range(4):
            if b & 1 == 1:
                p ^= a
            a <<= 1
            hiBitSet = a & 0x10
            if hiBitSet:
                a ^= 0x13
            b >>= 1
        return p

    def encrpyt(self, msg, n):
        state = self.__encode(msg)
        state = self.__add_round_key(state, self.round_keys[0])

        for i in range(1, n):
            state = self.__sub_nibbles(state)
            state = self.__shift_rows(state)
            state = self.__mix_col(state)
            state = self.__add_round_key(state, self.round_keys[i])
        state = self.__sub_nibbles(state)
        state = self.__shift_rows(state)
        state = self.__add_round_key(state, self.round_keys[n])

        # Matrix to integer
        return (state[0][0] << 12) | (state[1][0] << 8) | (
            state[0][1] << 4) | state[1][1]

    def decrypt(self, msg, n):
        state = self.__encode(msg)
        state = self.__add_round_key(state, self.round_keys[n])
        state = self.__inv_shift_rows(state)
        state = self.__inv_sub_nibbles(state)

        for i in range(n - 1, 0, -1):
            state = self.__add_round_key(state, self.round_keys[i])
            state = self.__inv_mix_col(state)
            state = self.__inv_shift_rows(state)
            state = self.__inv_sub_nibbles(state)

        state = self.__add_round_key(state, self.round_keys[0])
        # Matrix to integer
        return (state[0][0] << 12) | (state[1][0] << 8) | (
            state[0][1] << 4) | state[1][1]


