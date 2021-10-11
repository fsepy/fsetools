# -*- coding: utf-8 -*-
import numpy as np


def c_steel_T(T):
    # BS EN 1993-1-2:2005, 3.4.1.2
    T -= 273.15
    if T < 20:
        return 425 + 0.773 * 20 - 1.69e-3 * 400 + 2.22e-6 * 8000
    if 20 <= T < 600:
        return 425 + 0.773 * T - 1.69e-3 * T ** 2 + 2.22e-6 * T ** 3
    elif 600 <= T < 735:
        return 666. + 13002. / (738. - T)
    elif 735 <= T < 900:
        return 545. + 17820. / (T - 731.)
    elif 900 <= T <= 1200:
        return 650.
    elif T > 1200:
        return 650.


def temperature(
        t: np.ndarray,
        T_g: np.ndarray,
        k_sh: float,
        A_m: float,
        V: float,
        epsilon_m: float,  # Section 2.2 (2), 0.7 for carbon, 0.4 for stainless
        alpha_c: float = 25.,
        rho_a: float = 7850.,
):
    """
    BS EN 1993-1-2 4.2.5
    SI UNITS FOR ALL INPUTS AND OUTPUTS.

    :param fire_time:
    :param T_g:
    :param A_m:
    :param V:
    :param member_perimeter_box:
    :param rho_a:
    :param c_steel_T:
    :param h_net_d:
    :param epsilon:
    :return:
    """

    # Create steel temperature change array s
    T_a = np.zeros_like(t, dtype=float)

    sigma = 56.7e-9
    epsilon_f = 1.0  # Section 4.2.5.1 (3)
    Phi = 1.0  # Assumed, should be 1.0 within a fire compartment

    T_a[0] = T_g[0]
    for i in range(1, len(t), 1):
        # h_net_d defined in BS EN 1991-1-2 Section 3.1, Equation 3.1
        # h_net = h_net_c + h_net_r
        # h_net_c = alpha_c * (T_g - T_m)
        # h_net_r = Phi * epsilon_m * epsilon_f * sigma * (T_g ** 4 - T_m ** 4)
        h_net_c = alpha_c * (T_g[i] - T_a[i - 1])
        h_net_r = Phi * epsilon_m * epsilon_f * sigma * (T_g[i] ** 4 - T_a[i - 1] ** 4)
        h_net_d = h_net_c + h_net_r

        # BS EN 1993-1-2:2005 (e4.25)
        const = (A_m / V) / rho_a / c_steel_T(T_a[i - 1])
        dt = t[i] - t[i - 1]

        T_a_i = k_sh * const * h_net_d * dt
        T_a[i] = T_a[i - 1] + T_a_i

    return dict(T_a=T_a)


def _test():
    import matplotlib.pyplot as plt
    plt.style.use('seaborn-paper')

    time = np.arange(0, 180 * 60, 1.)
    temperature_fire = (345.0 * np.log10((time / 60.0) * 8.0 + 1.0) + 20.0) + 273.15

    temperature_steel = temperature(
        t=time,
        T_g=temperature_fire,
        k_sh=1.0,
        A_m=1.768,
        V=0.01408,
        rho_a=7850,
        alpha_c=25.,
        epsilon_m=0.7
    )['T_a']

    fig, ax = plt.subplots(figsize=(3.5, 3.5))

    ax.plot(time / 60, temperature_fire - 273.15, label='ISO 834')
    ax.plot(time / 60, temperature_steel - 273.15, label='Steel')
    ax.set_xlim(0, 180)
    ax.set_xticks(range(0, 181, 30))
    ax.set_xlabel('Time [min]')
    ax.set_ylim(0, 1200.)
    ax.set_yticks(range(0, 1201, 200))
    ax.set_ylabel('Temperature [$^oC$]')
    ax.legend().set_visible(True)
    ax.grid(which='both', c='k', ls='--')
    fig.tight_layout()
    t = 30
    print(f'Steel temperature at {t} minutes is {np.amax(temperature_steel[time <= t * 60]) - 273.15} deg.C')
    plt.show()


if __name__ == '__main__':
    _test()
