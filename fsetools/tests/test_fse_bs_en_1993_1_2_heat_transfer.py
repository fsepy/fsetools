import numpy as np
from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c import protection_thickness as protection_thickness_c
from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c import temperature as temperature_c
from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c import temperature_max as temperature_max_c

from fsetools.lib.fse_bs_en_1991_1_2_parametric_fire import temperature as param_temp
from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer import temperature
from fsetools.lib.fse_travelling_fire import temperature_si as trav_temp


def __trav_fire(t: np.ndarray):
    return trav_temp(
        t=t,
        T_0=273.15,
        q_fd=600e6,
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
        lambda_=720 ** 2,
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
        lambda_=720 ** 2,
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
        T_c = temperature_c(**kwargs)
        ax.plot(t / 60, T - 273.15, c='k')
        ax.plot(t / 60, T_c - 273.15, c='r', ls='--')
        assert np.allclose(T, T_c, rtol=1.e-4)  # Assertion

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
        T_c = temperature_c(**kwargs)
        ax.plot(t / 60, T - 273.15, c='k')
        ax.plot(t / 60, T_c - 273.15, c='r', ls='--')
        assert np.allclose(T, T_c, rtol=1.e-4)  # Assertion

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
        T_c = temperature_c(**kwargs)
        # print(temperature_max(**kwargs), np.amax(T_c))
        ax.plot(t / 60, T - 273.15, c='k')
        ax.plot(t / 60, T_c - 273.15, c='r', ls='--')
        assert np.allclose(T, T_c, rtol=1.e-4)  # check if the two function return the same

    ax.grid(ls='--', c='k', linewidth=0.5)
    lines = [Line2D([0], [0], color='k'), Line2D([0], [0], color='r', linestyle='--')]
    labels = ['temperature', 'temperature_c']
    ax.legend(lines, labels).set_visible(True)
    plt.show()


def test_temperature_extreme():
    import matplotlib.pyplot as plt

    t = np.arange(0, 210 * 60, 1, dtype=np.float)
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


def test_protection_thickness_c():
    import matplotlib.pyplot as plt

    t = np.arange(0, 210 * 60, 1, dtype=np.float)
    kwargs = __test_heat_transfer_kwargs(t, __trav_fire(t))
    kwargs.pop('protection_thickness')
    kwargs['solver_temperature_goal'] = 873.15 + 20
    kwargs['solver_temperature_goal_tol'] = 0.1

    solver_d_p, solver_T_a_max, _, _ = protection_thickness_c(**kwargs)

    print(
        f'Solved protection thickness   {solver_d_p:<8.4} mm\n'
        f'Solved max. steel temperature {solver_T_a_max - 273.15:<8.2f} °C'
    )

    assert abs(solver_T_a_max - (873.15 + 20)) <= 0.1
    assert abs(solver_d_p - 0.01556) <= 1e-5  # based on a solution on 05/10/2020

    kwargs_check = __test_heat_transfer_kwargs(t, __trav_fire(t))
    kwargs_check['protection_thickness'] = solver_d_p
    T_c = temperature_c(**kwargs_check)
    assert abs(np.amax(T_c) - solver_T_a_max) < 1e-3

    fig, ax = plt.subplots()
    ax.plot(t, __trav_fire(t), label='Gas temperature')
    ax.plot(t, T_c, label='Steel temperature')
    ax.axhline(solver_T_a_max, ls='--', color='k', label=f'Steel temp. at d_p={solver_d_p:.4} mm')
    ax.legend().set_visible(True)
    fig.show()


def test_protection_thickness_c_extreme():
    import matplotlib.pyplot as plt

    t = np.arange(0, 210 * 60, 1, dtype=np.float)
    kwargs = __test_heat_transfer_kwargs(t, __param_fire_2(t))

    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    list_d_p, list_T_a_max = np.linspace(0.0001, 0.5, 100), list()

    for protection_thickness in np.linspace(0.0001, 0.5, 10):
        kwargs['protection_thickness'] = protection_thickness
        T_a = temperature_c(**kwargs)
        ax1.plot(t / 60, T_a, label=f'd_p {protection_thickness * 1000:<4.0f} mm')
    ax1.legend().set_visible(True)
    ax1.set_xlabel('Time [$min$]')
    ax1.set_ylabel('Steel temperature [$K$]')

    for protection_thickness in list_d_p:
        kwargs['protection_thickness'] = protection_thickness
        T_a_max, t = temperature_max_c(**kwargs)
        list_T_a_max.append(T_a_max)
    ax2.plot(list_d_p * 1000, list_T_a_max)
    ax2.set_xlabel('d_p [$mm$]')

    fig.show()


if __name__ == '__main__':
    test_temperature_trav()
    test_temperature_param()
    test_temperature_param_2()
    test_protection_thickness_c()
    test_protection_thickness_c_extreme()
    test_temperature_extreme()
