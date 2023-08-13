import numpy as np

from fsetools.lib.fse_bs_en_1991_1_2_parametric_fire import temperature as param_temp
from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer import temperature
from fsetools.lib.fse_travelling_fire import temperature_si as trav_temp


def __trav_fire(t: np.ndarray):
    return trav_temp(
        t=t,
        T_0=273.15,
        q_f_d=600e6,
        hrrpua=0.25e6,
        l=100,
        w=16,
        s=0.012,
        e_h=3,
        e_l=50,
        T_max=1050 + 273.15,
    )


def __param_fire(t: np.ndarray):
    return param_temp(
        t=t,
        A_t=963.5,
        A_f=340,
        A_v=20,
        h_eq=2,
        q_fd=420e6,
        lbd=720 ** 2,
        rho=1,
        c=1,
        t_lim=0.333,
    )


def __param_fire_2(t: np.ndarray):
    return param_temp(
        t=t,
        A_t=1283.5,
        A_f=500,
        A_v=115.2,
        h_eq=2,
        q_fd=336e6,
        lbd=720 ** 2,
        rho=1,
        c=1,
        t_lim=0.333,
    )


def __test_heat_transfer_kwargs(t, T):
    return dict(
        fire_time=t,
        fire_temperature=T,
        beam_rho=7850.,
        beam_cross_section_area=0.017,
        protection_k=0.2,
        protection_rho=800.,
        protection_c=1700.,
        protection_thickness=0.01,
        protection_protected_perimeter=2.14,
    )


def test_temperature_trav():
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    # --------------------------------------------------
    # Check if the Cython version returns the same value
    # --------------------------------------------------
    fig, ax = plt.subplots()
    t = np.arange(0, 210 * 60, 5)
    kwargs = dict(**__test_heat_transfer_kwargs(t, __trav_fire(t)))

    list_dp = np.linspace(0.0001, 0.1000, 10)

    for d_p in list_dp:
        kwargs['protection_thickness'] = d_p
        T = temperature(**kwargs)
        ax.plot(t / 60, T - 273.15, c='k')

    ax.grid(ls='--', c='k', linewidth=0.5)
    lines = [Line2D([0], [0], color='k'), Line2D([0], [0], color='r', linestyle='--')]
    labels = ['temperature', 'temperature_c']
    ax.legend(lines, labels).set_visible(True)
    plt.show()


def test_temperature_param():
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    # --------------------------------------------------
    # Check if the Cython version returns the same value
    # --------------------------------------------------
    fig, ax = plt.subplots()
    t = np.arange(0, 210 * 60, 5)
    kwargs = dict(**__test_heat_transfer_kwargs(t, __param_fire(t)))

    list_dp = np.arange(0.0001, 0.05 + 0.002, 0.001)

    for d_p in list_dp:
        kwargs['protection_thickness'] = d_p
        T = temperature(**kwargs)
        ax.plot(t / 60, T - 273.15, c='k')

    ax.grid(ls='--', c='k', linewidth=0.5)
    lines = [Line2D([0], [0], color='k'), Line2D([0], [0], color='r', linestyle='--')]
    labels = ['temperature', 'temperature_c']
    ax.legend(lines, labels).set_visible(True)
    plt.show()


def test_temperature_param_2():
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    # --------------------------------------------------
    # Check if the Cython version returns the same value
    # --------------------------------------------------
    fig, ax = plt.subplots()
    t = np.arange(0, 210 * 60, 5)
    kwargs = dict(**__test_heat_transfer_kwargs(t, __param_fire_2(t)))

    list_dp = np.arange(0.0001, 0.05 + 0.002, 0.001)

    for d_p in list_dp:
        kwargs['protection_thickness'] = d_p
        T = temperature(**kwargs)
        # print(temperature_max(**kwargs), np.amax(T_c))
        ax.plot(t / 60, T - 273.15, c='k')

    ax.grid(ls='--', c='k', linewidth=0.5)
    lines = [Line2D([0], [0], color='k'), Line2D([0], [0], color='r', linestyle='--')]
    labels = ['temperature', 'temperature_c']
    ax.legend(lines, labels).set_visible(True)
    plt.show()


def test_temperature_extreme():
    import matplotlib.pyplot as plt

    t = np.arange(0, 210 * 60, 1, dtype=float)
    kwargs = __test_heat_transfer_kwargs(t, __param_fire(t))

    fig, ax1 = plt.subplots()

    for protection_thickness in np.linspace(0.5, 0.0001, 10):
        kwargs['protection_thickness'] = protection_thickness
        T_a = temperature(**kwargs)
        ax1.plot(t / 60, T_a, label=f'd_p {protection_thickness * 1000:<4.0f} mm')
    ax1.legend().set_visible(True)
    ax1.set_xlabel('Time [$min$]')
    ax1.set_ylabel('Steel temperature [$K$]')

    fig.show()
