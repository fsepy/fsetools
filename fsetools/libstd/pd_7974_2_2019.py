"""
All SI UNITS unless specified.
"""


def eq_62_A_v(m_dot_smoke, T_0, T_1, rho_0, C_v, g, d_v, theta_1, A_in, C_in):
    """Natural (outlet) vent geometrical area required.

    :param m_dot_smoke:
    :param T_0: K, ambient air temperature
    :param T_1: K, absolute temperature of gas layer in reservoir
    :param theta_1: deg.C, excess temperature of the smoke layer in a reservoir
    :param A_in: m2, inlet vent area
    :param d_v: m, depth of smoke below centreline of vent (i.e., to mid-vent)
    :param C_v: 1, coefficient of discharge
    :param C_in: 1, coefficient of inlet/supply vent
    :param rho_0: kg/m3, ambient air density
    :param g: m/s2, gravity acceleration
    :return:
    """
    _a = m_dot_smoke * T_1
    _b = 2 * g * d_v * (rho_0 ** 2) * theta_1 * T_0
    _c = (T_1 * T_0 * m_dot_smoke ** 2) / (A_in ** 2 * C_in ** 2)
    return _a / ((C_v * (_b - _c)) ** 0.5)


def eq_63_A_v(m_dot_smoke, T_0: float, c_p_0, rho_0, C_v, g, d_v, Q_dot_c):
    """Natural (outlet) vent geometrical area required for very large inlet areas.

    :param m_dot_smoke: kg/s, mass flow rate of smoke
    :param T_0: K, ambient temperature
    :param c_p_0: kJ/kg/K, ambient air specific heat at constant pressure
    :param rho_0: kg/m3, ambient air density
    :param C_v: 1, coefficient of discharge
    :param g: m/s2, gravity acceleration
    :param d_v: m, depth of smoke below centreline of vent (i.e., to mid-vent)
    :param Q_dot_c: kW, rate of heat release convected by the plume
    :return:
    """
    _a = (m_dot_smoke ** 1.5) * (T_0 ** 0.5) * (c_p_0 ** 0.5)
    _b = rho_0 * C_v * ((2 * g * d_v) ** 0.5)
    _c = 1 / Q_dot_c
    _d = 1 + Q_dot_c / (m_dot_smoke * c_p_0 * T_0)
    return (_a / _b) * _c * _d
