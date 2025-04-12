def eq_6_1_characteristic_fire_diameter(
        Q_star: float,
        rho_0: float = 1.204,
        c_p: float = 1.005,
        T_0: float = 293,
        g: float = 9.807,
):
    """
    This function calculates the characteristic fire diameter as defined in Section 6.3.6 FDS user's manual.

    Quote from the document:

    <q>
    The quantity D∗ / δx can be thought of as the number of computational cells spanning the characteristic (not
    necessarily the physical) diameter of the fire. The more cells spanning the fire, the better the resolution of the
    calculation. It is better to assess the quality of the mesh in terms of this non-dimensional parameter, rather than
    an absolute mesh cell size. For example, a cell size of 10 cm may be “adequate,” in some sense, for evaluating the
    spread of smoke and heat through a building from a sizable fire, but may not be appropriate to study a very small,
    smoldering source [fn1].

    [fn1]   For the validation study sponsored by the U.S. Nuclear Regulatory Commission, the D∗ / δx values ranged
            from 4 to 16.
    </q>

    :param Q_star: total heat release rate of the fire.
    :param rho_0: ambient air density.
    :param c_p: ambient air heat capacity.
    :param T_0: ambient air temperature.
    :param g: gravity.
    :return D_star: characteristic fire size.
    """

    D_star = (Q_star / (rho_0 * c_p * T_0 * g ** 0.5)) ** (2 / 5)

    return D_star


def _test_eq_6_1_characteristic_fire_diameter():
    results_func = eq_6_1_characteristic_fire_diameter(
        Q_star=1000,
    )

    results_hand_calc = 0.959

    assert abs(results_func - results_hand_calc) < 0.001


if __name__ == '__main__':
    _test_eq_6_1_characteristic_fire_diameter()
