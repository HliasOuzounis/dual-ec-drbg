from ecdsa.ellipticcurve import Point
from ecdsa.curves import NIST256p

import matplotlib.pyplot as plt

dual_ec_drbg = NIST256p

nist_p256 = {
            "p": 2**256 - 2**224 + 2**192 + 2**96 - 1,
            "a": -0x3,
            "b": 0x5ac635d8_aa3a93e7_b3ebbd55_769886bc_651d06b0_cc53b0f6_3bce3c3e_27d2604b,
            "G": (0x6b17d1f2_e12c4247_f8bce6e5_63a440f2_77037d81_2deb33a0_f4a13945_d898c296,
                  0x4fe342e2_fe1a7f9b_8ee7eb4a_7c0f9e16_2bce3357_6b315ece_cbb64068_37bf51f5),
            "Q": (0xc97445f4_5cdef9f0_d3e05e1e_585fc297_235b82b5_be8ff3ef_ca67c598_52018192,
                  0xb28ef557_ba31dfcb_dd21ac46_e2a91e3c_304f44cb_87058ada_2cb81515_1e610046),
            "n": 0xffffffff_00000000_ffffffff_ffffffff_bce6faad_a7179e84_f3b9cac2_fc632551,
            "h": 0x1,
}

class DualECDRBG():
    def __init__(self):
        self.curve = NIST256p.curve
        self.p = self.curve.p()
        
        self.P = Point(self.curve, nist_p256["G"][0], nist_p256["G"][1])
        self.Q = Point(self.curve, nist_p256["Q"][0], nist_p256["Q"][1])
        
        self.seed = 0x42
        
    def generate(self):
        r = (self.seed * self.P).x()
        self.seed = (r * self.P).x()
        
        output = (r * self.Q).x()

        return self.truncate(output)
    
    def truncate(self, x, n = 16):
        return x & (2 ** (x.bit_length() - n) - 1)

def _main():
    fig, axs = plt.subplots(1, 1)
    decdrbg = DualECDRBG()
    # for i in range(1000):
        # axs.scatter(x, (x ** 3 + a * x + b) % p, color='r')
        # print(decdrbg.generate())
    # plt.show()
    
if __name__ == "__main__":
    _main()