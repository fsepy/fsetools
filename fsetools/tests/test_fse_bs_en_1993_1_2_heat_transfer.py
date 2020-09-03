import numpy as np
from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c import protection_thickness as protection_thickness_c
from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c import temperature as temperature_c

from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer import temperature
from fsetools.lib.fse_travelling_fire import temperature_backup as fire_temperature


def __fire():
    temp = fire_temperature(
    t=np.arange(0, 210 * 60, 0.1),
    T_0=273.15,
    q_fd=600e6,
    hrrpua=0.25e6,
    l=100,
    w=16,
    s=0.012,
    e_h=3,
    e_l=50,
    T_max=1050+273.15,
    )

    # temp = fire_temperature(
    #     t=np.arange(0, 210 * 60, 0.1),
    #     fire_load_density_MJm2=600,
    #     fire_hrr_density_MWm2=0.25,
    #     room_length_m=100,
    #     room_width_m=16,
    #     fire_spread_rate_ms=0.012,
    #     beam_location_height_m=3,
    #     beam_location_length_m=100 / 2,
    #     fire_nft_limit_c=1050,
    # )

    return temp


def test_temperature():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    t = np.arange(0, 210 * 60, 0.1)
    kwargs = dict(
        fire_time=t,
        fire_temperature=__fire(),
        beam_rho=7850.,
        beam_cross_section_area=0.017,
        protection_k=0.2,
        protection_rho=800,
        protection_c=1700,
        protection_protected_perimeter=2.14,
    )

    list_dp = np.arange(0.0001, 0.01 + 0.002, 0.001)
    print(list_dp)

    for d_p in list_dp:
        kwargs['protection_thickness'] = d_p
        ax.plot(t, temperature(**kwargs) - 273.15, c='k')
        ax.plot(t, temperature_c(**kwargs) - 273.15, c='r', ls='--')
    ax.grid()

    plt.show()


def test_protection_thickness():
    t = np.arange(0, 210 * 60, 0.1)
    kwargs = dict(
        fire_time=t,
        fire_temperature=__fire(),
        beam_rho=7850.,
        beam_cross_section_area=0.017,
        protection_k=0.2,
        protection_rho=800,
        protection_c=1700,
        solver_temperature_goal=873.15,
        solver_temperature_goal_tol=1,
        protection_protected_perimeter=2.14,
    )
    print(protection_thickness_c(**kwargs))


if __name__ == '__main__':
    # test_temperature()
    test_protection_thickness()
