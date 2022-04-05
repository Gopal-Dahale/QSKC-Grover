import numpy as np


class SAES:

    def __init__(self, key):
        self.key = key
        self.sbox = np.array(
            [9, 4, 10, 11, 13, 1, 8, 5, 6, 2, 0, 3, 12, 14, 15, 7])
        self.inv_sbox = np.array(
            [10, 5, 9, 11, 1, 7, 8, 15, 6, 0, 2, 3, 13, 4, 13, 14])

        self.round_keys = self._generate_round_keys()
        self.round_constants = np.array(
            [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36])
        self.mix_col = np.array([[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3],
                                 [3, 1, 1, 2]])

    def _generate_round_keys(self):
        
        

    # def encrpyt(self, msg):
