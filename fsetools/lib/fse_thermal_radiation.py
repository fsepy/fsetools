# coding: utf-8

import math
from statistics import median
from typing import Callable

from fsetools.libstd.bre_br_187_2014 import eq_A4_phi_parallel_corner
from fsetools.libstd.bre_br_187_2014 import eq_A5_phi_perpendicular_corner


def linear_solver(
        func: Callable,
        dict_params: dict,
        x_name: str,
        y_target: float,
        x_upper: float,
        x_lower: float,
        y_tol: float,
        iter_max: int = 1000,
        func_multiplier: float = 1
):
    """Solver of single-root function (single variable), i.e. f(x)=a x + b

    :param func:            The function to be solved.
    :param dict_params:     Additional parameters of the function.
    :param x_name:          The variable (name) to be solved for.
    :param y_target:        The target to be solved for, i.e. solve for `f(x)==y_target`.
    :param x_upper:         The upper limit of the variable.
    :param x_lower:         The lower limit of the variable.
    :param y_tol:           Solver tolerance, i.e. actually solve for `abs(f(x)-y_target)<y_tal`.
    :param iter_max:        Maximum iteration of the solver.
    :param func_multiplier: 1 if f(x) is proportional to x, -1 if f(x) is inversely proportional to x.
    :return:                The solved value, i.e. x_solved when following is true `abs(f(x_solved)-y_target)<y_tal`.

    """
    if x_lower > x_upper:
        x_lower += x_upper
        x_upper = x_lower - x_upper
        x_lower = x_lower - x_upper

    y_target *= func_multiplier

    x1 = x_lower
    x2 = (x_lower + x_upper) / 2
    x3 = x_upper

    dict_params[x_name] = x1
    y1 = func_multiplier * func(**dict_params)
    dict_params[x_name] = x2
    y2 = func_multiplier * func(**dict_params)
    dict_params[x_name] = x3
    y3 = func_multiplier * func(**dict_params)

    if y_target < y1:
        return x1
    if y_target > y3:
        return x3

    iter_count = 0
    while True:
        if abs(y2 - y_target) < y_tol:
            return x2
        elif iter_max < iter_count:
            return None
        elif y2 < y_target:
            x1 = x2
        elif y2 > y_target:
            x3 = x2
        x2 = (x1 + x3) / 2
        dict_params[x_name] = x2
        y2 = func_multiplier * func(**dict_params)
        iter_count += 1

    return None  # this shouldn't be possible, should always terminate within the while loop above


def phi_parallel_any_br187(W_m, H_m, w_m, h_m, S_m):
    r"""
    :param W_m:
    :param H_m:
    :param w_m:
    :param h_m:
    :param S_m:
    :return:
    """
    phi = [
        eq_A4_phi_parallel_corner(*P[0:-1], S_m, P[-1])
        for P in four_planes(W_m, H_m, w_m, h_m)
    ]
    return sum(phi)


def phi_perpendicular_any_br187(W_m, H_m, w_m, h_m, S_m):
    four_P = four_planes(W_m, H_m, w_m, h_m)
    phi = [eq_A5_phi_perpendicular_corner(*P[0:-1], S_m, P[-1]) for P in four_P]
    return sum(phi)


def four_planes(W_m: float, H_m: float, w_m: float, h_m: float) -> tuple:
    """
    :param W_m:
    :param H_m:
    :param w_m:
    :param h_m:
    :return:
    """

    # COORDINATES
    o = (0, 0)
    e1 = (0, 0)
    e2 = (W_m, H_m)
    r1 = (w_m, h_m)

    # GLOBAL MIN, MEDIAN AND MAX
    min_ = (min([W_m, w_m, 0]), min([H_m, h_m, 0]))
    mid_ = (median([W_m, w_m, 0]), median([H_m, h_m, 0]))
    max_ = (max([W_m, w_m, 0]), max([H_m, h_m, 0]))

    # FOUR PLANES
    A = 0, 0, 0
    B = 0, 0, 0
    C = 0, 0, 0
    D = 0, 0, 0

    # RECEIVER AT CORNER
    if e1 == e2 or e1 == r1 or e1 == (e2[0], r1[1]) or e1 == (r1[0], e2[1]):
        A = (max_[0] - min_[0], max_[1] - min_[1], 1)
        B = (0, 0, 0)
        C = (0, 0, 0)
        D = (0, 0, 0)

        # A = phi_parallel_corner_br187(*A, S_m)
        #
        # phi = A

    # RECEIVER ON EDGE
    elif ((r1[0] == e1[0] or r1[0] == e2[0]) and e1[1] < r1[1] < e2[1]) or (
            (r1[1] == e1[1] or r1[1] == e2[1]) and e1[0] < r1[0] < e2[0]
    ):
        # vertical edge
        if (r1[0] == e1[0] or r1[0] == e2[0]) and e1[1] < r1[1] < e2[1]:
            A = (max_[0] - min_[0], max_[1] - mid_[1], 1)
            B = (max_[0] - min_[0], mid_[1] - min_[1], 1)
            C = (0, 0, 0)
            D = (0, 0, 0)

        # horizontal edge
        elif (r1[1] == e1[1] or r1[1] == e2[1]) and e1[0] < r1[0] < e2[0]:
            A = (max_[0] - mid_[0], max_[1] - min_[1], 1)
            B = (mid_[0] - min_[0], max_[1] - min_[1], 1)
            C = (0, 0, 0)
            D = (0, 0, 0)
        else:
            print("error")

    # RECEIVER WITHIN EMITTER
    elif o[0] < w_m < W_m and o[1] < h_m < H_m:
        A = (mid_[0] - min_[0], mid_[1] - min_[1], 1)
        B = (max_[0] - mid_[0], max_[1] - mid_[1], 1)
        C = (mid_[0] - min_[0], max_[1] - mid_[1], 1)
        D = (max_[0] - mid_[0], mid_[1] - min_[1], 1)

    # RECEIVER OUTSIDE EMITTER
    else:
        # within y-axis range max[1] and min[1], far right
        if min_[1] < r1[1] < max_[1] and r1[0] == max_[0]:
            A = max_[0] - min_[0], max_[1] - mid_[1], 1
            B = max_[0] - min_[0], mid_[1] - min_[1], 1
            C = max_[0] - mid_[0], max_[1] - mid_[1], -1  # negative
            D = max_[0] - mid_[0], mid_[1] - min_[1], -1  # negative
        # within y-axis range max[1] and min[1], far left
        elif min_[1] < r1[1] < max_[1] and r1[0] == min_[0]:
            A = max_[0] - min_[0], max_[1] - mid_[1], 1
            B = max_[0] - min_[0], mid_[1] - min_[1], 1
            C = mid_[0] - min_[0], max_[1] - mid_[1], -1  # negative
            D = mid_[0] - min_[0], mid_[1] - min_[1], -1  # negative
        # within x-axis range max[0] and min[0], far top
        elif min_[0] < r1[0] < max_[0] and r1[1] == max_[1]:
            A = max_[0] - mid_[0], max_[1] - min_[1], 1
            B = mid_[0] - min_[0], max_[1] - min_[1], 1
            C = max_[0] - mid_[0], max_[1] - mid_[1], -1
            D = mid_[0] - min_[0], max_[1] - mid_[1], -1
        # within x-axis range max[0] and min[0], far bottom
        elif min_[0] < r1[0] < max_[0] and r1[1] == min_[1]:
            A = max_[0] - mid_[0], max_[1] - min_[1], 1
            B = mid_[0] - min_[0], max_[1] - min_[1], 1
            C = max_[0] - mid_[0], mid_[1] - min_[1], -1
            D = mid_[0] - min_[0], mid_[1] - min_[1], -1
        # receiver out, within 1st quadrant
        elif r1[0] == max_[0] and r1[1] == max_[1]:
            A = max_[0] - min_[0], max_[1] - min_[1], 1
            B = max_[0] - mid_[0], max_[1] - mid_[1], 1
            C = max_[0] - mid_[0], max_[1] - min_[1], -1
            D = max_[0] - min_[0], max_[1] - mid_[1], -1
        # receiver out, within 2nd quadrant
        elif r1[0] == max_[0] and r1[1] == min_[1]:
            A = max_[0] - min_[0], max_[1] - min_[1], 1
            B = max_[0] - mid_[0], mid_[1] - min_[1], 1
            C = max_[0] - min_[0], mid_[1] - min_[1], -1
            D = max_[0] - mid_[0], max_[1] - min_[1], -1
        # receiver out, within 3rd quadrant
        elif r1[0] == min_[0] and r1[1] == min_[1]:
            A = max_[0] - min_[0], max_[1] - min_[1], 1
            B = mid_[0] - min_[0], mid_[1] - min_[1], 1
            C = mid_[0] - min_[0], max_[1] - min_[1], -1
            D = max_[0] - min_[0], mid_[1] - min_[1], -1
        # receiver out, within 4th quadrant
        elif r1[0] == min_[0] and r1[1] == max_[1]:
            A = max_[0] - min_[0], max_[1] - min_[1], 1
            B = mid_[0] - min_[0], max_[1] - mid_[1], 1
            C = mid_[0] - min_[0], max_[1] - min_[1], -1
            D = max_[0] - min_[0], max_[1] - mid_[1], -1
        # unkown
        else:
            return math.nan, math.nan, math.nan

    return A, B, C, D


def _test_phi_parallel_any_br187():
    # All testing values are taken from independent sources

    # check receiver at emitter corner
    assert abs(phi_parallel_any_br187(*(10, 10, 0, 0, 10)) - 0.1385316060) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 0, 10, 10)) - 0.1385316060) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 10, 10, 10)) - 0.1385316060) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 10, 0, 10)) - 0.1385316060) < 1e-8

    # check receiver on emitter edge
    assert abs(phi_parallel_any_br187(*(10, 10, 2, 0, 10)) - 0.1638694545) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 2, 10, 10)) - 0.1638694545) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 0, 2, 10)) - 0.1638694545) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 10, 2, 10)) - 0.1638694545) < 1e-8

    # check receiver within emitter, center
    assert abs(phi_parallel_any_br187(*(10, 10, 5, 5, 10)) - 0.2394564705) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 2, 2, 10)) - 0.1954523349) < 1e-8

    # check receiver fall outside, side ways
    assert abs(phi_parallel_any_br187(*(10, 10, 5, 15, 10)) - 0.0843536644) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 5, -5, 10)) - 0.0843536644) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 15, 5, 10)) - 0.0843536644) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, -5, 5, 10)) - 0.0843536644) < 1e-8

    # check receiver fall outside, 1st quadrant
    assert abs(phi_parallel_any_br187(*(10, 10, 20, 15, 10)) - 0.0195607021) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 20, -5, 10)) - 0.0195607021) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, -10, -5, 10)) - 0.0195607021) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, -10, 15, 10)) - 0.0195607021) < 1e-8


def _test_phi_perpendicular_any_br187():
    # All testing values are taken from independent sources

    # check receiver at emitter corner
    assert abs(phi_perpendicular_any_br187(10, 10, 0, 0, 10) - 0.05573419700) < 1e-8

    # check receiver on emitter edge
    assert abs(phi_perpendicular_any_br187(10, 10, 2, 0, 10) - 0.06505816388) < 1e-8
    assert abs(phi_perpendicular_any_br187(10, 10, 2, 10, 10) - 0.06505816388) < 1e-8
    assert abs(phi_perpendicular_any_br187(10, 10, 0, 2, 10) - 0.04656468770) < 1e-8
    assert abs(phi_perpendicular_any_br187(10, 10, 10, 2, 10) - 0.04656468770) < 1e-8

    # check receiver fall outside, side ways
    assert abs(phi_perpendicular_any_br187(10, 10, 5, -10, 10) - 0.04517433814) < 1e-8
    assert abs(phi_perpendicular_any_br187(10, 10, 5, 20, 10) - 0.04517433814) < 1e-8


if __name__ == "__main__":
    _test_phi_perpendicular_any_br187()
    _test_phi_parallel_any_br187()
