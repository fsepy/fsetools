import numpy as np

from fsetools.lib.fse_travelling_fire import temperature, temperature_si


def test_fire_travelling():
    time = np.arange(0, 210 * 60, 30)
    list_l = [25, 50, 100, 150]

    import matplotlib.pyplot as plt

    plt.style.use("seaborn-paper")
    fig, ax = plt.subplots(figsize=(3.94, 2.76))
    ax.set_xlabel("Time [minute]")
    ax.set_ylabel(u"Temperature [$℃$]")

    for length in list_l:
        temperature_ = temperature(
            t=time,
            fire_load_density_MJm2=600,
            fire_hrr_density_MWm2=0.25,
            room_length_m=length,
            room_width_m=16,
            fire_spread_rate_ms=0.012,
            beam_location_height_m=3,
            beam_location_length_m=length / 2,
            fire_nft_limit_c=1050,
        )

        ax.plot(time / 60, temperature_, label="Room length {:4.0f} m".format(length))

    ax.legend(loc=4).set_visible(True)
    ax.set_xlim((-10, 190))
    ax.grid(color="k", linestyle="--")
    plt.tight_layout()
    plt.show()


def test_fire_travelling_backup():
    import numpy as np

    time = np.arange(0, 22080, 30)
    list_l = [50, 100, 150]

    import matplotlib.pyplot as plt

    plt.style.use("seaborn-paper")
    fig, ax = plt.subplots(figsize=(3.94, 2.76))
    ax.set_xlabel("Time [minute]")
    ax.set_ylabel("Temperature [$℃$]")

    for l in list_l:
        temperature_0 = temperature_si(
            t=time,
            T_0=293.15,
            q_f_d=900e6,
            hrrpua=0.15e6,
            l=l,
            w=17.4,
            s=0.012,
            e_h=3.5,
            e_l=l / 2,
        )
        temperature_1 = temperature(
            t=time,
            fire_load_density_MJm2=900,
            fire_hrr_density_MWm2=0.15,
            room_length_m=l,
            room_width_m=17.4,
            fire_spread_rate_ms=0.012,
            beam_location_height_m=3.5,
            beam_location_length_m=l / 2,
            fire_nft_limit_c=1323.15 - 273.15
        )
        ax.plot(time / 60, temperature_0 - 273.15)
        ax.plot(time / 60, temperature_1, ls=':', c='r')

        assert np.allclose(temperature_0 - 273.15, temperature_1)

    ax.legend().set_visible(True)
    ax.set_xlim((0, 180))
    ax.grid(color="grey", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()


def test_fire_travelling_multiple():
    time = np.arange(0, 210 * 60, 30)
    length = 100

    import matplotlib.pyplot as plt

    plt.style.use("seaborn-paper")
    fig, ax = plt.subplots(figsize=(3.94, 2.76))
    ax.set_xlabel("Time [minute]")
    ax.set_ylabel("Temperature [$℃$]")

    temperature_list = temperature(
        t=time,
        fire_load_density_MJm2=600,
        fire_hrr_density_MWm2=0.25,
        room_length_m=length,
        room_width_m=16,
        fire_spread_rate_ms=0.012,
        beam_location_height_m=3,
        beam_location_length_m=np.linspace(0, length, 12)[1:-1],
        fire_nft_limit_c=1050,
    )

    for temperature_ in temperature_list:
        ax.plot(time / 60, temperature_, label="Room length {:4.0f} m".format(length))

    ax.legend(loc=4).set_visible(True)
    ax.set_xlim((-10, 190))
    ax.grid(color="k", linestyle="--")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # test_fire_travelling()
    test_fire_travelling_backup()
    # test_fire_travelling_multiple()
