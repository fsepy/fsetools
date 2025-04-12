import math


def eq_A4_phi_parallel_corner(W_m, H_m, S_m, multiplier=1):
    """Equation A4 in BR 187 second edition (2014) calculates view factor from a rectangle corner parallel.

    :param W_m: in m, width of emitter panel
    :param H_m: in m, height of emitter panel
    :param S_m: in m, separation distance from surface to surface
    :param multiplier:
    :return phi: configuration factor
    """

    # Calculate view factor, phi
    X = W_m / S_m
    Y = H_m / S_m
    a = 1 / 2 / math.pi
    b = X / (1 + X ** 2) ** 0.5
    c = math.atan(Y / (1 + X ** 2) ** 0.5)
    d = Y / (1 + Y ** 2) ** 0.5
    e = math.atan(X / (1 + Y ** 2) ** 0.5)
    phi = a * (b * c + d * e)

    return phi * multiplier


def eq_A5_phi_perpendicular_corner(W_m, H_m, S_m, multiplier=1):
    """Equation A5 in BR 187 second edition (2014) calculates view factor from a rectangle corner perpendicular.

    :param W_m: in m, width of emitter panel
    :param H_m: in m, height of emitter panel
    :param S_m: in m, separation distance from surface to surface
    :param multiplier:
    :return phi: configuration factor
    """
    X = W_m / S_m
    Y = H_m / S_m

    a = 1 / 2 / math.pi
    b = math.atan(X)
    c = 1 / (Y ** 2 + 1) ** 0.5
    d = math.atan(X / (Y ** 2 + 1) ** 0.5)

    phi = a * (b - c * d)

    return phi * multiplier
