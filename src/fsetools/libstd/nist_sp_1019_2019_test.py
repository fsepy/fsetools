from .nist_sp_1019_2019 import *


def test_eq_6_1_characteristic_fire_diameter():
    results_func = eq_6_1_characteristic_fire_diameter(
        Q_star=1000,
    )
    results_hand_calc = 0.959
    assert abs(results_func - results_hand_calc) < 0.001


if __name__ == '__main__':
    test_eq_6_1_characteristic_fire_diameter()
