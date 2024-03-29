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
        return 666 + 13002 / (738 - T)
    elif 735 <= T < 900:
        return 545 + 17820 / (T - 731)
    elif 900 <= T <= 1200:
        return 650
    elif T > 1200:
        return 650


def temperature(
        fire_time,
        fire_temperature,
        beam_rho,
        beam_cross_section_area,
        protection_k,
        protection_rho,
        protection_c,
        protection_thickness,
        protection_protected_perimeter,
        *_,
        **__
):
    """
    SI UNITS!
    Function calculates the maximum steel temperature for a protected steel member based upon BS EN 1993-1-2.

    PARAMETERS:
    :param fire_time:                       Time array [s]
    :param T_g:                Gas temperature array [K]
    :param beam_rho:                        Steel beam density [kg/m3]
    :param beam_cross_section_area:         Steel beam cross sectional area [m2]
    :param protection_k:                    Protection thermal conductivity [K/kg/m]
    :param protection_rho:                  Protection density [kg/m3]
    :param protection_c:                    Protection specific heat capacity [J/K/kg]
    :param protection_thickness:            Protection layer thickness [m]
    :param protection_protected_perimeter:  Protection protected perimeter (of the steel beam section) [m]
    :return:                                Steel beam temperature array [K]
    """

    # todo: 4.2.5.2 (2) - thermal properties for the insulation material
    # todo: revise BS EN 1993-1-2:2005, Clauses 4.2.5.2

    T_g = fire_temperature
    V = beam_cross_section_area
    rho_a = beam_rho
    lambda_p = protection_k
    rho_p = protection_rho
    d_p = protection_thickness
    A_p = protection_protected_perimeter
    c_p = protection_c

    T_a = np.zeros_like(fire_time, dtype=np.float32)
    dT_a = np.zeros_like(fire_time, dtype=np.float32)
    c_a = np.zeros_like(fire_time, dtype=np.float32)

    # Check time step <= 30 seconds. [BS EN 1993-1-2:2005, Clauses 4.2.5.2 (3)]

    # the following parameters are used for debug purposes
    is_debug = False
    if is_debug:
        phi_, a_, b_, c_, d_ = [np.zeros_like(fire_time, dtype=np.float16) for i in range(5)]

    T_a[0] = T_g[0]  # initially, steel temperature is equal to ambient
    for i in range(1, len(fire_time)):
        c_a[i] = c_steel_T(T_a[i - 1])

        # Steel temperature equations are from [BS EN 1993-1-2:2005, Clauses 4.2.5.2, Eq. 4.27]
        # This a ratio of heat stored in the protection
        phi = (c_p * rho_p / c_a[i] / rho_a) * d_p * A_p / V

        a = (lambda_p * A_p / V) / (d_p * c_a[i] * rho_a)
        b = (T_g[i] - T_a[i - 1]) / (1.0 + phi / 3.)
        c = (2.718 ** (phi / 10.0) - 1.0) * (T_g[i] - T_g[i - 1])
        d = fire_time[i] - fire_time[i - 1]

        if is_debug:
            phi_[i] = phi
            a_[i] = a
            b_[i] = b
            c_[i] = c
            d_[i] = d

        dT_a[i] = (a * b * d - c) / d  # deviated from e4.27, converted to rate [s-1]
        if dT_a[i] < 0 < (T_g[i] - T_g[i - 1]):
            dT_a[i] = 0

        T_a[i] = T_a[i - 1] + dT_a[i] * d

        # NOTE: Steel temperature can be in cooling phase at the beginning of calculation, even the ambient temperature
        #       (fire) is hot. This is
        #       due to the factor 'phi' which intends to address the energy locked within the protection layer.
        #       The steel temperature is forced to be increased or remain as previous when ambient temperature and
        #       its previous temperature are all higher than the current calculated temperature.
        #       A better implementation is perhaps to use a 1-D heat transfer model.

    if is_debug:
        try:
            import pandas as pd
            data = pd.DataFrame.from_dict(dict(
                T_g=T_g,
                T_a=T_a,
                dT_a=dT_a,
                phi=phi_,
                a=a_,
                b=b_,
                c=c_,
                d=d_,
                c_a=c_a
            ))
        except:
            data = None

    return T_a


def temperature_max(
        fire_time,
        fire_temperature,
        beam_rho,
        beam_cross_section_area,
        protection_k,
        protection_rho,
        protection_c,
        protection_thickness,
        protection_protected_perimeter,
):
    """
    SI UNITS!
    Function calculates the maximum steel temperature for a protected steel member based upon BS EN 1993-1-2.

    LIMITATIONS:
        1. Constant time interval in `fire_time` throughout;
        2. `fire_temperature` has *one* maxima.

    PARAMETERS:
    :param fire_time:                       Time array [s]
    :param fire_temperature:                Gas temperature array [K]
    :param beam_rho:                        Steel beam density [kg/m3]
    :param beam_cross_section_area:         Steel beam cross sectional area [m2]
    :param protection_k:                    Protection thermal conductivity [K/kg/m]
    :param protection_rho:                  Protection density [kg/m3]
    :param protection_c:                    Protection specific heat capacity [J/K/kg]
    :param protection_thickness:            Protection layer thickness [m]
    :param protection_protected_perimeter:  Protection protected perimeter (of the steel beam section) [m]
    :return:                                Steel beam temperature array [K]
    """

    # todo: 4.2.5.2 (2) - thermal properties for the insulation material
    # todo: revise BS EN 1993-1-2:2005, Clauses 4.2.5.2

    V = beam_cross_section_area
    rho_a = beam_rho
    lambda_p = protection_k
    rho_p = protection_rho
    d_p = protection_thickness
    A_p = protection_protected_perimeter
    c_p = protection_c

    T = fire_temperature[0]  # current steel temperature
    d = fire_time[1] - fire_time[0]

    for i in range(1, len(fire_temperature)):

        T_g = fire_temperature[i]

        c_s = c_steel_T(T)

        # Steel temperature equations are from [BS EN 1993-1-2:2005, Clauses 4.2.5.2, Eq. 4.27]
        phi = (c_p * rho_p / c_s / rho_a) * d_p * A_p / V

        a = (lambda_p * A_p / V) / (d_p * c_s * rho_a)
        b = (T_g - T) / (1.0 + phi / 3.0)
        c = (2.718 ** (phi / 10.0) - 1.0) * (T_g - fire_temperature[i - 1])

        dT = (a * b * d - c) / d  # deviated from e4.27, converted to rate [s-1]
        if dT < 0 < (T_g - fire_temperature[i - 1]):
            dT = 0

        T = T + dT * d

        # Terminate early if maximum temperature is reached
        if dT < 0:
            T -= dT * d
            break
    return T
