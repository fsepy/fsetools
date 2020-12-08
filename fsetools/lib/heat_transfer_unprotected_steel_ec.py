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


def unprotected_steel_eurocode(
        time,
        temperature_ambient,
        perimeter_section,
        area_section,
        perimeter_box,
        density_steel,
        h_conv,
        emissivity_resultant,
):
    """
    SI UNITS FOR INPUTS AND OUTPUTS.
    :param time:
    :param temperature_ambient:
    :param perimeter_section:
    :param area_section:
    :param perimeter_box:
    :param density_steel:
    :param c_steel_T:
    :param h_conv:
    :param emissivity_resultant:
    :return:
    """

    # Create steel temperature change array s
    temperature_steel = np.zeros_like(time, dtype=np.float)

    # BS EN 1993-1-2:2005 (e4.26a)
    k_sh = 0.9 * (perimeter_box / area_section) / (perimeter_section / area_section)
    F = perimeter_section
    V = area_section
    rho_s = density_steel
    h_c = h_conv
    sigma = 56.7e-9
    epsilon = emissivity_resultant

    temperature_steel[0] = temperature_ambient[0]
    for i in range(1, len(time), 1):
        # BS EN 1993-1-2:2005 (e4.25)
        a = h_c * (temperature_ambient[i] - temperature_steel[i - 1])
        b = sigma * epsilon * (np.power(temperature_ambient[i], 4) - np.power(temperature_steel[i - 1], 4))
        c = k_sh * F / V / rho_s / c_steel_T(temperature_steel[i - 1])
        d = time[i] - time[i - 1]

        temperature_rate_steel = c * (a + b) * d
        temperature_steel[i] = temperature_steel[i - 1] + temperature_rate_steel

    return dict(temperature=temperature_steel)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    time = np.arange(0, 180 * 60, 1.)
    temperature_fire = (345.0 * np.log10((time / 60.0) * 8.0 + 1.0) + 20.0) + 273.15

    temperature_steel = unprotected_steel_eurocode(
        time=time,
        temperature_ambient=temperature_fire,
        perimeter_section=1.768,
        area_section=0.01408,
        perimeter_box=300 * 4 / 1000,
        density_steel=7850,
        h_conv=25.,
        emissivity_resultant=1.,
    )['temperature']

    plt.plot(time / 60, temperature_fire - 273.15)
    plt.plot(time / 60, temperature_steel - 273.15)
    plt.show()
