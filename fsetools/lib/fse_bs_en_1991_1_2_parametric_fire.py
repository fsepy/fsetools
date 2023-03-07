import numpy as np

__all__ = 'temperature',


# CALCULATION
def eq_3_12_T_g(t_star, T_0: float = 20):
    # eq. 3.12
    T_g = 1325 * (1 - 0.324 * np.exp(-0.2 * t_star) - 0.204 * np.exp(-1.7 * t_star) - 0.472 * np.exp(-19 * t_star))
    T_g += T_0
    return T_g


def eq_3_16_T_g(t_star_max, T_max, t_star):  # ventilation controlled
    # eq. 3.16
    if t_star_max <= 0.5:
        T_g = T_max - 625 * (t_star - t_star_max)
    elif 0.5 < t_star_max < 2.0:
        T_g = T_max - 250 * (3 - t_star_max) * (t_star - t_star_max)
    elif 2.0 <= t_star_max:
        T_g = T_max - 250 * (t_star - t_star_max)
    else:
        T_g = np.nan
    return T_g


def eq_3_22_T_g(t_star_max, T_max, t_star, Gamma, t_lim):  # fuel controlled
    # eq. 3.22
    if t_star_max <= 0.5:
        T_g = T_max - 625 * (t_star - Gamma * t_lim)
    elif 0.5 < t_star_max < 2.0:
        T_g = T_max - 250 * (3 - t_star_max) * (t_star - Gamma * t_lim)
    elif 2.0 <= t_star_max:
        T_g = T_max - 250 * (t_star - Gamma * t_lim)
    else:
        T_g = np.nan
    return T_g


def variables_1(t, Gamma, t_max):
    t_star = Gamma * t
    t_star_max = Gamma * t_max
    return t_star, t_star_max


def variables_2(t, t_lim, q_td, b, O):
    O_lim = 0.0001 * q_td / t_lim
    Gamma_lim = ((O_lim / 0.04) / (b / 1160)) ** 2

    if O > 0.04 and q_td < 75 and b < 1160:
        k = 1 + ((O - 0.04) / (0.04)) * ((q_td - 75) / (75)) * ((1160 - b) / (1160))
        Gamma_lim *= k

    t_star_ = Gamma_lim * t
    t_star_max_ = Gamma_lim * t_lim
    return t_star_, t_star_max_


def temperature(
        t: np.ndarray, A_t: float, A_f: float, A_v: float, h_eq: float, q_fd: float, lbd: float, rho: float,
        c: float, t_lim: float, T_0: float = 293.15):
    """Function Description: (SI UNITS ONLY)
    This function calculates the time-temperature curve according to Eurocode 1 part 1-2, Appendix A.
    :param t: numpy.ndarray, [s], time evolution.
    :param A_t:     [m2], total surface area (including openings).
    :param A_f:     [m2], floor area.
    :param A_v:     [m2], opening area.
    :param h_eq:    [m2], opening height.
    :param q_fd:    [J/m2], fuel density.
    :param lbd:     [K/kg/m], lining thermal conductivity.
    :param rho:     [kg/m3], lining density.
    :param c:       [J/K/kg], lining thermal capacity.
    :param t_lim:   [s], limiting time for the fire.
    :return T_g:    [s], temperature evolution.
    """
    # Reference: Eurocode 1991-1-2; Jean-Marc Franssen, Paulo Vila Real (2010) - Fire Design of Steel Structures

    # Convert units SI -> Local
    q_fd = q_fd / 1e6  # [J/m2] -> [MJ/m2]
    t_lim = t_lim / 3600  # [s] -> [hr]
    t = t / 3600  # [s] -> [hr]
    T_0 = T_0 - 273.15  # [K] -> [C]

    # ACQUIRING REQUIRED VARIABLES
    b = (lbd * rho * c) ** 0.5  # thermal inertia
    O = A_v * h_eq ** 0.5 / A_t  # opening factor
    q_td = q_fd * A_f / A_t  # total fuel load
    Gamma = ((O / 0.04) / (b / 1160)) ** 2

    t_max = 0.0002 * q_td / O

    # check criteria
    # if not 50 <= q_td <= 1000:
    #     if is_cap_q_td:
    #         msg = "q_td ({:4.1f}) EXCEEDED [50, 1000] AND IS CAPPED.".format(q_td, is_cap_q_td)
    #     else:
    #         msg = "q_td ({:4.1f}) EXCEEDED [50, 1000] AND IS UNCAPPED.".format(q_td)
    #     warnings.warn(msg)

    t_star, t_star_max = variables_1(t, Gamma, t_max)

    if t_max >= t_lim:  # ventilation controlled fire
        T_max = eq_3_12_T_g(t_star_max, T_0)
        T_g_heating = eq_3_12_T_g(Gamma * t, T_0)
        T_g_cooling = eq_3_16_T_g(t_star_max, T_max, t_star)
    else:  # fuel controlled fire
        t_star_f, t_star_max_f = variables_2(t, t_lim, q_td, b, O)
        T_max = eq_3_12_T_g(t_star_max_f, T_0)
        T_g_heating = eq_3_12_T_g(t_star_f, T_0)
        T_g_cooling = eq_3_22_T_g(t_star_max, T_max, t_star, Gamma, t_lim)

    T_g = np.minimum(T_g_heating, T_g_cooling)
    T_g[T_g < T_0] = T_0

    # UNITS: Eq. -> SI
    T_g += 273.15

    return T_g
