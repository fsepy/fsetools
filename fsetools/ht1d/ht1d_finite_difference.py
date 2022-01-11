# Sub-functions for 1D heat transfer code
# __main__ will main_args a non-linear 1D heat transfer analysis
# Danny Hopkin
# OFR Consultants
# 15/05/2019

#  Conversion from DegC to DegK

import numpy as np


def ISO834_ft(t):
    #  returns the ISO curve where t is [s]
    tmin = t / 60
    tiso = 345 * np.log10((8 * tmin) + 1) + 20
    return tiso


def Common_CtoK(T):
    # Returns Kelvin

    TK = T + 273
    return TK


#  Calculation of flux abosrbed by first element


def ONEDHT_QINC(TGAS, TSURF, EMIS, hc):
    # Get absorbed heat flux (in Watts)

    QRAD = (
            0.0000000567 * EMIS * ((Common_CtoK(TGAS) ** 4) - (Common_CtoK(TSURF) ** 4))
    )  # Radiation component
    QCONV = hc * (Common_CtoK(TGAS) - Common_CtoK(TSURF))  # Convective component
    QINC = QRAD + QCONV  # Sum components and return value
    return QINC


# Calculation of heat flux leaving unexposed element


def ONEDHT_QOUT(TSURF, TAMB, EMIS, hc):
    # Heat flux lost to ambient on unexposed face (in Watts)

    QRAD = (
            0.0000000567 * EMIS * ((Common_CtoK(TSURF) ** 4) - (Common_CtoK(TAMB) ** 4))
    )  # Radiation component
    QCONV = hc * (Common_CtoK(TSURF) - Common_CtoK(TAMB))  # Convective component
    QOUT = QRAD + QCONV  # Sum components and return value
    return QOUT


# Calculation of temperature of first element


def ONEDHT_ELEM1(Qinc, T1, T2, LAMDA1, LAMDA2, dx, dt, Cp, Rho):
    # Calculate temperature of first element given incoming flux Q1

    a1 = (2 * dt) / (Rho * Cp * dx)  # calculate diffusivity
    a2 = (LAMDA1 + LAMDA2) / 2  # calculate mean conductivity
    a3 = (T1 - T2) / dx  # Calculate temperature gradient

    dT1 = a1 * (Qinc - (a2 * a3))  # Calculate change in temperature in time step

    T1new = max(T1 + dT1, 20)  # Calculate new temperature

    return T1new


# Calculation of temperature for intermediate elements


def ONEDHT_ELEMJ(TJN1, TJ, TJP1, LAMDAJN1, LAMDAJ, LAMDAJP1, dx, dt, Cp, Rho):
    # Calculate temperature of element j, using temps for j-1 and j+1
    b1 = dt / (Rho * Cp * (dx ** 2))  # calculate diffusivity
    b2 = (LAMDAJN1 + LAMDAJ) / 2  # calculate mean conductivity1
    b3 = TJN1 - TJ  # Calculate delta T1
    b4 = (LAMDAJ + LAMDAJP1) / 2  # calculate mean conductivity2
    b5 = TJ - TJP1  # Calculate delta T2
    dTJ = b1 * ((b2 * b3) - (b4 * b5))  # Calculate change in temperature in time step
    Tjnew = TJ + dTJ  # Calculate new temperature
    return Tjnew


# Calculation of temperature of final element


def ONEDHT_ELEMF(Qout, TFN1, TF, LAMDAFN1, LAMDAF, dx, dt, Cp, Rho):
    # Calculate temperature of the final element

    c1 = (2 * dt) / (Rho * Cp * dx)  # calculate diffusivity
    c2 = (LAMDAFN1 + LAMDAF) / 2  # calculate mean conductivity
    c3 = (TFN1 - TF) / dx  # Calculate temperature gradient

    dTF = c1 * ((c2 * c3) - Qout)  # calculate change in temperature in time step
    Tfnew = TF + dTF  # calculate new temperature
    return Tfnew


import warnings


def c_steel_T(temperature):
    if temperature < 20:
        warnings.warn("Temperature ({:.1f} °C) is below 20 °C".format(temperature))
        return 425 + 0.773 * 20 - 1.69e-3 * np.power(20, 2) + 2.22e-6 * np.power(20, 3)
    if 20 <= temperature < 600:
        return (
                425
                + 0.773 * temperature
                - 1.69e-3 * np.power(temperature, 2)
                + 2.22e-6 * np.power(temperature, 3)
        )
    elif 600 <= temperature < 735:
        return 666 + 13002 / (738 - temperature)
    elif 735 <= temperature < 900:
        return 545 + 17820 / (temperature - 731)
    elif 900 <= temperature <= 1200:
        return 650
    elif temperature > 1200:
        warnings.warn(
            "Temperature ({:.1f} °C) is greater than 1200 °C".format(temperature)
        )
        return 650
    else:
        warnings.warn("Temperature ({:.1f} °C) is outside bound.".format(temperature))
        return 0


def k_steel_T(temperature):
    if temperature < 20:
        warnings.warn("Temperature ({:.1f} °C) is below 20 °C".format(temperature))
        return 54 - 3.33e-2 * 20
    if temperature < 800:
        return 54 - 3.33e-2 * temperature
    elif temperature <= 1200:
        return 27.3
    elif temperature > 1200:
        warnings.warn(
            "Temperature ({:.1f} °C) is greater than 1200 °C".format(temperature)
        )
        return 27.3
    else:
        warnings.warn("Temperature ({:.1f} °C) is outside bound.".format(temperature))
        return 0
