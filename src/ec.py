from ecdsa.ellipticcurve import Point, CurveFp, INFINITY
import matplotlib.pyplot as plt

ec_params = {
    "p": 103,
    "a": -1,
    "b": 6,
}

class MyEC():
    def __init__(self):
        self.a = ec_params["a"]
        self.b = ec_params["b"]
        self.prime = ec_params["p"]

        self.curve = CurveFp(ec_params["p"], ec_params["a"], ec_params["b"])
    
    def calc_order(self):
        self.order = 1 # point at infinity
        for x in range(self.prime):
            for y in range(self.prime):
                if (y ** 2) % self.prime == self(x):
                    self.order += 1
        return self.order
    
    def point_order(self, P):
        order = 1
        Q = P
        while Q != INFINITY:
            Q = Q + P
            order += 1
        return order
    
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
    

def main():
    my_ec = MyEC()
    print(my_ec.calc_order())
    
    px, py = 22, 34
    P = Point(my_ec.curve, px, py)
    print(my_ec.point_order(P))
    
    fig, axs = plt.subplots(1, 1, figsize=(8, 6))
    for i in range(my_ec.point_order(P)):
        Q = i * P
        axs.scatter(Q.x(), Q.y(), color='r')
        
    axs.plot((0, my_ec.prime), [(my_ec.prime - 1) // 2] * 2, 'b--')
    axs.set_ylabel("y")
    axs.set_xlabel("x")
    
    fig.suptitle("y^2 = x^3 - x + 6 mod 103")
    fig.savefig("./images/ec.png")
    
    fig.suptitle('')

    axs.scatter(P.x(), P.y(), color='g', s=100)
    for i in range(1, 7):
        Q1 = i * P
        Q2 = (i + 1) * P
        plt.annotate('', xy=(Q2.x(), Q2.y()), xytext=(Q1.x(), Q1.y()),
                     arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->', lw=2))
        axs.scatter(Q2.x(), Q2.y(), color='b')   
    fig.savefig("./images/ec-arrow.png")
    
    plt.show()
    
        
if __name__ == "__main__":
    main()