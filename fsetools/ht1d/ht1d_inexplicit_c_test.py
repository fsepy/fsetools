import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from scipy.interpolate import interp1d

from fsetools.ht1d.ht1d_inexplicit_c import main as main_c


def test_inexplicit_c():
    T_solved = main_c(
        n_nodes=21,
        T_init=20,
        tol=1e-3,
        t_end=7200,
        dt=5,
        dx=0.005,
        T_boundary_0=interp1d([0, 3600, 7200], [20, 1200, 20], bounds_error=False),
        k=0.12,
        rho=600,
        c=1500,
    )

    l = np.linspace(0, (21 - 1) * 0.005, 21, dtype=float)
    t = np.arange(0, 7200. + 5. / 2., 5., dtype=float)

    # fig, ax = plt.subplots()
    # for T in T_solved[::100]:
    #     ax.plot(l, T)

    xx, yy = np.meshgrid(t / 60., l)
    zz = T_solved.T
    fig_1, ax_1 = plt.subplots()
    csf = ax_1.contourf(xx, yy, zz, cmap=cm.get_cmap('viridis'))
    fig_1.colorbar(csf, ax=ax_1, shrink=0.9)
    ax_1.set_xlabel('Time'), ax_1.set_ylabel('Depth')

    plt.show()


test_inexplicit_c()
