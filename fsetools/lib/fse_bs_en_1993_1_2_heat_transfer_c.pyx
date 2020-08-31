# -*- coding: utf-8 -*-
import numpy as np


cdef double c_steel_T(double temperature):

    temperature -= 273.15
    if temperature < 20:
        # warnings.warn('Temperature ({:.1f} °C) is below 20 °C'.format(temperature))
        return 425 + 0.773 * 20 - 1.69e-3 * (400) + 2.22e-6 * (8000)
    if 20 <= temperature < 600:
        return (425 + 0.773 * temperature - 1.69e-3 * (temperature ** 2) + 2.22e-6 * (temperature ** 3))
    elif 600 <= temperature < 735:
        return 666 + 13002 / (738 - temperature)
    elif 735 <= temperature < 900:
        return 545 + 17820 / (temperature - 731)
    elif 900 <= temperature <= 1200:
        return 650
    elif temperature > 1200:
        return 650
    else:
        return 0


def protected_steel_eurocode(
        fire_time,
        double[:] fire_temperature,
        double beam_rho,
        double beam_cross_section_area,
        double protection_k,
        double protection_rho,
        double protection_c,
        double protection_thickness,
        double protection_protected_perimeter,
        bint terminate_when_cooling=False,
        double terminate_max_temperature=np.inf,
        *_,
        **__
):
    """
    SI UNITS!
    This function calculate the temperature curve of protected steel section based on BS EN 1993-1-2:2005, Section 4
    . Ambient (fire) time-temperature data must be given, as well as the parameters specified below.
    :param fire_time: ndarray, [s], time evolution.
    :param fire_temperature: ndarray, [K], imposed temperature evolution.
    :param beam_rho: float, [kg/m3], steel density.
    :param beam_cross_section_area: float, [m2], steel cross section area.
    :param protection_k: float, [K/kg/m], protection thermal conductivity.
    :param protection_rho: float, [kg/m3], protection density.
    :param protection_c: float, [J/K/kg], protection thermal capacity.
    :param protection_thickness: float, [m], protection thickness.
    :param protection_protected_perimeter: float, [m], protected perimeter.
    :param terminate_when_cooling: bool, [-], if True then terminate and return values when first peak steel
    temperature is observed.
    :return temperature_steel: ndarray, [K], is calculated steel temperature.
    """

    # todo: 4.2.5.2 (2) - thermal properties for the insulation material
    # todo: revise BS EN 1993-1-2:2005, Clauses 4.2.5.2

    # BS EN 1993-1-2:2005, 3.4.1.2
    # return self.__make_property("c")

    cdef double V = beam_cross_section_area
    cdef double rho_a = beam_rho
    cdef double lambda_p = protection_k
    cdef double rho_p = protection_rho
    cdef double d_p = protection_thickness
    cdef double A_p = protection_protected_perimeter
    cdef double c_p = protection_c

    cdef double[:] temperature_steel = fire_time * 0.0
    cdef double[:] temperature_rate_steel = fire_time * 0.0
    cdef double[:] specific_heat_steel = fire_time * 0.0

    # Check time step <= 30 seconds. [BS EN 1993-1-2:2005, Clauses 4.2.5.2 (3)]

    flag_heating_started = False

    temperature_steel[0] = fire_temperature[0]  # initially, steel temperature is equal to ambient
    cdef int i
    cdef double a, b, c, d, phi
    for i in range(fire_time.shape[0]-1):
        i += 1  # actual index since the first item had been skipped.

        T_g = fire_temperature[i]

        specific_heat_steel[i] = c_steel_T(temperature_steel[i - 1])

        # Steel temperature equations are from [BS EN 1993-1-2:2005, Clauses 4.2.5.2, Eq. 4.27]
        phi = (c_p * rho_p / specific_heat_steel[i] / rho_a) * d_p * A_p / V

        a = (lambda_p * A_p / V) / (d_p * specific_heat_steel[i] * rho_a)
        b = (T_g - temperature_steel[i - 1]) / (1.0 + phi / 3.0)
        c = (np.exp(phi / 10.0) - 1.0) * (T_g - fire_temperature[i - 1])
        d = fire_time[i] - fire_time[i - 1]

        temperature_rate_steel[i] = (a * b * d - c) / d  # deviated from e4.27, converted to rate [s-1]

        temperature_steel[i] = temperature_steel[i - 1] + temperature_rate_steel[i] * d

        if (temperature_rate_steel[i] > 0 and flag_heating_started is False) and fire_time[i] > 1800:
            flag_heating_started = True

        # Terminate steel temperature calculation if necessary
        if (
                terminate_when_cooling
                and flag_heating_started
                and temperature_rate_steel[i] < 0
        ):
            break
        elif flag_heating_started and terminate_max_temperature < temperature_steel[i]:
            break

        # NOTE: Steel temperature can be in cooling phase at the beginning of calculation, even the ambient temperature
        #       (fire) is hot. This is
        #       due to the factor 'phi' which intends to address the energy locked within the protection layer.
        #       The steel temperature is forced to be increased or remain as previous when ambient temperature and
        #       its previous temperature are all higher than the current calculated temperature.
        #       A better implementation is perhaps to use a 1-D heat transfer model.

        # DEPRECIATED 26 MAR 2019
        # if temperature_steel[i] < temperature_steel[i-1] or temperature_steel[i] < temperature_ambient[i]:
        #     temperature_rate_steel[i] = 0
        #     temperature_steel[i] = temperature_steel[i-1]

    return temperature_steel


def protected_steel_eurocode_max_temperature(
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
        double terminate_check_wait_time=3600,
        double terminate_max_temperature=np.inf,
):
    """
    LIMITATIONS:
    Constant time interval throughout
    Only one maxima

    SI UNITS!
    This function calculate the temperature curve of protected steel section based on BS EN 1993-1-2:2005, Section 4
    . Ambient (fire) time-temperature data must be given, as well as the parameters specified below.

    :param fire_time:                    {ndarray} [s]
    :param fire_temperature:     {ndarray} [K]
    :param beam_rho:               {float} [kg/m3]
    :param beam_cross_section_area:      {float} [m2]
    :param protection_k:            {float} [K/kg/m]
    :param protection_rho:          {float} [kg/m3]
    :param protection_c:            {float} [J/K/kg]
    :param protection_thickness:    {float} [m]
    :param protection_protected_perimeter:     {float} [m]
                                                            temperature is observed.
    :return time:                   {ndarray, float} [s]
    :return temperature_steel:      {ndarray, float} [K]
    :return data_all:               {Dict} [-]
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

    cdef bint flag_heating_started = False

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

        T += dT * d

        if not flag_heating_started:
            if fire_time[i] >= terminate_check_wait_time:
                if dT > 0:
                    flag_heating_started = True

        # Terminate early if maximum temperature is reached
        elif flag_heating_started:
            if T > terminate_max_temperature:
                break
            if dT < 0:
                T -= dT * d
                break
    return T


def _speed_test():

    rho = 7850
    t = np.arange(0, 700, 0.1)
    T = 345.0 * np.log10(t * 8.0 + 1.0) + 293.15

    list_dp = np.arange(0.0001, 0.01 + 0.002, 0.001)

    for d_p in list_dp:
        T_s = protected_steel_eurocode_max_temperature(
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
