from fsetools.lib.fse_flame_height import *


def test_mean_flame_height_pd_7974():
    # function results
    function_result_11 = mean_flame_height_pd_7974(Q_dot_star=0.14, fuel_type=0, fire_diameter=1.)
    function_result_12 = mean_flame_height_pd_7974(Q_dot_star=0.16, fuel_type=0, fire_diameter=1.)
    function_result_13 = mean_flame_height_pd_7974(Q_dot_star=0.5, fuel_type=0, fire_diameter=1.)
    function_result_14 = mean_flame_height_pd_7974(Q_dot_star=20, fuel_type=0, fire_diameter=1.)
    function_result_22 = mean_flame_height_pd_7974(Q_dot_star=5, fuel_type=1, fire_diameter=1.)
    function_result_32 = mean_flame_height_pd_7974(Q_dot_star=500, fuel_type=2, fire_diameter=1.)

    # calculated results
    pre_calc_result_11 = 0.784
    pre_calc_result_12 = 0.97258
    pre_calc_result_13 = 2.07887
    pre_calc_result_14 = 10.93770
    pre_calc_result_22 = 9.07508
    pre_calc_result_32 = 43.42160

    # check
    assert abs(function_result_11 - pre_calc_result_11) < 0.0001
    assert abs(function_result_12 - pre_calc_result_12) < 0.0001
    assert abs(function_result_13 - pre_calc_result_13) < 0.0001
    assert abs(function_result_14 - pre_calc_result_14) < 0.0001
    assert abs(function_result_22 - pre_calc_result_22) < 0.0001
    assert abs(function_result_32 - pre_calc_result_32) < 0.0001
