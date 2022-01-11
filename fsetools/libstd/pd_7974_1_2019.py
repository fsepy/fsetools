"""
All SI UNITS unless specified.
"""
import typing

import numpy as np


def eq_5_dimensionless_hrr(
        Q_dot_kW: float,
        rho_0: float,
        c_p_0_kJ_kg_K: float,
        T_0: float,
        g: float,
        D: float,
) -> float:
    """Equation 5 in Section 8.3.2.2 PD 7974-1:2019 calculates dimensionless for rectangular fire source.

    :param Q_dot_kW: in kW, fire heat release rate.
    :param rho_0: in kg/m^3, density of ambient air.
    :param c_p_0_kJ_kg_K: in kJ/kg/K, specific heat capacity of ambient air.
    :param T_0: in K, ambient air temperature.
    :param g: in m/s^2, acceleration due to gravity.
    :param D: in m, diameter.
    :return Q_dot_star: dimensionless, dimensionless heat release rate.
    """

    # equation starts
    aa = Q_dot_kW
    bb = rho_0 * c_p_0_kJ_kg_K * T_0 * (g ** 0.5) * (D ** (5 / 2))
    Q_dot_star = aa / bb

    return Q_dot_star




def eq_11_dimensionless_hrr_rectangular(
        Q_dot_kW: float,
        rho_0: float,
        c_p_0_kJ_kg_K: float,
        T_0: float,
        g: float,
        L_A: float,
        L_B: float
) -> float:
    """Equation 11 in Section 8.3.2.2 PD 7974-1:2019 calculates dimensionless for rectangular fire source.

    :param Q_dot_kW: in kW, fire heat release rate.
    :param rho_0: in kg/m^3, density of ambient air.
    :param c_p_0_kJ_kg_K: in kJ/kg/K, specific heat capacity of ambient air.
    :param T_0: in K, ambient air temperature.
    :param g: in m/s^2, acceleration due to gravity.
    :param L_A: in m, rectangular shape dimension's shorter edge.
    :param L_B: in m, rectangular shape dimension's longer edge.
    :return Q_dot_star_rect: dimensionless, dimensionless heat release rate
    """

    # equation starts
    aa = Q_dot_kW
    bb = rho_0 * c_p_0_kJ_kg_K * T_0 * (g ** 0.5) * (L_A ** 1.5) * L_B
    Q_dot_star_rect = aa / bb

    return Q_dot_star_rect




def eq_12_dimensionless_hrr_line(
        Q_dot_l_kW_m: float,
        rho_0: float,
        c_p_0_kJ_kg_K: float,
        T_0: float,
        g: float,
        L_A: float,
) -> float:
    """Equation 12 in Section 8.3.2.2 PD 7974-1:2019 calculates dimensionless heat release rate for line fire source.
    Note dimension ratio should be less than 0.4 (i.e. L_A / L_B) to use line fire source correlation.

    :param Q_dot_l_kW_m: in kW/m, fire heat release rate per unit length along the line.
    :param rho_0: in kg/m^3, density of ambient air.
    :param c_p_0_kJ_kg_K: in kJ/kg/K, specific heat capacity of ambient air.
    :param T_0: in K, ambient air temperature.
    :param g: in m/s^2, acceleration due to gravity.
    :param L_A: in m, length of line shaped fire source.
    :return Q_dot_star_rect: dimensionless, dimensionless heat release rate
    """

    # equation starts
    aa = Q_dot_l_kW_m
    bb = rho_0 * c_p_0_kJ_kg_K * T_0 * (g ** 0.5) * (L_A ** 1.5)
    Q_dot_star_line = aa / bb

    return Q_dot_star_line




def eq_10_virtual_origin(D: float, Q_dot_kW: float):
    """Equation 10 in Section 8.3.1 PD 7974-1:2019 calculates virtual fire origin.

    :param D: in m, fire diameter.
    :param Q_dot_kW: in kW, fire heat release rate.
    :return z_0: in m, fire's virtual origin.
    """

    z_0 = -1.02 * D + 0.083 * Q_dot_kW ** (2 / 5)

    return z_0




def eq_14_plume_temperature(
        T_0: float,
        g: float,
        c_p_0_kJ_kg_K: float,
        rho_0: float,
        Q_dot_c_kW: float,
        z: float,
        z_0: float,
):
    """Equation 14 in Section 8.3.3 PD 7974-1:2019 calculates mean gas temperature along fire centre-line.

    :param T_0: in K, ambient air temperature.
    :param g: in m/s^2, acceleration due to gravity.
    :param c_p_0_kJ_kg_K: in kJ/kg/K, specific heat capacity of ambient air.
    :param rho_0: in kg/m^3, density of ambient air.
    :param Q_dot_c_kW: in kW, convective heat release rate.
    :param z: in m, height above fuel surface.
    :param z_0: in m, virtual fire origin.
    :return theta_bar_cl: in K, mean centre-line excess gas temperature.
    """

    # intermediate parameters
    aa = (T_0 / (g * c_p_0_kJ_kg_K ** 2 * rho_0 ** 2)) ** (1 / 3)
    bb = Q_dot_c_kW ** (2 / 3)
    cc = (z - z_0) ** (-5 / 3)

    # calculate the temperature
    theta_bar_cl = 9.1 * aa * bb * cc

    return theta_bar_cl




def eq_15_plume_velocity(
        T_0: float,
        g: float,
        c_p_0_kJ_kg_K: float,
        rho_0: float,
        Q_dot_c_kW: float,
        z: float,
        z_0: float,
):
    """Equation 15 in Section 8.3.3 PD 7974-1:2019 calculates mean gas velocity along fire centre-line.

    :param T_0: in K, ambient air temperature.
    :param g: in m/s^2, acceleration due to gravity.
    :param c_p_0_kJ_kg_K: in kJ/kg/K, specific heat capacity of ambient air.
    :param rho_0: in kg/m^3, density of ambient air.
    :param Q_dot_c_kW: in kW, convective heat release rate.
    :param z: in m, height above fuel surface.
    :param z_0: in m, virtual fire origin.
    :return u_bar_cl: in m/s, mean gas velocity of plume.
    """

    # intermediate parameters
    aa = (g / (c_p_0_kJ_kg_K * rho_0 * T_0)) ** (1 / 3)
    bb = Q_dot_c_kW ** (1 / 3)
    cc = (z - z_0) ** (-1 / 3)

    # calculate the temperature
    u_bar_cl = 3.4 * aa * bb * cc

    # check
    return u_bar_cl




def eq_22_t_squared_fire_growth(
        alpha: float,
        t: typing.Union[np.ndarray, float],
        t_i: float = 0,
        n: float = 2
) -> typing.Union[np.ndarray, float]:
    """Equation 22 in Section 8.4.1 PD 7974-1:2019 calculates t-square fire growth heat release rate.

    :param alpha: in kW/m^2.
        slow        0.0029
        medium      0.0117
        fast        0.0469
        ultra-fast  0.1876
    :param t: in s, current time.
    :param t_i: in s, initial time, default is 0.
    :param n: fire growth power, default is 2, only use 3 for racked storage.
    :return Q_dot_kW: in W, calculated heat release rate.
    """

    Q_dot = alpha * (t - t_i) ** n

    return Q_dot * 1e3




def eq_55_activation_of_heat_detector_device(
        u: float,
        RTI: float,
        Delta_T_g: float,
        Delta_T_e: float,
        C: float
) -> float:
    """Equation 55 in Section 8.9 PD 7974-1:2019 calculates the heat detectors temperature rise.

    PARAMETERS:
    :param u: m/s, velocity of gases in proximity to heat sensing element.
    :param RTI: (m s)^0.5, response time index of heat sensing element.
    :param Delta_T_g:   deg.C, change in gas temperature. (this is the gas temperature above ambient, i.e.
                        Delta_T_g = T_g - T_0)
    :param C: (m/s)^0.5, conduction factor (delay factor?)
    :param Delta_T_e: deg.C, change in temperature of heat sensing element.
    :return dTe_dt: 

    INDICATIVE NOTES
    Tsui and Spearpoint [37] quote C factors in the range of 0.33 – 0.65 (m/s)^0.5 depending upon the response type.
    RTI values are given in the literature, e.g. [38]. The rated temperature, permitting calculation of ΔTe, can be
    found in the relevant manufacturer’s specifications.

    REFERENCES
    [37]    TSUI A. and SPEARPOINT M. J. Variability of sprinkler response time index and conduction factor using the
            plunge test. Building Services Engineering Research and Technology, 31 (2) pp. 163–176, 2010.
            DOI:10.1177/0143624410363064.
    [36]    HESKESTAD G. and BILL R. Quantification of thermal responsiveness of automatic sprinklers including
            conduction effects. Fire Safety Journal, 14 (1-2) pp. 113–125, 1988.

    """

    aa = u ** 0.5 / RTI
    bb = Delta_T_g - Delta_T_e * (1 + C / u ** 0.5)

    dTe_dt = aa * bb

    return dTe_dt




def eq_26_axisymmetric_ceiling_jet_temperature(
        Q_dot_c_kW: float,
        z_H: float,
        z_0: float,
        r: float,
):
    """Equation 26 in Section 8.4.3.2 PD 7974-1:2019 calculates the temperature of ceiling jet above fire.

    :param Q_dot_c_kW: in kW, conductive heat release rate.
    :param z_H: in m, height of the ceiling above the fire source.
    :param z_0: height of the virtual source above the fuel surface.
    :param r: in m, radial distance from the ceiling impingement point.
    :return theta_cj: in deg.C, temperature (above ambient temperature) of ceiling jet.

    NOTES
    The properties of the ceiling jet are dependent upon the surface roughness of the ceiling together with heat losses
    to it. Most of the methods available in [24] calculate the maximum temperature and velocity in the ceiling jet. If
    detectors or sprinkler heads are situated substantially lower than where the maximum temperature and velocity
    occur, then longer activation times should be expected.

    The ceiling jet formulae assume that the jet is moving through ambient air and is not submerged within a ceiling
    smoke layer. Existing correlations in 8.3.3 for the maximum temperature and velocity in the plume can be used when
    `r` are less than or equal to the limits given. `z_H-z_0`

    REFERENCES
    [24] ALPERT R.L. Ceiling Jet Flows, SFPE Handbook of Fire Protection Engineering, Fifth Edition, 14, 429–454, 2016.
    """

    # Limitations see docstring
    try:
        assert r / (z_H - z_0) > 0.134
    except AssertionError:
        errmsg = f'Failed to assert `r / (z_H - z_0) = {r / (z_H - z_0):.3f} > 0.134`. ' \
                 f'Inputs are outside of the Alpert\'s ceiling jet correlation limits.'
        raise ValueError(errmsg)

    # intermediate variables
    aa = 6.721
    bb = (Q_dot_c_kW ** (2 / 3)) / ((z_H - z_0) ** (5 / 3))
    cc = (r / (z_H - z_0)) ** -0.6545

    # ceiling jet temperature above ambient temperature
    theta_cj = aa * bb * cc

    return theta_cj




def eq_27_axisymmetric_ceiling_jet_velocity(
        Q_dot_c_kW: float,
        z_H: float,
        z_0: float,
        r: float,
):
    """Equation 26 in Section 8.4.3.2 PD 7974-1:2019 calculates the temperature of ceiling jet above fire.

    :param Q_dot_c_kW: in kW, conductive heat release rate.
    :param z_H: in m, height of the ceiling above the fire source.
    :param z_0: height of the virtual source above the fuel surface.
    :param r: in m, radial distance from the ceiling impingement point.
    :return u_cj: in deg.C, temperature (above ambient temperature) of ceiling jet.

    NOTES
    The properties of the ceiling jet are dependent upon the surface roughness of the ceiling together with heat losses
    to it. Most of the methods available in [24] calculate the maximum temperature and velocity in the ceiling jet. If
    detectors or sprinkler heads are situated substantially lower than where the maximum temperature and velocity
    occur, then longer activation times should be expected.

    The ceiling jet formulae assume that the jet is moving through ambient air and is not submerged within a ceiling
    smoke layer. Existing correlations in 8.3.3 for the maximum temperature and velocity in the plume can be used when
    `r/(z_H-z_0)` are less than or equal to the limits given.

    REFERENCES
    [24] ALPERT R.L. Ceiling Jet Flows, SFPE Handbook of Fire Protection Engineering, Fifth Edition, 14, 429–454, 2016.
    """

    # Limitations see docstring
    try:
        assert r / (z_H - z_0) > 0.246
    except AssertionError:
        errmsg = f'Failed to assert `r / (z_H - z_0) = {r / (z_H - z_0)} > 0.246`. ' \
                 f'Inputs are outside of the Alpert\'s ceiling jet correlation limits.'
        raise ValueError(errmsg)

    # intermediate variables
    aa = 0.2526
    bb = (Q_dot_c_kW ** (1 / 3)) / ((z_H - z_0) ** (1 / 3))
    cc = (r / (z_H - z_0)) ** -1.0739

    # ceiling jet temperature above ambient temperature
    u_cj = aa * bb * cc

    return u_cj







