from fsetools.lib.fse_external_fire_spread_prob import *


def test_radiative_heat_flux_from_fire():
    res = radiative_heat_flux_from_fire(
        fire_duration=30 * 60,  # Fire duration [mins]
        fire_time_step=1,  # Time step [sec]
        fire_hrr_density_kWm2=1000,  # HRR per unit area [kw/m²]
        fire_alpha=0.047,  # Fire growth parameter [kW/s²]
        fire_conv_frac=0.7,  # Convective fraction
        H=4.73,  # Height of ceiling [m]
        S=3,
        W_o=4,
        detector_to_fire_vertical_distance=4.73,
        detector_act_temp=93 + 273.15,  # Sprinkler activation temperature [deg C]
        detector_to_fire_horizontal_distance=5.66,  # Radial distance from the ceiling impingement point [m]
        detector_response_time_index=135,  # Sprinkler response time index [(m.s)^1/2]
        detector_conduction_factor=0.65,  # Conduction factor [(m.s)^1/2]
    )
    assert abs(res['q_f'] - 25.65647576197544) < 1e-7
    assert abs(res['q_s'] - 0.5572758456599368) < 1e-7
    assert abs(res['q'] - 26.213751607635377) < 1e-7


def test_flame_radiation():
    res = flame_radiation(
        fire_hrr_act_kW=3776.65,
        fire_hrr_density_kWm2=650,
        H=4.2,
        W_o=36.7,
        S=5.6,
        fire_conv_frac=0.7
    )
    assert abs(res['q_f'] - 5.198697215497442) < 1e-7


def test_smoke_radiation():
    res = smoke_radiation(
        smoke_temperature=99.65 + 273.15,
        epsilon_s=1,
        W_o=36.7,
        H=4.2,
        S=5.6,
    )
    assert abs(res['q_s'] - 0.234779676403217) < 1e-7


if __name__ == '__main__':
    test_radiative_heat_flux_from_fire()
    test_flame_radiation()
    test_smoke_radiation()
