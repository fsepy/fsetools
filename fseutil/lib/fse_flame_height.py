def mean_flame_height_pd_7974(
        Q_dot_star: float,
        fuel_type: int,
        fire_diameter: float
):
    """Calculates mean flame height in accordance with Clause 8.3.2 in PD 7974-1:2019

    :param Q_dot_star: dimensionless heat release rate.
    :param fuel_type:   0   Natural gas 10 cm to 50 cm diameter burner [1]
                        1   10 cm to 200 cm side wood cribs ΔH_c = 18.6 MJ/kg [2]
                        2   Gas, liquids and solids ΔH_c/φ²=3185 kJ/kg of air [3]
    :param fire_diameter: in m, fire source diameter.
    :return flame_height: in m, calculated mean fire height.

    [1] ZUKOSKI E. Fire Safety Science. Proceedings of the First International Symposium on Fire Safety Science, 1984.
    [2] THOMAS P.H. The size of flames from natural fires, Ninth Symposium. The Combustion Institute, 1963.
    [3] HESKESTAD G. Virtual origins of fire plumes. Fire Safety Journal, 5 (2) pp. 109–114, 1983.
    """
    if fuel_type == 0:
        if Q_dot_star < 0.15:
            flame_height = fire_diameter * 40 * Q_dot_star ** 2
        elif Q_dot_star < 1.0:
            flame_height = fire_diameter * 3.3 * Q_dot_star ** (2 / 3)
        elif Q_dot_star < 40:
            flame_height = fire_diameter * 3.3 * Q_dot_star ** (2 / 5)
        else:
            flame_height = -1
    elif fuel_type == 1:
        if 0.75 < Q_dot_star < 8.8:
            flame_height = fire_diameter * 3.4 * Q_dot_star ** 0.61
        else:
            flame_height = -1
    elif fuel_type == 2:
        if 0.12 < Q_dot_star < 12000:
            flame_height = fire_diameter * (3.7 * Q_dot_star ** (2 / 5) - 1.02)
        else:
            flame_height = -1
    else:
        raise ValueError('Unknown fuel type.')

    return flame_height


def _test_mean_flame_height_pd_7974():
    # function results
    function_result_11 = mean_flame_height_pd_7974(Q_dot_star=0.14, fuel_type=0, fire_diameter=1.)
    function_result_12 = mean_flame_height_pd_7974(Q_dot_star=0.16, fuel_type=0, fire_diameter=1.)
    function_result_13 = mean_flame_height_pd_7974(Q_dot_star=0.5, fuel_type=0, fire_diameter=1.)
    function_result_14 = mean_flame_height_pd_7974(Q_dot_star=20, fuel_type=0, fire_diameter=1.)
    function_result_15 = mean_flame_height_pd_7974(Q_dot_star=41, fuel_type=0, fire_diameter=1.)
    function_result_21 = mean_flame_height_pd_7974(Q_dot_star=0.74, fuel_type=1, fire_diameter=1.)
    function_result_22 = mean_flame_height_pd_7974(Q_dot_star=5, fuel_type=1, fire_diameter=1.)
    function_result_23 = mean_flame_height_pd_7974(Q_dot_star=8.9, fuel_type=1, fire_diameter=1.)
    function_result_31 = mean_flame_height_pd_7974(Q_dot_star=0.11, fuel_type=2, fire_diameter=1.)
    function_result_32 = mean_flame_height_pd_7974(Q_dot_star=500, fuel_type=2, fire_diameter=1.)
    function_result_33 = mean_flame_height_pd_7974(Q_dot_star=12001, fuel_type=2, fire_diameter=1.)

    # calculated results
    pre_calc_result_11 = 0.784
    pre_calc_result_12 = 0.97258
    pre_calc_result_13 = 2.07887
    pre_calc_result_14 = 10.93770
    pre_calc_result_15 = -1
    pre_calc_result_21 = -1
    pre_calc_result_22 = 9.07508
    pre_calc_result_23 = -1
    pre_calc_result_31 = -1
    pre_calc_result_32 = 43.42160
    pre_calc_result_33 = -1

    # check
    assert abs(function_result_11 - pre_calc_result_11) < 0.0001
    assert abs(function_result_12 - pre_calc_result_12) < 0.0001
    assert abs(function_result_13 - pre_calc_result_13) < 0.0001
    assert abs(function_result_14 - pre_calc_result_14) < 0.0001
    assert abs(function_result_15 - pre_calc_result_15) < 0.0001
    assert abs(function_result_21 - pre_calc_result_21) < 0.0001
    assert abs(function_result_22 - pre_calc_result_22) < 0.0001
    assert abs(function_result_23 - pre_calc_result_23) < 0.0001
    assert abs(function_result_32 - pre_calc_result_32) < 0.0001
    assert abs(function_result_31 - pre_calc_result_31) < 0.0001
    assert abs(function_result_33 - pre_calc_result_33) < 0.0001


if __name__ == '__main__':
    _test_mean_flame_height_pd_7974()
