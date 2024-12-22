from ecdsa.ellipticcurve import Point
from ecdsa.curves import NIST256p

import matplotlib.pyplot as plt
import time

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
    
            "trunc": 16,
            "l": 256, # output bit length
}

class DualECDRBG():
    def __init__(self):
        self.curve = NIST256p.curve
        self.p = self.curve.p()
        
        self.P = Point(self.curve, nist_p256["G"][0], nist_p256["G"][1])
        self.Q = Point(self.curve, nist_p256["Q"][0], nist_p256["Q"][1])
        
        self.seed = 0x42
        
    def generate(self, n = 16, seed = None):
        if seed is None:
            seed = self.seed
        r = (seed * self.P).x()
        self.seed = (r * self.P).x()
        
        output = (r * self.Q).x()

        return self.truncate(output, n)
    
    def truncate(self, x, n = 16):
        if x.bit_length() <= n:
            return 0
        return x & (2 ** (nist_p256["l"] - n) - 1)
    
    def __call__(self, x):
        return (x ** 3 + nist_p256["a"] * x + nist_p256["b"]) % self.p
    
    
def square_root_exists(n, p):
    return pow(n, (p - 1) // 2, p) == 1

def square_root_mod_p(n, p):
    assert (p + 1) % 4 == 0, "p + 1 must be divisible by 4"
    assert square_root_exists(n, p), "n is not a quadratic residue"
    return pow(n, (p + 1) // 4, p)

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def mod_inverse(d, n):
    gcd, x, y = extended_gcd(d, n)
    if gcd != 1:
        raise ValueError("No modular inverse exists")
    return x % n

def find_possible_seeds(ec_curve, output, real_seed, e, n):
    possible_seeds = []
    for i in range(0, 2 ** n):
        x = i << (nist_p256["l"] - n) | output
        z = ec_curve(x)
        if not square_root_exists(z, ec_curve.p):
            continue
        y = square_root_mod_p(z, ec_curve.p)
        
        A = Point(ec_curve.curve, x, y)
        
        pred_seed = (e * A).x()
        possible_seeds.append(pred_seed)
        # if pred_seed == real_seed:
        #     possible_seeds.append(pred_seed)
        # pred_output = ec_curve.generate(n, pred_seed)
        # if pred_output == next_output:
        #     possible_seeds.append(pred_seed)

    return possible_seeds

def _main():
    fig, axs = plt.subplots(1, 1)
    decdrbg = DualECDRBG()
    
    P = decdrbg.P
    k = pow(69, 42, nist_p256["p"])
    k = 0x1234567890ABCDEF
    Q = k * P

    e = mod_inverse(k, nist_p256["n"])
    decdrbg.Q = Q
    
    assert e * Q == e * k * P == P

    print(f"Q_x = {hex(Q.x())}")
    print(f"Q_y = {hex(Q.y())}")
    
    decdrbg.seed = 0x42
    output = decdrbg.generate(16)
    print(f"Output: {hex(output)}")
    next_seed = decdrbg.seed
    print(f"Current Seed")
    print(hex(decdrbg.seed))
    pred_seed = find_possible_seeds(decdrbg, output, next_seed, e, 16)
    print(len(pred_seed))
    print(next_seed in pred_seed)        
    exit()
    
    max_trunc = 16
    times = []
    possible_seeds_size = []
    for i in range(max_trunc + 1):
        output = decdrbg.generate(i)
        real_seed = decdrbg.seed
        next_output = decdrbg.generate(i)

        t = time.time()
        possible_seeds = find_possible_seeds(decdrbg, output, real_seed, e, i)
        assert real_seed in possible_seeds, f"Real seed not found in possible seeds {possible_seeds}"
        times.append(time.time() - t)
        possible_seeds_size.append(len(possible_seeds))
        print(f"Truncation: {i} bits, found {len(possible_seeds)} possible seeds")
    
    fig, axs = plt.subplots(1, 1)
    axs.set_yscale("log")
    axs.plot(range(len(times)), times)
    axs.set_xlabel("Truncated Bits")
    axs.set_ylabel("Time (s)")
    
    fig.suptitle("Time taken to find possible seeds")
    fig.savefig("./images/time_find_seeds_dual_ec_drbg.png")

    plt.show()
        
    
if __name__ == "__main__":
    _main()