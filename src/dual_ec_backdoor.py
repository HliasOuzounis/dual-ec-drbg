from ecdsa.ellipticcurve import Point, CurveFp
import random


ec_params = {
    "p": 10**9 + 7,
    "a": -3,
    "b": 123456789,
    "n": 1000008295,
    "trunc": 16,
    "l": 32, # output bit length
}

class MyEC():
    def __init__(self):
        self.a = ec_params["a"]
        self.b = ec_params["b"]
        self.prime = ec_params["p"]

        self.curve = CurveFp(ec_params["p"], ec_params["a"], ec_params["b"])
        
        self.seed = random.randint(0, ec_params["p"] - 1)
    
    def set_P(self, x, y):
        self.P = Point(self.curve, x, y)
    
    def set_Q(self, x, y):
        self.Q = Point(self.curve, x, y)
        
    def generate(self, seed = None):
        if seed is None:
            seed = self.seed
            
        r = (seed * self.P).x()
        self.seed = (r * self.P).x()
        
        output = (r * self.Q).x()

        return self.truncate(output, ec_params["trunc"])
    
    def truncate(self, x, n = ec_params["trunc"]):
        if x.bit_length() <= n:
            return 0
        return x & (2 ** (ec_params["l"] - n) - 1)
    
    def __call__(self, x):
        return (x ** 3 + self.a * x + self.b) % self.prime

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

def find_possible_seeds(ec_curve, output, next_output, e):
    possible_seeds = []
    for i in range(0, 2 ** ec_params["trunc"]):
        x = i << (ec_params["l"] - ec_params["trunc"]) | output
        z = ec_curve(x)
        if not square_root_exists(z, ec_curve.prime):
            continue
        y = square_root_mod_p(z, ec_curve.prime)
        
        A = Point(ec_curve.curve, x, y)

        pred_seed = (e * A).x()
        
        pred_output = ec_curve.generate(pred_seed)
        if pred_output == next_output:
            possible_seeds.append(pred_seed)
    

def main():
    global ec_params
    my_ec = MyEC()
    
    gx = 31415926 # first 9 digits of pi
    gy = square_root_mod_p(gx**3 + ec_params["a"] * gx + ec_params["b"], ec_params["p"])
    
    my_ec.set_P(gx, gy)

    # d = pow(42, 42, my_ec.prime)
    d = 42 * 69 * 111 % my_ec.prime
    e = mod_inverse(d, ec_params["n"])
    
    Q = d * my_ec.P
    my_ec.set_Q(Q.x(), Q.y())

    assert e * Q == my_ec.P
    
    for i in range(20):
        ec_params["trunc"] = i

        output = my_ec.generate()
        real_seed = my_ec.seed
        next_output = my_ec.generate()

        predicted_seeds = find_possible_seeds(my_ec, output, next_output, e)

        print(f"Truncation: {ec_params['trunc']}")
        print(f"Possible seeds: {predicted_seeds}")
        print(f"Real seed: {real_seed}")
        
if __name__ == "__main__":
    main()