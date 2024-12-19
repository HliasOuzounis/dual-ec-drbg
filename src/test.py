from ecdsa.ellipticcurve import Point, CurveFp
import matplotlib.pyplot as plt

my_ec_curve = {
    "p": 103,
    "a": -0x3,
    "b": 1,
}

class MyEC():
    def __init__(self):
        self.a = my_ec_curve["a"]
        self.b = my_ec_curve["b"]
        self.prime = my_ec_curve["p"]

        self.curve = CurveFp(my_ec_curve["p"], my_ec_curve["a"], my_ec_curve["b"])
        
        self.seed = 0xdeadbeef
    
    def set_P(self, x, y):
        self.P = Point(self.curve, x, y)
    
    def set_Q(self, x, y):
        self.Q = Point(self.curve, x, y)
        
    def generate(self):
        r = (self.seed * self.P).x()
        self.seed = (r * self.P).x()
        
        output = (r * self.Q).x()

        return self.truncate(output)
    
    def truncate(self, x, n = 16):
        return x & (2 ** (x.bit_length() - n) - 1)
    
    def __call__(self, x):
        return (x ** 3 + self.a * x + self.b) % self.prime

def square_root_mod_p(n, p):
    assert (p + 1) % 4 == 0, "p + 1 must be divisible by 4"
    assert pow(n, (p - 1) // 2, p) == 1, "n is not a quadratic residue"
    return pow(n, (p + 1) // 4, p)


def main():
    my_ec = MyEC()
    
    gx = 3 # first 8 digits of pi
    gy = square_root_mod_p(gx**3 + my_ec_curve["a"] * gx + my_ec_curve["b"], my_ec_curve["p"])
    
    my_ec.set_P(gx, gy)

    e = pow(42, 69, my_ec.prime)
    Q = e * my_ec.P
    my_ec.set_Q(Q.x(), Q.y())
    
    fig, axs = plt.subplots(1, 1)
    
    P = my_ec.P
    points = [i * P for i in range(my_ec.prime)]
    axs.scatter([p.x() for p in points], [p.y() for p in points], color='r')
    plt.show()
        
        
if __name__ == "__main__":
    main()