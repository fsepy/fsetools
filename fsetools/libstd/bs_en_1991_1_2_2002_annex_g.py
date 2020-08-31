from math import cos, atan, sin, pi


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


if __name__ == '__main__':
    _test_clause_g_3_phi()
