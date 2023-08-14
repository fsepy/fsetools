# -*- coding: utf-8 -*-

from fsetools.lib.fse_travelling_fire_flux import *


def test_fire():
    time = np.arange(0, 120 * 60 + 5, 10)
    list_l = [5, 10, 15, 20, 25, 30, 35]

    import matplotlib.pyplot as plt

    plt.style.use("seaborn-paper")
    fig, ax = plt.subplots(figsize=(3.94, 2.76))
    ax.set_xlabel("Time [minute]")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 130)
    ax.set_ylabel('Incident heat flux [kW/m$^2$]')

    dict_data = {
        'time': time,
    }

    # Bench marking data created on 27th Oct 2020 based upon the current module to date.
    # Third party independent bench marking data should be used when possible in the future.
    benchmark_data = [
        [120., 76.254, 20.52940854, 6.2199491, 1.46112866],
        [71.94916035, 120., 38.21356264, 10.64247797, 2.40767674],
        [32.31925324, 92.90937378, 70.63257901, 19.95276393, 4.28969048],
        [14.37444291, 50.11227294, 120., 38.63567426, 8.50709581],
        [7.14649502, 27.02891858, 101.01412924, 74.17947618, 19.72186683],
        [3.97111501, 14.43237124, 54.65055657, 120., 49.03390614],
        [2.39197632, 8.31942742, 29.56698589, 88.02792, 120., ],
    ]

    for i, beam_location_length_m in enumerate(list_l):
        heat_flux_ = heat_flux(
            t=time,
            fire_load_density_MJm2=760 * 0.8,
            fire_hrr_density_MWm2=0.5,
            room_length_m=40,
            room_width_m=16,
            fire_spread_rate_ms=0.018,
            beam_location_height_m=3,
            beam_location_length_m=beam_location_length_m,
            fire_nff_limit_kW=120,
        )

        assert np.allclose(heat_flux_[[60, 120, 180, 240, 300]], benchmark_data[i], rtol=1.e-3)
        ax.plot(time / 60, heat_flux_, label="Ceiling position {:4.0f} m".format(beam_location_length_m))

        dict_data['Ceiling location = ' + str(beam_location_length_m) + ' [m]'] = heat_flux_

    ax.legend(loc=4).set_visible(True)
    ax.grid(color="k", linestyle="--")
    plt.tight_layout()
    plt.show()

    # df_data = pd.DataFrame.from_dict(dict_data)

    return dict_data
