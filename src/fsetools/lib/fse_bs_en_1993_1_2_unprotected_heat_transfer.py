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
