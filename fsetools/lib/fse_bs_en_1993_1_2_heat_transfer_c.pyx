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
    Calculate the time dependent temperature of a protected steel section based upon Section 4 in BS EN 1993-1-2:2005.

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

    cdef double[:] temperature_steel = fire_time * 0.0

    # Check time step <= 30 seconds. [BS EN 1993-1-2:2005, Clauses 4.2.5.2 (3)]

    temperature_steel[0] = fire_temperature[0]  # initially, steel temperature is equal to ambient
    cdef int i
    cdef double a, b, c, d, phi, c_s, T_g, temperature_rate_steel
    for i in range(fire_time.shape[0]-1):
        i += 1  # actual index since the first item had been skipped.

        T_g = fire_temperature[i]

        c_s = c_steel_T(temperature_steel[i - 1])

        # Steel temperature equations are from [BS EN 1993-1-2:2005, Clauses 4.2.5.2, Eq. 4.27]
        phi = (c_p * rho_p / c_s / rho_a) * d_p * A_p / V

        a = (lambda_p * A_p / V) / (d_p * c_s * rho_a)
        b = (T_g - temperature_steel[i - 1]) / (1.0 + phi / 3.0)
        c = (np.exp(phi / 10.0) - 1.0) * (T_g - fire_temperature[i - 1])
        d = fire_time[i] - fire_time[i - 1]

        temperature_rate_steel = (a * b * d - c) / d  # deviated from e4.27, converted to rate [s-1]
        if temperature_rate_steel < 0 < (T_g - fire_temperature[i - 1]):
            temperature_rate_steel = 0

        temperature_steel[i] = temperature_steel[i - 1] + temperature_rate_steel * d

        # NOTE: Steel temperature can be in cooling phase at the beginning of calculation, even the ambient temperature
        #       (fire) is hot. This is
        #       due to the factor 'phi' which intends to address the energy locked within the protection layer.
        #       The steel temperature is forced to be increased or remain as previous when ambient temperature and
        #       its previous temperature are all higher than the current calculated temperature.
        #       A better implementation is perhaps to use a 1-D heat transfer model.

    return np.array(temperature_steel)


def temperature_max(
        *,
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
    LIMITATIONS:
        - Fixed time interval throughout.
        - Single maxima.

    SI UNITS!
    This function calculate the temperature curve of protected steel section based on BS EN 1993-1-2:2005, Section 4
    . Ambient (temperature) time-temperature data must be given, as well as the parameters specified below.

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
        c = (np.exp(phi / 10.0) - 1.0) * (T_g - fire_temperature[i - 1])

        dT = (a * b * d - c) / d  # deviated from e4.27, converted to rate [s-1]
        if dT < 0 < (T_g - fire_temperature[i - 1]):
            dT = 0

        T = T + dT * d

        if dT < 0:
            return T

    return T


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
    :return:                                (d_p, T_a_max)
                                                `d_p`         is the solved protection thickness [m]
                                                `T_a_max`     is the solved maximum steel temperature [K]
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
    cdef double T_g, c_s, phi, a, b, c, dT, d_p_3, T, T_1, T_2, T_3

    cdef double d_p = 0.0001  # initial
    cdef double d_p_1 = 0.0001
    cdef double d_p_2 = 0.21

    # -------------------------------
    # Solve maximum steel temperature
    # -------------------------------
    while True:
        T = fire_temperature[0]
        for i in range(1, len(fire_temperature)):
            T_g = fire_temperature[i]
            c_s = c_steel_T(T)
            # Steel temperature equations are from [BS EN 1993-1-2:2005, Clauses 4.2.5.2, Eq. 4.27]
            phi = (c_p * rho_p / c_s / rho_a) * d_p * A_p / V
            a = (lambda_p * A_p / V) / (d_p * c_s * rho_a)
            b = (T_g - T) / (1.0 + phi / 3.0)
            c = (np.exp(phi / 10.0) - 1.0) * (T_g - fire_temperature[i - 1])
            dT = (a * b * d - c) / d  # deviated from e4.27, converted to rate [s-1]
            if dT < 0 < (T_g - fire_temperature[i - 1]):
                dT = 0
            T += dT * d
            # Terminate if maximum temperature is reached
            if dT < 0:
                T -= dT * d
                break

        # ---------------------------
        # Adjust protection thickness
        # ---------------------------
        if solver_iter_count == 0:
            if T < solver_temperature_goal + solver_temperature_goal_tol:
                return -np.inf, T
        elif solver_iter_count == 1:
            if T > solver_temperature_goal - solver_temperature_goal_tol:
                return np.inf, T

        if solver_iter_count <= 20:
            if T <= solver_temperature_goal - solver_temperature_goal_tol:
                # steel temperature is too low, decrease thickness
                d_p_2 = d_p
            elif T >= solver_temperature_goal + solver_temperature_goal_tol:
                # steel temperature is too high, increase thickness
                d_p_1 = d_p
            else:
                return d_p, T

            d_p = (d_p_1 + d_p_2) / 2
        else:
            return np.nan, np.nan
        # -------------------------------
        # End adjust protection thickness
        # -------------------------------
        solver_iter_count += 1


def _speed_test():

    rho = 7850
    t = np.arange(0, 700, 0.1)
    T = 345.0 * np.log10(t * 8.0 + 1.0) + 293.15

    list_dp = np.arange(0.0001, 0.01 + 0.002, 0.001)

    for d_p in list_dp:
        T_s = temperature_max(
            fire_time=t,
            fire_temperature=T,
            beam_rho=rho,
            beam_cross_section_area=0.017,
            protection_k=0.2,
            protection_rho=800,
            protection_c=1700,
            protection_thickness=d_p,
            protection_protected_perimeter=2.14,
        )


if __name__ == "__main__":
    import timeit
    print(timeit.timeit(_speed_test, number=10))
