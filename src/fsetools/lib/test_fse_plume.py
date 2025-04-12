from .fse_plume import *


def test_1():
    pass


def test_2():
    import matplotlib.pyplot as plt
    plt.style.use("seaborn-v0_8")

    z = np.linspace(0.1, 10, 100)
    z_Q_c_factor = z / (1000 ** (2 / 5))
    delta_T = fire_plume_temperature_rise_centreline(1000, z, fire_plume_region(1000, z))

    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(5, 5))

    ax1.plot(z_Q_c_factor, delta_T)
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_yticks(range(100, 1001, 100))
    ax1.set_ylabel('dT [$^o$C]')
    ax1.set_xlabel('z/$Q_{c}$$^{2/5}$')
    ax1.grid()
    fig.show()


if __name__ == '__main__':
    test_1()
    test_2()
