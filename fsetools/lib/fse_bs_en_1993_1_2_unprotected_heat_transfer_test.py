import numpy as np

from fsetools.lib.fse_bs_en_1993_1_2_unprotected_heat_transfer import temperature


def test():
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

    t = 30
    print(f'Steel temperature at {t} minutes is {np.amax(temperature_steel[time <= t * 60]) - 273.15} deg.C')
