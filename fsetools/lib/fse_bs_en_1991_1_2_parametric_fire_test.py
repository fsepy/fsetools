import numpy as np

from fsetools.lib.fse_bs_en_1991_1_2_parametric_fire import *


def test_1():
    """
    Verify against Figure 7, Section 1.2.2 in Holicky, M. et al [1].
    Yan Fu, 1st Oct 2018
    Updated by Yan Fu, 18th Mar 2022

    REFERENCES
    [1] Holicky, M., Meterna, A., Sedlacek, G. and Schleich, J.B., 2005. Implementation of eurocodes, handbook 5, design
    of buildings for the fire situation. Leonardo da Vinci Pilot Project: Luxembourg.
    """

    import copy

    # Verification data obtained from [1]
    t = (20, 30, 40, 50, 60, 70, 80)
    Ts = [(689.1109391, 782.7282474, 167.4009827, 20, 20, 20, 20),
          (689.1109391, 782.7317977, 402.4756096, 20, 20, 20, 20),
          (689.1109391, 782.7317977, 508.8188932, 236.7716603, 20, 20, 20),
          (843.9616854, 946.9144525, 781.2034026, 540.8761379, 304.2731159, 69.53931579, 20),
          (741.3497451, 827.5114674, 885.6845648, 818.8612125, 692.3328174, 565.8079725, 441.145249),
          (601.424372, 726.7651987, 777.4756096, 813.2641976, 843.4522203, 780.3602113, 719.1303236),
          (269.3348197, 430.1234077, 533.0726245, 604.3089737, 651.2880412, 685.2109576, 709.8019654), ]

    # prepare inputs
    kws = dict(A_t=360, A_f=100, h_eq=1, q_fd=600e6, lbd=1, rho=1, c=2250000, t_lim=20 * 60,
               t=np.arange(0, 2 * 60 * 60 + 1, 1), T_0=293.15, )

    # define opening area
    A_v_list = [72, 50.4, 36.00001, 32.4, 21.6, 14.4, 7.2]

    # calculate fire curves
    x1_list, y1_list = list(), list()
    for i in A_v_list:
        y = temperature(A_v=i, **copy.copy(kws))
        x = np.arange(0, 2 * 60 * 60 + 1, 1) + 10 * 60
        x1_list.append(x / 60)
        y1_list.append(y - 273.15)

    from scipy.interpolate import interp1d

    for i in range(len(A_v_list)):
        assert np.allclose(Ts[i], interp1d(x1_list[i], y1_list[i])(t), atol=10)

    return x1_list, y1_list, t, Ts


def plot_test_1():
    x1_list, y1_list, t, Ts = test_1()
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(7, 1)
    for i, ax in enumerate(axes):
        ax.plot(x1_list[i], y1_list[i], label='Result')
        ax.scatter(t, Ts[i], label='Benchmark')
    plt.show()


if __name__ == '__main__':
    test_1()
    plot_test_1()
