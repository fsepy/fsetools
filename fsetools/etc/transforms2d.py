import math
from typing import Union

import numpy as np


def unit_vector(vector: np.ndarray):
    """ Returns the unit vector of the vector. """
    return vector / np.linalg.norm(vector)


def angle_between_two_vectors_2d(v1: Union[list, tuple, np.ndarray], v2: Union[list, tuple, np.ndarray]) -> float:
    """ Returns the angle in radians between vectors 'v1' and 'v2' """
    # v1_u = v1 / np.linalg.norm(v1)
    # v2_u = v2 / np.linalg.norm(v2)
    # r = np.arccos2(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    ang1 = np.arctan2(*np.array(v1)[::-1])
    ang2 = np.arctan2(*np.array(v2)[::-1])
    r = (ang1 - ang2) % (2 * np.pi)

    return r


def rotation_meshgrid(xx: np.ndarray, yy: np.ndarray, theta_in_radians: float):
    """Rotate a mesh grid by angle theta_in_radians.

    :param xx: x values of a mesh grid.
    :param yy: y values of a mesh grid.
    :param theta_in_radians: the angle to be rotated.
    :return (xx2, yy2): rotated arrays.
    """

    # Clockwise, 2D rotation_meshgrid matrix
    R = rotation_matrix(theta_in_radians)

    return np.einsum('ji, mni -> jmn', R, np.dstack([xx, yy]))


def rotation_matrix(theta_in_radians: float):
    # Clockwise, 2D rotation_meshgrid matrix

    R = np.array(
        [
            [np.cos(theta_in_radians), np.sin(theta_in_radians)],
            [-np.sin(theta_in_radians), np.cos(theta_in_radians)]]
    )

    return R


def find_line_segment_intersection_1(pt1, pt2, ptA, ptB):
    """ this returns the intersection of Line(pt1,pt2) and Line(ptA,ptB)

        returns a tuple: (xi, yi, valid, r, s), where
        (xi, yi) is the intersection
        r is the scalar multiple such that (xi,yi) = pt1 + r*(pt2-pt1)
        s is the scalar multiple such that (xi,yi) = pt1 + s*(ptB-ptA)
            valid == 0 if there are 0 or inf. intersections (invalid)
            valid == 1 if it has a unique intersection ON the segment    """

    DET_TOLERANCE = 0.00000001

    # the first line is pt1 + r*(pt2-pt1)
    # in component form:
    x1, y1 = pt1
    x2, y2 = pt2
    dx1 = x2 - x1
    dy1 = y2 - y1

    # the second line is ptA + s*(ptB-ptA)
    x, y = ptA;
    xB, yB = ptB
    dx = xB - x;
    dy = yB - y

    # we need to find the (typically unique) values of r and s
    # that will satisfy
    #
    # (x1, y1) + r(dx1, dy1) = (x, y) + s(dx, dy)
    #
    # which is the same as
    #
    #    [ dx1  -dx ][ r ] = [ x-x1 ]
    #    [ dy1  -dy ][ s ] = [ y-y1 ]
    #
    # whose solution is
    #
    #    [ r ] = _1_  [  -dy   dx ] [ x-x1 ]
    #    [ s ] = DET  [ -dy1  dx1 ] [ y-y1 ]
    #
    # where DET = (-dx1 * dy + dy1 * dx)
    #
    # if DET is too small, they're parallel
    #
    DET = (-dx1 * dy + dy1 * dx)

    if math.fabs(DET) < DET_TOLERANCE: return (0, 0, 0, 0, 0)

    # now, the determinant should be OK
    DETinv = 1.0 / DET

    # find the scalar amount along the "self" segment
    r = DETinv * (-dy * (x - x1) + dx * (y - y1))

    # find the scalar amount along the input line
    s = DETinv * (-dy1 * (x - x1) + dx1 * (y - y1))

    # return the average of the two descriptions
    xi = (x1 + r * dx1 + x + s * dx) / 2.0
    yi = (y1 + r * dy1 + y + s * dy) / 2.0
    return (xi, yi, 1, r, s)


def find_line_segment_intersection_2(p0, p1, p2, p3):
    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1]

    denom = s10_x * s32_y - s32_x * s10_y

    if denom == 0: return None  # collinear

    denom_is_positive = denom > 0

    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]

    s_numer = s10_x * s02_y - s10_y * s02_x

    if (s_numer < 0) == denom_is_positive: return None  # no collision

    t_numer = s32_x * s02_y - s32_y * s02_x

    if (t_numer < 0) == denom_is_positive: return None  # no collision

    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive: return None  # no collision

    # collision detected

    t = t_numer / denom

    intersection_point = [p0[0] + (t * s10_x), p0[1] + (t * s10_y)]

    return intersection_point


def points_in_ploy(points_xy: list, poly_xy: list):
    poly_xy_list = list(poly_xy)
    poly_xy_list.append(poly_xy_list[0])

    results = np.full((len(points_xy),), False, dtype=np.bool)

    for i, point in enumerate(points_xy):
        p1 = (-1e100, point[1])
        p2 = (1e100, point[1])

        count_intersection = 0
        for j in range(len(poly_xy_list) - 1):
            p3 = poly_xy_list[j]
            p4 = poly_xy_list[j + 1]

            if find_line_segment_intersection_2(p1, p2, p3, p4):
                count_intersection += 1

        if count_intersection == 2:
            results[i] = True

    return results


def ray_tracing_numpy(x, y, poly):
    n = len(poly)
    inside = np.zeros(len(x), np.bool_)
    p2x = 0.0
    p2y = 0.0
    xints = 0.0
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        idx = np.nonzero((y > min(p1y, p2y)) & (y <= max(p1y, p2y)) & (x <= max(p1x, p2x)))[0]
        if p1y != p2y:
            xints = (y[idx] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
        if p1x == p2x:
            inside[idx] = ~inside[idx]
        else:
            idxx = idx[x[idx] <= xints]
            inside[idxx] = ~inside[idxx]

        p1x, p1y = p2x, p2y
    return inside
