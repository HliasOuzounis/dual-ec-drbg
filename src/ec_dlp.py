from sage.all import *
import matplotlib.pyplot as plt
import time as t

ec_params = {
    "a": 1,
    "b": 7,
}

def find_e(P, Q):
    e = 1
    while e * P != Q:
        e += 1
        if e * P == P:
            return None
    return e

def generate_primes(n):
    primes = []
    for i in range(2, n):
        is_prime = True
        for j in range(2, i):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes

def main():
    primes = generate_primes(10**6)
    p_list = []
    times = []
    for p in primes[10:]:
        i = 0
        total_time = 0
        E = EllipticCurve(GF(p), [1, 10])
        
        reps = 1
        while i < reps:
            P = E.random_point()
            Q = E.random_point()
            
            t0 = t.time()
            e = find_e(P, Q)
            if e is None:
                continue
            i += 1
            total_time += t.time() - t0

        p_list.append(p)
        times.append(total_time / i)
        print(p, total_time / i)

    plt.plot(p_list, times)
    plt.savefig("ec_dlp.png")

if __name__ == "__main__":
    main()