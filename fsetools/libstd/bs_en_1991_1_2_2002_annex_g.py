from math import cos, atan, sin, pi
import numpy as np


def clause_g_3_phi(w, h, s, theta):
    """
    Clause G.3, page 57
    :param w:
    :param h:
    :param s:
    :param theta:
    :return:
    """

    a = h / s
    b = w / s

    # Equation G.4, page 57
    aa = atan(a)
    bb = (1 - b * cos(theta)) / ((1 + b ** 2 - 2 * b * cos(theta))) ** 0.5
    cc = atan((a) / ((1 + b ** 2 - 2 * b * cos(theta)) ** 0.5))
    dd = (a * cos(theta)) / ((a ** 2 + (sin(theta)) ** 2) ** 0.5)
    ee = atan((b - cos(theta)) / ((a ** 2 + (sin(theta)) ** 2) ** 0.5))
    ff = atan(cos(theta) / ((a ** 2 + (sin(theta)) ** 2) ** 0.5))

    phi = 1 / (2 * pi) * (aa - bb * cc + dd * (ee + ff))

    _latex = [
        f'\\phi=\\frac{{1}}{{2\\pi}} \\left(\\arctan\\left(a\\right)-\\frac{{1-b cos\\left(\\theta\\right)}}{{{{\\left(1+b^2-2b cos\\left(\\theta\\right)\\right)}}^{{0.5}}}} \\arctan\\left(\\frac{{a}}{{{{\\left(1+b^2-2b cos\\left(\\theta\\right)\\right)}}^{{0.5}}}}\\right)+\\frac{{a cos\\left(\\theta\\right)}}{{{{\\left(a^2+{{sin\\left(\\theta\\right)}}^2\\right)}}^{{0.5}}}} \\left(\\arctan\\left(\\frac{{b-cos\\left(\\theta\\right)}}{{{{\\left(a^2+{{sin\\left(\\theta\\right)}}^2\\right)}}^{{0.5}}}}\\right)+\\arctan\\left(\\frac{{cos\\left(\\theta\\right)}}{{{{\\left(a^2+{{sin\\left(\\theta\\right)}}^2\\right)}}^{{0.5}}}}\\right)\\right)\\right)',
        f'\\phi=\\frac{{1}}{{2\\pi}} \\left(\\arctan\\left({a:.2f}\\right)-\\frac{{1-{b:.2f} cos\\left({theta:.2f}\\right)}}{{{{\\left(1+{b:.2f}^2-2\\cdot {b:.2f} cos\\left({theta:.2f}\\right)\\right)}}^{{0.5}}}} \\arctan\\left(\\frac{{{a:.2f}}}{{{{\\left(1+{b:.2f}^2-2\\cdot {b:.2f} cos\\left({theta:.2f}\\right)\\right)}}^{{0.5}}}}\\right)+\\frac{{{a:.2f} cos\\left({theta:.2f}\\right)}}{{{{\\left({a:.2f}^2+{{sin\\left({theta:.2f}\\right)}}^2\\right)}}^{{0.5}}}} \\left(\\arctan\\left(\\frac{{{b:.2f}-cos\\left({theta:.2f}\\right)}}{{{{\\left({a:.2f}^2+{{sin\\left({theta:.2f}\\right)}}^2\\right)}}^{{0.5}}}}\\right)+\\arctan\\left(\\frac{{cos\\left({theta:.2f}\\right)}}{{{{\\left({a:.2f}^2+{{sin\\left({theta:.2f}\\right)}}^2\\right)}}^{{0.5}}}}\\right)\\right)\\right)',
        f'\\phi={phi:.4f}\\ \\left[-\\right]',
    ]

    return dict(phi=phi, _latex=_latex)


def _test_clause_g_3_phi():
    res = clause_g_3_phi(w=6, h=10, s=2, theta=pi / 2)

    print(res['phi'])
    [print(i) for i in res['_latex']]


class Phi:
    def __init__(self):
        pass

    @staticmethod
    def rotation_matrix_2d(theta: float):
        """

        :param theta: [rad] is the angle in radian
        :return R: [-] is the 2 dimensional rotation matrix
        """
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))
        return R

    @staticmethod
    def clause_5_c(theta: float, w: float, h: float, s: float) -> float:
        """

        :param theta:   [rad]   is the internal angle between emitter and receiver
        :param w:       [m]     is the emitter width
        :param h:       [m]     is the emitter height
        :param s:       [m]     is the separation between emitter and receiver
        :return Phi:    [-]     is the configuration factor
        """

        a = h / s
        b = w / s

        aa = atan(a)
        bb = (1 - b * cos(theta)) / ((1 + b ** 2 - 2 * b * cos(theta)) ** 0.5)
        cc = atan(a / ((1 + b ** 2 - 2 * b * cos(theta)) ** 0.5))
        dd = (a * cos(theta)) / ((a ** 2 + sin(theta) ** 2) ** 0.5)
        ee = atan((b - cos(theta)) / ((a ** 2 + sin(theta) ** 2) ** 0.5))
        ff = atan((cos(theta) / ((a ** 2 + sin(theta) ** 2) ** 0.5)))

        Phi_ = 1 / (2 * pi) * (aa - bb * cc + dd * (ee + ff))

        return Phi_

    @staticmethod
    def __clause_5_c(phi: float, a: float, b: float, c: float) -> float:
        """
        Configuration factor for rectangular emitter and receiver at an angle phi as per Clause 5 c. NB the equation defined in BS EN 1991-1-2 might be incorrect as only three
        variables are present. Equation from SFPE p. 3479 is used.

        :param phi: [rad]   is the internal angle between emitter and receiver
        :param a:   [m]     is the emitter width
        :param b:   [m]     is the emitter height
        :param c:   [m]     is the separation between emitter and receiver
        :return F:  [-]     is the configuration factor
        """
        N = a / b
        L = c / b
        V = 1 / (N ** 2 + L ** 2 - 2 * N * L * cos(phi))
        W = (1 + (L ** 2) * (sin(phi) ** 2)) ** 0.5

        aa = atan(1 / L)
        bb = V * (N * cos(phi) - L) * atan(V)
        cc = cos(phi) / W
        dd = atan((N - L * cos(phi)) / W)
        ee = atan((L * cos(phi) / W))

        F = 1/2/pi * (aa + bb + cc * (dd + ee))

        return F


if __name__ == '__main__':
    # _test_clause_g_3_phi()

    N = (1, -1)  # normal of
    x, y = 1, 1

    # Validation conditions
    # The angle between receiver and emitter should be greater than 0 and less than 90 degrees
    assert -90 < np.arctan2(N[1], N[0]) * 180 / np.pi < 0
    N = np.reshape(N, newshape=(2, 1))
    R = Phi.rotation_matrix_2d(0.5 * np.pi)
    print(R)
    N_ = np.dot(R, N)
    print(N_)
    a = N_[0, 0] / N_[1, 0]
    print(f'a={a}')
    # y = a x + b
    # b = y - a * x
    b = y - a * x
    print(f'b={b}')

    y_ = 0
    x_ = (y_ - b) / a
    print(x_, np.isclose(x_, 0))
