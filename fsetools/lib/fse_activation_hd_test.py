from fsetools.lib.fse_activation_hd import *


def test_heat_detector_activation_ceiling_pd7974():
    from fsetools.libstd.pd_7974_1_2019 import eq_22_t_squared_fire_growth

    # Pre-calculated results

    # Code results
    t = np.array([i * 0.5 for i in range(1200)])
    res = heat_detector_temperature_pd7974(
        fire_time=t,
        fire_hrr_kW=[eq_22_t_squared_fire_growth(alpha=0.0117, t=i) / 1000. for i in t],
        detector_to_fire_vertical_distance=3.6,
        detector_to_fire_horizontal_distance=2.83,
        detector_response_time_index=115,
        detector_conduction_factor=0.4,
        fire_hrr_density_kWm2=510,
        fire_conv_frac=0.7,
    )
    detector_activation_temperature = 68 + 273.15

    # find the activation time
    calculated_activation_time = t[np.argmin(np.abs(res['detector_temperature'] - detector_activation_temperature))]
    given_activation_time = 333  # checked against Chris Mayfield's calculation on 7th Feb 2020 15:20, Bicester
    assert abs(calculated_activation_time - given_activation_time) <= 1.


def test_heat_detector_activation_ceiling_pd7974_2():
    from fsetools.libstd.pd_7974_1_2019 import eq_22_t_squared_fire_growth

    # Pre-calculated results

    # Code results
    gas_time = np.array([i * 0.5 for i in range(1200)])
    gas_hrr_kWm2 = eq_22_t_squared_fire_growth(0.0117, gas_time) / 1000.
    res = heat_detector_temperature_pd7974(
        fire_time=gas_time,
        fire_hrr_kW=gas_hrr_kWm2,
        detector_to_fire_vertical_distance=3.,
        detector_to_fire_horizontal_distance=2.5,
        detector_response_time_index=115,
        detector_conduction_factor=0.4,
        fire_hrr_density_kWm2=510,
        fire_conv_frac=0.7,
    )
    detector_activation_temperature = 68 + 273.15

    # find the activation time
    calculated_activation_time = gas_time[
        np.argmin(np.abs(res['detector_temperature'] - detector_activation_temperature))]
    given_activation_time = 287  # checked against Danny Hopkin's calculation on 7th Feb 2020 16:20, Bicester
    assert abs(calculated_activation_time - given_activation_time) <= 1.
