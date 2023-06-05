# -*- coding: utf-8 -*-
import warnings

import numpy as np


def temperature(
        t: np.ndarray,
        A_w: float,
        h_w: float,
        A_t: float,
        A_f: float,
        t_alpha: float,
        b: float,
        q_x_d: float,
        gamma_fi_Q: float = 1.0,
        q_ref: float = 1300e6,
        rho_Q_dot: float = 0.25e6,
        outputs: dict = None,
):
    """This piece of code calculates a time dependent temperature array in accordance of Appendix AA in German Annex "
    Simplified natural fire model for fully developed room fires" to DIN EN 1991-1-2/NA:2010-12.
    Limitations are detailed in the Section AA.2 and they are:
      - minimum fuel load 100 MJ/sq.m
      - maximum fuel load 1,300 MJ/sq.m
      - maximum floor area 400 sq.m
      - maximum ceiling height 5 m
      - minimum vertical vent opening to floor area 12.5 %
      - maximum vertical vent opening to floor area 50 %

    PARAMETERS:
    :param t:           [s]     time
    :param A_w:         [m²]    is window opening area
    :param h_w:         [m²]    is weighted window opening height
    :param A_t:         [m²]    is total enclosure internal surface area, including openings
    :param A_f:         [m²]    is total floor area
    :param t_alpha:     [s]     is the fire growth factor, Table BB.2, for residential/office t_alpha = 300 [s]
    :param b:           [J/m²/s0.5/K] is the weighted heat storage capacity, see equation AA.31 and Table AA.1
    :param q_x_d:       [J/m²]  is the design value for fire load density, same as q_f_d
    :param gamma_fi_Q:  [1]     is the partial factor according to BB.5.3
    :param q_ref:       [J/m²]  is the reference upper bound heat release rate, 1300 [MJ/m²] for offices/residential
    :param rho_Q_dot:   [W/m²]  is the heat release rate per unit area
    :return T:          [K]     is calculated gas temperature within fire enclosure

    SUPPLEMENTAL DATA:

    DIN EN 1991-1-2/NA:1010-12 (English translation)

    Table AA.1 - Influence groups as a function of heat storage capacity b
    | Line | Influence group | Heat storage capacity b [J/m2/s0.5/K] |
    |------|-----------------|---------------------------------------|
    |    1 |               1 |                                  2500 |
    |    2 |               2 |                                  1500 |
    |    3 |               3 |                                   750 |

    Table BB.2
    | Line |                 Occupancy                  | Fire propagation | t_alpha [s] | RHR_f [MW/m2] |
    |------|--------------------------------------------|------------------|-------------|---------------|
    |    1 | Residential building                       | medium           |         300 |          0.25 |
    |    2 | Office building                            | medium           |         300 |          0.25 |
    |    3 | Hospital (room)                            | medium           |         300 |          0.25 |
    |    4 | Hotel (room)                               | medium           |         450 |          0.25 |
    |    5 | Library                                    | medium           |         300 |          0.25 |
    |    6 | School (classroom)                         | medium           |         300 |          0.15 |
    |    7 | Shop, shopping centre                      | fast             |         150 |          0.25 |
    |    8 | Place of public assembly (theatre, cinema) | fast             |         150 |          0.50 |
    |    9 | Public transport                           | slow             |         600 |          0.25 |
    """
    q_x_d /= 1e6  # J -> MJ
    rho_Q_dot /= 1e6  # W/m2 -> MW/m2
    q_ref /= 1e6  # J/m2 -> MJ/m2

    # AA.1
    Q_max_v_k = 1.21 * A_w * np.sqrt(h_w)  # [MW] AA.1

    # AA.2
    Q_max_f_k = rho_Q_dot * A_f  # [MW] AA.2

    # AA.3, Characteristic value of the maximum HRR, is the lower value of the Q_max_f_k and Q_max_v_k
    Q_max_k = min(Q_max_f_k, Q_max_v_k)  # [MW]

    # AA.5
    Q_max_v_d = gamma_fi_Q * Q_max_v_k  # [MW] AA.5
    Q_max_f_d = gamma_fi_Q * Q_max_f_k  # [MW] AA.6, gamma_fi_Q see BB.5.3

    # AA.6
    Q_max_d = gamma_fi_Q * Q_max_k

    # Work out fire type
    if Q_max_v_k == Q_max_k:
        fire_type = 0  # ventilation controlled fire
    elif Q_max_f_k == Q_max_k:
        fire_type = 1  # fuel controlled fire
    else:
        raise ValueError('Unknown fire type. Q_max_v_k={Q_max_v_k}, Q_max_k={Q_max_k}.')

    # AA.7 - AA.19: Calculate location of t and Q
    O = A_w * h_w ** 0.5 / A_t
    Q_d = q_ref * A_f  # [MJ], total fire load in the compartment
    if fire_type == 0:  # ventilation controlled fire
        # AA.7
        t_1 = t_alpha * np.sqrt(Q_max_v_d)  # [s] AA.7

        # AA.8
        T_1_v = -8.75 / O - 0.1 * b + 1175  # [°C]

        Q_1 = t_1 ** 3 / (3 * t_alpha ** 2)

        # AA.9
        Q_2 = 0.7 * Q_d - Q_1  # AA.9(a)
        t_2 = t_1 + Q_2 / Q_max_v_d  # [s] AA.9(b)

        # AA.10
        T_2_v = min((1340, (0.004 * b - 17) / O - 0.4 * b + 2175))

        # AA.11
        Q_3 = 0.3 * Q_d
        t_3 = t_2 + (2 * Q_3)

        # AA.12
        T_3_v = -5.0 / O - 0.16 * b + 1060  # [°C]

        T_1, T_2, T_3 = T_1_v, T_2_v, T_3_v

    elif fire_type == 1:  # fuel controlled fire
        # AA.19
        k = ((Q_max_f_d ** 2) / (A_w * h_w ** 0.5 * (A_t - A_w) * b)) ** (1 / 3)

        # AA.13
        t_1 = t_alpha * Q_max_f_d ** 0.5

        # AA.21
        Q_1 = t_1 ** 3 / (3 * t_alpha ** 2)  # [MW]

        # AA.14
        T_1_f = min(980., 24000 * k + 20)  # [°C]

        # AA.15
        Q_2 = 0.7 * Q_d - Q_1
        t_2 = t_1 + Q_2 / Q_max_f_d

        # AA.16
        T_2_f = min(1340., 33000 * k + 20)  # [°C]

        # AA.17
        Q_3 = 0.3 * Q_d
        t_3 = t_2 + (2 * Q_3) / Q_max_f_d

        # AA.18
        T_3_f = min(660., 16000 * k + 20)  # [°C]

        # AA.19
        # See above

        T_1, T_2, T_3 = T_1_f, T_2_f, T_3_f

    else:
        raise ValueError('Unexpected fire type.')

    # Prerequisite for AA.20 and AA.21
    Q_1 = t_1 ** 3 / (3 * t_alpha ** 2)  # [MW]
    Q_x_d = q_x_d * A_f

    if Q_1 < 0.7 * Q_x_d:
        # AA.20
        t_2_x = t_1 + (0.7 * Q_x_d - t_1 ** 3 / (3 * t_alpha ** 2)) / Q_max_d  # [s]

        # AA.21
        T_2_x = (T_2 - T_1) * ((t_2_x - t_1) / (t_2 - t_1)) ** 0.5 + T_1  # [°C]
    elif Q_1 >= 0.7:
        # AA.22
        t_1_x = (0.7 * Q_x_d * 3 * t_alpha ** 2) ** (1 / 3)  # [s]
        t_2_x = (0.7 * Q_x_d * 3 * t_alpha ** 2) ** (1 / 3)  # [s]

        # AA.23
        T_2_x = (T_1 - 20) / (t_1 ** 2) * t_1_x ** 2 + 20  # [°C]
    else:
        warnings.warn("Q_1 out of bound for AA.20 to AA.23.")
        t_1_x = t_2_x = T_2_x = np.nan

    # AA.25
    t_3_x = 0.6 * Q_x_d / Q_max_d + t_2_x  # [s]

    # AA.24
    T_3_x = T_3 * np.log10(t_3_x / 60 + 1) / np.log10(t_3 / 60 + 1)  # [°C]

    # Check flash-over, this has to be behind all calcs above!!!
    # AA.30
    Q_fo = 0.0078 * A_t + 0.378 * A_w * h_w ** 0.5  # [MW]
    # AA.29
    t_1_fo = (t_alpha ** 2 * Q_fo) ** 0.5  # [s]

    t_1 = min(t_1, t_1_fo)

    if 't_2_x' in outputs:
        outputs['t_2_x'] = t_2_x

    if outputs:
        for k in outputs.keys():
            if k in locals():
                outputs[k] = locals()[k]

    # CONVERT UNITS TO SI
    return T_t(t, t_1, t_2, t_2_x, t_3_x, T_1, T_2_x, T_3_x, ) + 273.15


# AA.26 - AA.28
def T_t(t, t_1, t_2, t_2_x, t_3_x, T_1, T_2_x, T_3_x, T_0=20):
    # Initialise container for return value
    T = np.zeros(len(t))

    # AA.26
    t_1_ = np.logical_and(0 <= t, t <= t_1)

    T_1_ = (T_1 - 20) / t_1 ** 2 * t[t_1_] ** 2 + 20
    T[t_1_] = T_1_  # [°C]

    # AA.27
    # t_2_ = np.logical_and(t_1 <= t, t <= t_2)
    # T_2_ = (T_2_x - T_1) * ((t[t_2_] - t_1) / (t_2_x - t_1)) ** 0.5 + T_1
    # T[t_2_] = T_2_  # [°C]

    # AA.27 MOD
    t_2_ = np.logical_and(t_1 <= t, t <= t_2_x)
    T_2_ = (T_2_x - T_1) * ((t[t_2_] - t_1) / (t_2_x - t_1)) ** 0.5 + T_1
    T[t_2_] = T_2_  # [°C]

    # AA.28
    # t_3_ = t > t_2
    # T_3_ = (T_3_x - T_2_x) * ((t[t_3_] - t_2) / (t_3_x - t_2_x)) ** 0.5 + T_2_x
    # T[t_3_] = T_3_  # [°C]

    # AA.28 MOD
    t_3_ = t > t_2_x
    T_3_ = (T_3_x - T_2_x) * ((t[t_3_] - t_2_x) / (t_3_x - t_2_x)) ** 0.5 + T_2_x
    T[t_3_] = T_3_  # [°C]

    # No temperate below T_initial
    T[T < T_0] = T_0

    return T
