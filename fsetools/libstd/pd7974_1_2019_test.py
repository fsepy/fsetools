from fsetools.libstd.pd_7974_1_2019 import *


def test_eq_5_dimensionless_hrr():
    # function results
    function_results = eq_5_dimensionless_hrr(
        Q_dot_kW=500,
        rho_0=1.2,
        c_p_0_kJ_kg_K=1.,
        T_0=293.15,
        g=9.81,
        D=2,
    )

    # pre calculated results
    pre_calc_results = 0.08022  # 500 / 6232.76335

    # check
    assert abs(function_results - pre_calc_results) < 0.0001


def test_eq_11_dimensionless_hrr_rectangle():
    # function results
    function_results = eq_11_dimensionless_hrr_rectangular(
        Q_dot_kW=500,
        rho_0=1.2,
        c_p_0_kJ_kg_K=1.,
        T_0=293.15,
        g=9.81,
        L_A=5,
        L_B=2
    )

    # pre calculated results
    pre_calc_results = 0.02029  # 500 / 24637.16037

    # check
    assert abs(function_results - pre_calc_results) < 0.0001


def test_eq_12_dimensionless_hrr_line():
    # function results
    function_results = eq_12_dimensionless_hrr_line(
        Q_dot_l_kW_m=250,
        rho_0=1.2,
        c_p_0_kJ_kg_K=1.,
        T_0=293.15,
        g=9.81,
        L_A=5,
    )

    # pre calculated results
    pre_calc_results = 0.02029  # 250 / 12318.58018

    # check
    assert abs(function_results - pre_calc_results) < 0.0001


def test_eq_10_virtual_origin():
    """Tests `eq_10_virtual_origin`"""

    test_1 = eq_10_virtual_origin(
        D=1.,
        Q_dot_kW=1000.,
    )

    assert abs(test_1 - 0.29546) < 0.0001


def test_eq_14_plume_temperature():
    """Tests function `eq_14_plume_temperature`"""

    # Function result
    test_1 = eq_14_plume_temperature(
        T_0=293.15,
        g=9.81,
        c_p_0_kJ_kg_K=1.,
        rho_0=1.2,
        Q_dot_c_kW=1000.,
        z=3.,
        z_0=0.29546  # based on 1000 kW, 1 m fire.
    )

    # Hand calculation result
    # = 9.1 * 2.7480173245 * 100 * 0.1904777789
    # = 476.326975078

    # Check
    assert abs(test_1 - 476.326975078) < 0.0001


def test_eq_15_plume_velocity():
    """Tests (verification) `eq_15_plume_velocity`"""

    # Code calculation result
    test_1 = eq_15_plume_velocity(
        T_0=293.15,
        g=9.81,
        c_p_0_kJ_kg_K=1.,
        rho_0=1.2,
        Q_dot_c_kW=1000.,
        z=3.,
        z_0=0.29546  # based on 1000 kW, 1 m fire.
    )

    # Hand calculation result
    # = 3.4 * 0.3032489373 * 10 * 0.7177428315
    # = 7.4002615308

    assert abs(test_1 - 7.4002615308) < 0.0001


def test_eq_22_t_squared_fire_growth():
    """This function tests `eq_22_t_squared_fire_growth`.
    """

    # TEST 1
    # ======

    # Function result
    test_1 = eq_22_t_squared_fire_growth(
        alpha=0.0117,
        t=300,
        t_i=0,
        n=2
    )

    # Hand calculation result
    # 1053

    # Check
    assert abs(test_1 * 1e-3 - 1053.) < 1.


def test_eq_55_activation_of_heat_detector_device():
    """This function tests `eq_55_activation_of_heat_detector_device`.
    """

    # TEST 1
    # ======

    test_1 = eq_55_activation_of_heat_detector_device(
        u=15,  # gas velocity in proximity of the device, in m/s
        RTI=100,  # response time index, in (m s)^0.5
        Delta_T_g=80,  # gas temperature above ambient, in K or C
        Delta_T_e=60,  # device temperature above ambient, in K or C
        C=0.33  # conduction factor, in (m/s)^0.5
    )

    # Hand calculation
    # = (15 ** 0.5 / 100) * (80 - 60 * (1 + 0.33 / 15 ** 0.5))
    # = 0.03873 * (80 - 60 * (1 + 0.08521))
    # = 0.03873 * 14.8874
    # = 0.57659

    assert abs(test_1 - 0.57659) < 0.001


def test_eq_26_axisymmetric_ceiling_jet_temperature():
    """This function tests `eq_26_axisymmetric_ceiling_jet_temperature`"""

    # TEST 1
    # ======
    test_1 = eq_26_axisymmetric_ceiling_jet_temperature(
        Q_dot_c_kW=1000.,
        z_H=3,
        z_0=0.29546,  # based on a fire with D = 1 m, Q_dot_kW = 1000 kW
        r=1.75,
    )

    # Hand calculation result
    # = 6.721 * 19.047777892 * 1.329648149
    # = 170.2217092266

    # Check
    assert abs(test_1 - 170.2217092266) < 0.001


def test_eq_27_axisymmetric_ceiling_jet_velocity():
    """This function tests `eq_26_axisymmetric_ceiling_jet_temperature`"""

    # TEST 1
    # ======
    test_1 = eq_27_axisymmetric_ceiling_jet_velocity(
        Q_dot_c_kW=1000.,
        z_H=3,
        z_0=0.29546,  # based on a fire with D = 1 m, Q_dot_kW = 1000 kW
        r=1.75,
    )

    # Hand calculation result
    # = 0.2526 * 7.1774283152 * 1.5959767175
    # = 2.8935351427

    # Check
    assert abs(test_1 - 2.8935351427) < 0.001
