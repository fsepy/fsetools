# -*- coding: utf-8 -*-
import numpy as np


cdef double c_steel_T(double T):

    T = T - 273.15
    if T < 20:
        # warnings.warn('Temperature ({:.1f} °C) is below 20 °C'.format(temperature))
        return 425 + 0.773 * 20 - 1.69e-3 * 400 + 2.22e-6 * 8000
    if 20 <= T < 600:
        return 425 + 0.773 * T - 1.69e-3 * (T ** 2) + 2.22e-6 * (T ** 3)
    elif 600 <= T < 735:
        return 666 + 13002 / (738 - T)
    elif 735 <= T < 900:
        return 545 + 17820 / (T - 731)
    elif 900 <= T <= 1200:
        return 650
    elif T > 1200:
        return 650
    else:
        return 0


def temperature(
        *,
        fire_time,
        double[:] fire_temperature,
        double beam_rho,
        double beam_cross_section_area,
        double protection_k,
        double protection_rho,
        double protection_c,
        double protection_thickness,
        double protection_protected_perimeter,
        **__
):
    """
    SI UNITS!
    Function calculates the steel temperature for a protected steel member based upon BS EN 1993-1-2.

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

    # BS EN 1993-1-2:2005, 3.4.1.2

    cdef double V = beam_cross_section_area
    cdef double rho_a = beam_rho
    cdef double lambda_p = protection_k
    cdef double rho_p = protection_rho
    cdef double d_p = protection_thickness
    cdef double A_p = protection_protected_perimeter
    cdef double c_p = protection_c

    cdef double[:] T_a = fire_time * 0.0

    # Check time step <= 30 seconds. [BS EN 1993-1-2:2005, Clauses 4.2.5.2 (3)]

    T_a[0] = fire_temperature[0]  # initially, steel temperature is equal to ambient
    cdef int i
    cdef double a, b, c, d, phi, c_s, T_g, dT
    for i in range(1, len(fire_time)):

        T_g = fire_temperature[i]

        c_s = c_steel_T(T_a[i - 1])

        # Steel temperature equations are from [BS EN 1993-1-2:2005, Clauses 4.2.5.2, Eq. 4.27]
        phi = (c_p * rho_p / c_s / rho_a) * d_p * A_p / V

        a = (lambda_p * A_p / V) / (d_p * c_s * rho_a)
        b = (T_g - T_a[i - 1]) / (1.0 + phi / 3.0)
        c = (2.718 ** (phi / 10.0) - 1.0) * (T_g - fire_temperature[i - 1])
        d = fire_time[i] - fire_time[i - 1]

        dT = (a * b * d - c) / d  # deviated from e4.27, converted to rate [s-1]
        if dT < 0 < (T_g - fire_temperature[i - 1]):
            dT = 0

        T_a[i] = T_a[i - 1] + dT * d

        # NOTE: Steel temperature can be in cooling phase at the beginning of calculation, even the ambient temperature
        #       (fire) is hot. This is
        #       due to the factor 'phi' which intends to address the energy locked within the protection layer.
        #       The steel temperature is forced to be increased or remain as previous when ambient temperature and
        #       its previous temperature are all higher than the current calculated temperature.
        #       A better implementation is perhaps to use a 1-D heat transfer model.

    return np.array(T_a)


cpdef tuple temperature_max(
        double[:] fire_time,
        double[:] fire_temperature,
        double beam_rho,
        double beam_cross_section_area,
        double protection_k,
        double protection_rho,
        double protection_c,
        double protection_thickness,
        double protection_protected_perimeter,
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

    cdef double V = beam_cross_section_area
    cdef double rho_a = beam_rho
    cdef double lambda_p = protection_k
    cdef double rho_p = protection_rho
    cdef double d_p = protection_thickness
    cdef double A_p = protection_protected_perimeter
    cdef double c_p = protection_c

    cdef double T = fire_temperature[0]  # current steel temperature
    cdef double d = fire_time[1] - fire_time[0]

    cdef int i
    cdef double T_g, c_s, phi, a, b, c, dT
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

        if dT < 0:
            break

    return T, fire_time[i-1]


def protection_thickness(
        *,
        double[:] fire_time,
        double[:] fire_temperature,
        double beam_rho,
        double beam_cross_section_area,
        double protection_k,
        double protection_rho,
        double protection_c,
        double protection_protected_perimeter,
        double solver_temperature_goal,
        double solver_temperature_goal_tol,
        int solver_max_iter = 20,
        double d_p_1 = 0.0001,
        double d_p_2 = 0.0300,
):
    """
    SI UNITS!
    To solve the protection thickness for the max. steel temperature, `T_a_max`, is within a predefined range:

        - `T_a_max_goal ± T_a_max_goal_tol`;
        - `T_a_max` is the max. steel temperature;
        - `T_a_max_goal` is a given max. steel temperature goal;
        - `T_a_max_goal_tol` is solver tolerance.

    The steel max. temperature is solved based upon BS EN 1993-1-2 for the given `fire_time` and `fire_temperature`.

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
    :param protection_protected_perimeter:  Protection protected perimeter (of the steel beam section) [m]
    :param solver_temperature_goal:         The max. steel temperature to be solved for [K]
    :param solver_temperature_goal_tol:     Tolerance of the max. steel temperature to be solved for [K]
    :param d_p_1:                           Protection thickness upper bound [m]
    :param d_p_2:                           Protection thickness lower bound [m]
    :return:                                (d_p, T_a_max, t, solver_iter_count)
                                            `d_p`               is the solved protection thickness [m]
                                            `T_a_max`           is the solved maximum steel temperature [K]
                                            `t`                 is the time when maximum steel temperature occurred [s]
                                            `solver_iter_count` is the solver iteration count

    """

    # todo: 4.2.5.2 (2) - thermal properties for the insulation material
    # todo: revise BS EN 1993-1-2:2005, Clauses 4.2.5.2

    cdef double V = beam_cross_section_area
    cdef double rho_a = beam_rho
    cdef double lambda_p = protection_k
    cdef double rho_p = protection_rho
    cdef double A_p = protection_protected_perimeter
    cdef double c_p = protection_c

    cdef double d = fire_time[1] - fire_time[0]

    cdef int i
    cdef int solver_iter_count = 0
    cdef bint flag_heating_started = False
    cdef bint solver_convergence_status = False
    cdef double t, T_g, c_s, phi, a, b, c, dT, d_p_3, T, T_1, T_2, T_3

    # -------------------------------
    # Solve maximum steel temperature
    # -------------------------------

    T_a_max_1, t = temperature_max(
            fire_time=fire_time,
            fire_temperature=fire_temperature,
            beam_rho=beam_rho,
            beam_cross_section_area=beam_cross_section_area,
            protection_k=protection_k,
            protection_rho=protection_rho,
            protection_c=protection_c,
            protection_thickness=d_p_1,
            protection_protected_perimeter=protection_protected_perimeter,
        )

    T_a_max_2, t = temperature_max(
            fire_time=fire_time,
            fire_temperature=fire_temperature,
            beam_rho=beam_rho,
            beam_cross_section_area=beam_cross_section_area,
            protection_k=protection_k,
            protection_rho=protection_rho,
            protection_c=protection_c,
            protection_thickness=d_p_2,
            protection_protected_perimeter=protection_protected_perimeter,
        )

    if T_a_max_1 < solver_temperature_goal + solver_temperature_goal_tol:
        return -np.inf, T_a_max_1, t, solver_iter_count
    if T_a_max_2 > solver_temperature_goal - solver_temperature_goal_tol:
        return np.inf, T_a_max_2, t, solver_iter_count

    cdef double d_p = (d_p_1+d_p_2) / 2 + ((np.random.rand() - 0.5) * 1e-5)  # initial

    while True:
        T, t = temperature_max(
            fire_time=fire_time,
            fire_temperature=fire_temperature,
            beam_rho=beam_rho,
            beam_cross_section_area=beam_cross_section_area,
            protection_k=protection_k,
            protection_rho=protection_rho,
            protection_c=protection_c,
            protection_thickness=d_p,
            protection_protected_perimeter=protection_protected_perimeter,
        )

        # ---------------------------
        # Adjust protection thickness
        # ---------------------------

        if solver_iter_count <= solver_max_iter:
            if T <= solver_temperature_goal - solver_temperature_goal_tol:
                # steel temperature is too low, decrease thickness
                d_p_2 = d_p
            elif T >= solver_temperature_goal + solver_temperature_goal_tol:
                # steel temperature is too high, increase thickness
                d_p_1 = d_p
            else:
                return d_p, T, t, solver_iter_count

            d_p = (d_p_1 + d_p_2) / 2
        else:
            return np.nan, np.nan, np.nan, np.nan

        solver_iter_count += 1
