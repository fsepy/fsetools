import numpy as np


def clause_a_3_temperature_time_heating_phase(t_star):
    # equation A.1, page 30
    a = 0.324 * np.exp(-0.2 * t_star)
    b = 0.204 * np.exp(-1.7 * t_star)
    c = 0.472 * np.exp(-19 * t_star)
    T_g = 1325 * (1 - a - b - c)
    return T_g


def clause_a_3_t_star(t, Gamma):
    # equation A.2a, page 30
    t_star = t * Gamma
    return t_star


def clause_a_7_t_star_max(t_max, Gamma):
    # equation A.6, page 31
    t_star_max = t_max * Gamma
    return t_star_max


def clause_a_7_t_max(t_lim, q_t_d, O):
    # equation A.7, page 31
    t_max = max([0.0002 * q_t_d / O, t_lim])
    return t_max


def clause_a_8_t_star(q_t_d, t_lim, b, t, t_max):
    assert abs(t_max - t_lim) < 1e-3

    # equation A.9, page 32
    O_lim = 0.1e-3 * q_t_d / t_lim
    # equation A.8, page 32
    Gamma_lim = ((O_lim / b) ** 2) / ((0.04 / 1160) ** 2)
    # equation A.2b, page 32
    t_star = t * Gamma_lim
    return t_star


def clause_a_11_temperature_time_curve_cooling_phase(
        q_t_d,
        Gamma,
        O,
        t_max,
        t_lim,
        Theta_max,
        t_star,
        override_t_max_lower_than_t_lim: bool = False
):
    # equation A.12, page 32
    t_star_max = (0.2e-3 * q_t_d / O) * Gamma
    if t_max > t_lim:
        x = 1
    elif abs(t_max - t_lim) < 1e-3 or override_t_max_lower_than_t_lim:  # t_max == t_lim
        x = t_lim * Gamma / t_star_max
    else:
        raise ValueError(f'Conditions t_max > t_lim or t_max == t_lim not met, {t_max} {t_lim}')

    if t_star_max <= 0.5:
        # equation A.11a
        Theta_g = Theta_max - 625 * (t_star - t_star_max * x)
    elif 0.5 < t_star_max < 2.0:
        # equation A.11b
        Theta_g = Theta_max - 250 * (3 - t_star_max) * (t_star - t_star_max * x)
    elif 2.0 <= t_star_max:
        # equation A.11c
        Theta_g = Theta_max - 250 * (t_star - t_star_max * x)
    else:
        Theta_g = np.nan
    return Theta_g


def fire(
        t, A_t, A_f, A_v, h_eq, q_fd, lambda_, rho, c, t_lim, temperature_initial=293.15
):
    """
    Function Description:

    This function calculates the time-temperature curve according to Eurocode 1 part 1-2, Appendix A.

    :param t: numpy.ndarray, [s], time evolution.
    :param A_t: float, [m2], total surface area (including openings).
    :param A_f: float, [m2], floor area.
    :param A_v: float, [m2], opening area.
    :param h_eq: float, [m2], opening height.
    :param q_fd: float, [J/m2], fuel density.
    :param lambda_: float, [K/kg/m], lining thermal conductivity.
    :param rho: float, [kg/m3], lining density.
    :param c: float, [J/K/kg], lining thermal capacity.
    :param t_lim: float, [s], limiting time for the fire.
    :return T_g: numpy.ndarray, [s], temperature evolution.


    Table F.2 - Conversion factor k_b depending on the thermal properties of the enclosure
    | b=√(ρcλ) [J/m²/s0.5/K]                  | k_b [min⋅m²/MJ]   |
    |:----------------------------------------|:------------------|
    | b>2500                                  | 0.04              |
    | 2500>=b>=720                            | 0.055             |
    | b<720                                   | 0.07              |
    """
    # Reference: Eurocode 1991-1-2; Jean-Marc Franssen, Paulo Vila Real (2010) - Fire Design of Steel Structures

    # UNITS: SI -> Equations
    q_fd /= 1e6  # [J/m2] -> [MJ/m2]
    t_lim /= 3600  # [s] -> [hr]
    t = t / 3600  # [s] -> [hr]
    temperature_initial -= 273.15  # [K] -> [C]

    # ACQUIRING REQUIRED VARIABLES
    # t = np.arange(time_start, time_end, time_step, dtype=float)

    b = (lambda_ * rho * c) ** 0.5
    O = A_v * h_eq ** 0.5 / A_t
    q_td = q_fd * A_f / A_t
    Gamma = ((O / 0.04) / (b / 1160)) ** 2

    t_max = 0.0002 * q_td / O

    # check criteria
    # todo: raise warnings to higher level
    # if not 50 <= q_td <= 1000:
    #     if is_cap_q_td:
    #         msg = "q_td ({:4.1f}) EXCEEDED [50, 1000] AND IS CAPPED.".format(q_td, is_cap_q_td)
    #     else:
    #         msg = "q_td ({:4.1f}) EXCEEDED [50, 1000] AND IS UNCAPPED.".format(q_td)
    #     warnings.warn(msg)

    # CALCULATION
    def _variables(t, Gamma, t_max):
        t_star = Gamma * t
        t_star_max = Gamma * t_max
        return t_star, t_star_max

    def _variables_2(t, t_lim, q_td, b, O):
        O_lim = 0.0001 * q_td / t_lim
        Gamma_lim = ((O_lim / 0.04) / (b / 1160)) ** 2

        if O > 0.04 and q_td < 75 and b < 1160:
            k = 1 + ((O - 0.04) / (0.04)) * ((q_td - 75) / (75)) * ((1160 - b) / (1160))
            Gamma_lim *= k

        t_star_ = Gamma_lim * t
        t_star_max_ = Gamma_lim * t_lim
        return t_star_, t_star_max_

    t_star, t_star_max = _variables(t, Gamma, t_max)
    # t_max = clause_a_7_t_max(t_lim, q_t_d=q_td, O=O)
    # t_star_max = clause_a_7_t_star_max(t_max=t_max, Gamma=Gamma)

    if t_max >= t_lim:  # ventilation controlled fire
        T_max = clause_a_3_temperature_time_heating_phase(t_star_max)
        T_heating_g = clause_a_3_temperature_time_heating_phase(Gamma * t)
        # T_cooling_g = _temperature_cooling_vent(t_star_max, T_max, t_star)
        fire_type = "ventilation controlled"
    else:  # fuel controlled fire
        t_star_, t_star_max_ = _variables_2(t, t_lim, q_td, b, O)
        T_max = clause_a_3_temperature_time_heating_phase(t_star_max_)
        T_heating_g = clause_a_3_temperature_time_heating_phase(t_star_)
        # T_cooling_g = _temperature_cooling_fuel(t_star_max, T_max, t_star, Gamma, t_lim)
        fire_type = "fuel controlled"

    T_cooling_g = clause_a_11_temperature_time_curve_cooling_phase(
        q_t_d=q_td,
        Gamma=Gamma,
        O=O,
        t_max=t_max,
        t_lim=t_lim,
        Theta_max=T_max,
        t_star=t_star,
        override_t_max_lower_than_t_lim=True
    )

    T_g = np.minimum(T_heating_g, T_cooling_g)
    T_g[T_g < temperature_initial] = temperature_initial

    # UNITS: Eq. -> SI
    t *= 3600
    T_g += 273.15

    return T_g


def _test_fire():
    """This is a test function to `fire` within this module `fire_parametric_ec`, it compares the function against
    Figure 7 in Holicky, M. et al [1].
    yan fu, 1 oct 2018

    REFERENCES
    [1] Holicky, M., Meterna, A., Sedlacek, G. and Schleich, J.B., 2005. Implementation of eurocodes, handbook 5, design
    of buildings for the fire situation. Leonardo da Vinci Pilot Project: Luxembourg."""

    import copy
    import pandas

    # LOAD VERIFICATION DATA
    # data are from the referenced document
    from io import StringIO

    verification_data = StringIO(
        """time_1,temperature_1,time_2,temperature_2,time_3,temperature_3,time_4,temperature_4,time_5,temperature_5,time_6,temperature_6,time_7,temperature_7
        20,689.1109391,20,689.1109391,20,689.1109391,20,843.9616854,20,741.3497451,20,601.424372,20,269.3348197
        30,782.7282474,30,782.7317977,30,782.7317977,30,946.9144525,30,827.5114674,30,726.7651987,30,430.1234077
        40,167.4009827,40,402.4756096,40,508.8188932,40,781.2034026,40,885.6845648,40,777.4756096,40,533.0726245
        50,20,50,20,50,236.7716603,50,540.8761379,50,818.8612125,50,813.2641976,50,604.3089737
        60,20,60,20,60,20,60,304.2731159,60,692.3328174,60,843.4522203,60,651.2880412
        70,20,70,20,70,20,70,69.53931579,70,565.8079725,70,780.3602113,70,685.2109576
        80,20,80,20,80,20,80,20,80,441.145249,80,719.1303236,80,709.8019654"""
    )
    verification_data = pandas.read_csv(
        verification_data, skip_blank_lines=True, skipinitialspace=True
    )

    # CALCULATE TIME TEMPERATURE CURVE BASED ON THE VERIFICATION DATA INPUTS

    # prepare inputs
    kws = dict(
        A_t=360,
        A_f=100,
        h_eq=1,
        q_fd=600e6,
        lambda_=1,
        rho=1,
        c=2250000,
        t_lim=20 * 60,
        t=np.arange(0, 2 * 60 * 60 + 1, 1),
        temperature_initial=293.15,
    )

    # define opening area
    A_v_list = [72, 50.4, 36.000000001, 32.4, 21.6, 14.4, 7.2]

    # calculate fire curves
    x1_list = []  # calculated time array
    y1_list = []  # calculated temperature array
    for i in A_v_list:
        y = fire(A_v=i, **copy.copy(kws))
        x = np.arange(0, 2 * 60 * 60 + 1, 1) + 10 * 60
        x1_list.append(x / 60)
        y1_list.append(y - 273.15)

    # COMPARE CALCULATED AND THE VERIFICATION DATA

    def r_square(x1, y1, x2, y2):
        from scipy.interpolate import interp1d
        from scipy import stats

        slope, intercept, r_value, p_value, std_err = stats.linregress(
            y2, interp1d(x1, y1)(x2)
        )
        return r_value ** 2

    for i in range(len(A_v_list)):
        x1 = x1_list[i]
        y1 = y1_list[i]
        x2 = verification_data["time_{}".format(int(i + 1))]
        y2 = verification_data["temperature_{}".format(int(i + 1))]
        assert r_square(x1, y1, x2, y2) > 0.99


if __name__ == "__main__":
    # exmaple_plot_interflam()
    _test_fire()
