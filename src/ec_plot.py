import numpy as np
import matplotlib.pyplot as plt

def elliptic_curve_1(x):
    a = -6
    b = 5
    return (x ** 3 + a * x + b) ** 0.5

def elliptic_curve_2(x):
    a = -5
    b = 8
    return (x ** 3 + a * x + b) ** 0.5

def plot_eq(elliptic_curve_1, elliptic_curve_2):
    x = np.linspace(-8, 8, 100000)

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    fig.suptitle("Elliptic Curves")

    axs[0].plot(x, elliptic_curve_1(x), color='black')
    axs[0].plot(x, -elliptic_curve_1(x), color='black')

    axs[0].set_xlim(-8, 8)
    axs[0].set_ylim(-8, 8)
    axs[0].set_ylabel("y")
    axs[0].set_xlabel("x")

    axs[0].set_title("y^2 = x^3 - 6x + 5")

    axs[0].plot(x, np.zeros_like(x), color='black', linestyle='--')

    axs[1].plot(x, elliptic_curve_2(x), color='black')
    axs[1].plot(x, -elliptic_curve_2(x), color='black')

    axs[1].set_xlim(-8, 8)
    axs[1].set_ylim(-8, 8)
    axs[1].set_ylabel("y")
    axs[1].set_xlabel("x")

    axs[1].set_title("y^2 = x^3 - 5x + 8")

    axs[1].plot(x, np.zeros_like(x), color='black', linestyle='--')

    fig.savefig("./images/elliptic-curves.png")

    plt.show()

def plot_point_addition():
    x = np.linspace(-8, 8, 100000)

    fig, axs = plt.subplots(1, 1, figsize=(10, 8))

    axs.plot(x, elliptic_curve_2(x), color='black', linewidth=3)
    axs.plot(x, -elliptic_curve_2(x), color='black', linewidth=3)

    axs.set_xlim(-8, 8)
    axs.set_ylim(-8, 8)
    axs.set_ylabel("y")
    axs.set_xlabel("x")
    
    px = -2.65
    py = elliptic_curve_2(px)
    
    qx = 0.5
    qy = elliptic_curve_2(qx)
    
    m = (qy - py) / (qx - px)
    axs.plot(x, m * (x - px) + py, color='red')

    rx = m ** 2 - px - qx
    ry = m * (rx - px) + py
    
    axs.plot((rx, rx), (ry, -ry), color='purple', linestyle='--')
    
    axs.scatter(px, py, color='blue', label='P', s=150, zorder=10)
    axs.scatter(qx, qy, color='orange', label='Q', s=150, zorder=10)
    axs.scatter(rx, ry, color='purple', s=150, zorder=10, facecolors='none', linewidths=3, label='-R')

    ry = -ry
    axs.scatter(rx, ry, color='purple', label='R', s=150, zorder=10)

    axs.legend()
    fig.savefig("./images/point-addition.png")

    plt.show()
    
def plot_point_at_infinity():
    x = np.linspace(-8, 8, 100000)

    fig, axs = plt.subplots(1, 1, figsize=(10, 8))

    axs.plot(x, elliptic_curve_2(x), color='black', linewidth=3)
    axs.plot(x, -elliptic_curve_2(x), color='black', linewidth=3)

    axs.set_xlim(-8, 8)
    axs.set_ylim(-8, 8)
    axs.set_ylabel("y")
    axs.set_xlabel("x")
    
    px = 0.5
    py = elliptic_curve_2(px)
    
    qx = 0.5
    qy = -py
    
    axs.plot((px, px), (-8, 8), color='red')
    
    axs.scatter(px, py, color='blue', label='P', s=150, zorder=10)
    axs.scatter(qx, qy, color='orange', label='Q', s=150, zorder=10)

    axs.legend()
    fig.savefig("./images/point-at-infinity.png")

    plt.show()
    
def plot_point_doubling():
    x = np.linspace(-8, 8, 100000)

    fig, axs = plt.subplots(1, 1, figsize=(10, 8))

    axs.plot(x, elliptic_curve_2(x), color='black', linewidth=3)
    axs.plot(x, -elliptic_curve_2(x), color='black', linewidth=3)

    axs.set_xlim(-8, 8)
    axs.set_ylim(-8, 8)
    axs.set_ylabel("y")
    axs.set_xlabel("x")
    
    px = -1
    py = elliptic_curve_2(px)
    
    m = (3 * px ** 2 - 5) / (2 * py)
    axs.plot(x, m * (x - px) + py, color='red')

    rx = m ** 2 - 2 * px
    ry = m * (rx - px) + py
    
    axs.plot((rx, rx), (ry, -ry), color='purple', linestyle='--')
    
    axs.scatter(px, py, color='blue', label='P', s=150, zorder=10)
    axs.scatter(rx, ry, color='purple', s=150, zorder=10, facecolors='none', linewidths=3, label='-R')

    ry = -ry
    axs.scatter(rx, ry, color='purple', label='R', s=150, zorder=10)

    axs.legend()
    fig.savefig("./images/point-doubling.png")

    plt.show()
    

def main():
    ...
    # plot_eq()
    # plot_point_addition()
    # plot_point_at_infinity()
    # plot_point_doubling()

if __name__ == "__main__":
    main()