import numpy as np

from .fse_thermal_radiation_v2 import phi_angled_any_en_1_converted


def _test_phi_parallel_any_br187():
    # All testing values are taken from independent sources
    # check receiver at emitter corner
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 0, 0, 0, 10)) - 0.1385316060) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 0, 10, 0, 10)) - 0.1385316060) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 10, 10, 0, 10)) - 0.1385316060) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 10, 0, 0, 10)) - 0.1385316060) < 1e-5

    # check receiver on emitter edge
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 2, 0, 0, 10)) - 0.1638694545) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 2, 10, 0, 10)) - 0.1638694545) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 0, 2, 0, 10)) - 0.1638694545) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 10, 2, 0, 10)) - 0.1638694545) < 1e-5

    # check receiver within emitter, center
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 5, 5, 0, 10)) - 0.2394564705) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 2, 2, 0, 10)) - 0.1954523349) < 1e-5

    # check receiver fall outside, sideways
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 5, 15, 0, 10)) - 0.0843536644) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 5, -5, 0, 10)) - 0.0843536644) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 15, 5, 0, 10)) - 0.0843536644) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, -5, 5, 0, 10)) - 0.0843536644) < 1e-5

    # check receiver fall outside, 1st quadrant
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 20, 15, 0, 10)) - 0.0195607021) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, 20, -5, 0, 10)) - 0.0195607021) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, -10, -5, 0, 10)) - 0.0195607021) < 1e-5
    assert abs(phi_angled_any_en_1_converted(*(10, 10, -10, 15, 0, 10)) - 0.0195607021) < 1e-5


def _test_phi_perpendicular_any_br187():
    # All testing values are taken from independent sources

    # check receiver at emitter corner
    assert abs(phi_angled_any_en_1_converted(10, 10, 0, 0, 0, 10) - 0.05573419700) < 1e-5

    # check receiver on emitter edge
    assert abs(phi_angled_any_en_1_converted(10, 10, 2, 0, 0, 10) - 0.06505816388) < 1e-5
    assert abs(phi_angled_any_en_1_converted(10, 10, 2, 10, 0, 10) - 0.06505816388) < 1e-5
    assert abs(phi_angled_any_en_1_converted(10, 10, 0, 2, 0, 10) - 0.04656468770) < 1e-5
    assert abs(phi_angled_any_en_1_converted(10, 10, 10, 2, 0, 10) - 0.04656468770) < 1e-5

    # check receiver fall outside, side ways
    assert abs(phi_angled_any_en_1_converted(10, 10, 5, -10, 0, 10) - 0.04517433814) < 1e-5
    assert abs(phi_angled_any_en_1_converted(10, 10, 5, 20, 0, 10) - 0.04517433814) < 1e-5


if __name__ == '__main__':
    # _test_phi_parallel_any_br187()
    phi_angled_any_en_1_converted(np.linspace(1, 10, 10), 10, -10, 15, 0, 10)
