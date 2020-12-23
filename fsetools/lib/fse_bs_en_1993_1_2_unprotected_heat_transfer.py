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
        fire_time: np.ndarray,
        fire_temperature: np.ndarray,
        member_section_perimeter: float,
        member_section_area: float,
        member_perimeter_box: float,
        member_density: float = 7850.,
        h_conv: float = 25.,
        emissivity_resultant: float = 1.,
):
    """
    SI UNITS FOR ALL INPUTS AND OUTPUTS.
    :param fire_time:
    :param fire_temperature:
    :param member_section_perimeter:
    :param member_section_area:
    :param member_perimeter_box:
    :param member_density:
    :param c_steel_T:
    :param h_conv:
    :param emissivity_resultant:
    :return:
    """

    # Create steel temperature change array s
    temperature_steel = np.zeros_like(fire_time, dtype=np.float)

    # BS EN 1993-1-2:2005 (e4.26a)
    k_sh = 0.9 * (member_perimeter_box / member_section_area) / (member_section_perimeter / member_section_area)
    F = member_section_perimeter
    V = member_section_area
    rho_s = member_density
    h_c = h_conv
    sigma = 56.7e-9
    epsilon = emissivity_resultant

    temperature_steel[0] = fire_temperature[0]
    for i in range(1, len(fire_time), 1):
        # BS EN 1993-1-2:2005 (e4.25)
        a = h_c * (fire_temperature[i] - temperature_steel[i - 1])
        b = sigma * epsilon * (np.power(fire_temperature[i], 4) - np.power(temperature_steel[i - 1], 4))
        c = k_sh * F / V / rho_s / c_steel_T(temperature_steel[i - 1])
        d = fire_time[i] - fire_time[i - 1]

        temperature_rate_steel = c * (a + b) * d
        temperature_steel[i] = temperature_steel[i - 1] + temperature_rate_steel

    return dict(temperature=temperature_steel)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    time = np.arange(0, 180 * 60, 1.)
    temperature_fire = (345.0 * np.log10((time / 60.0) * 8.0 + 1.0) + 20.0) + 273.15

    temperature_steel = temperature(
        fire_time=time,
        fire_temperature=temperature_fire,
        member_section_perimeter=1.768,
        member_section_area=0.01408,
        member_perimeter_box=300 * 4 / 1000,
        member_density=7850,
        h_conv=25.,
        emissivity_resultant=1.,
    )['temperature']

    plt.plot(time / 60, temperature_fire - 273.15)
    plt.plot(time / 60, temperature_steel - 273.15)
    plt.show()
