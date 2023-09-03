from fsetools.lib.fse_plume import *


def test_1():
    verification_z = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0,)
    verification_delta_T = (852.514, 527.425, 351.617, 221.328, 152.588, 112.603, 87.091, 69.714, 57.288,)
    verification_plume_diameter = (2.288, 3.227, 4.167, 5.106, 6.045, 6.984, 7.924, 8.863, 9.802,)

    x1, y1, x2, y2 = list(), list(), list(), list()

    for z_, delta_T_, fire_diameter_ in zip(verification_z, verification_delta_T, verification_plume_diameter):
        delta_T, z_Q_c_factor = centre_line_temperature(Q_c_kW=1000, z=z_, T_0=293)
        z_0 = virtual_origin(Q_c_kW=1000, HRRPUA_kW_m2=250, conv_frac=0.7)
        plume_diameter__ = plume_diameter(Q_c_kW=1000, HRRPUA_kW_m2=250, conv_frac=0.7, z_0=z_0, z=z_)
        assert abs(delta_T_ - delta_T) < 1e-3
        assert abs(fire_diameter_ - plume_diameter__) < 1e-3
        x1.append(z_Q_c_factor)
        y1.append(delta_T)
        x2.append(z_)
        y2.append(plume_diameter__)

    return x1, y1, x2, y2,


def test_2():
    import matplotlib.pyplot as plt

    z = np.linspace(0.1, 10, 100)
    delta_T, z_Q_c_factor = centre_line_temperature(Q_c_kW=1000, z=z, T_0=293)
    z_0 = virtual_origin(Q_c_kW=1000, HRRPUA_kW_m2=250, conv_frac=0.7)
    plume_diameter__ = plume_diameter(Q_c_kW=1000, HRRPUA_kW_m2=250, conv_frac=0.7, z_0=z_0, z=z)

    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(5, 5))

    ax1.plot(z_Q_c_factor, delta_T)
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_yticks(range(100, 1001, 100))
    ax1.set_ylabel('dT [$^o$C]')
    ax1.set_xlabel('z/$Q_{c}$$^{2/5}$')
    ax1.grid()
    ax2.plot(z, plume_diameter__)
    ax2.set_ylabel('Plume diameter [m]')
    ax2.set_xlabel('Height above ground [m]')
    ax2.grid()
    fig.tight_layout()
    fig.show()


if __name__ == '__main__':
    test_1()
    test_2()
