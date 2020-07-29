from math import e

from scipy.optimize import bisect

from fsetools.lib.fse_thermal_radiation import phi_parallel_any_br187, phi_perpendicular_any_br187

SYMBOLS = dict(
    I_Z_i=('kW/m**2', 'radiative heat flux from the flame to column face $i$'),
    d_i=('-', 'the cross-sectional dimension of member face $i$'),
    epsilon_Z_i=('-', 'emissivity of the flames with respect to face $i$ of the column'),
    C_i=('-', 'protection coefficient of member face'),
    I_z=('kW/m**2', 'the radiative heat flux from a flame'),
    I_f=('kW/m**2', 'the radiative heat flux from an opening'),
    alpha=('kW/(m**2*K)', 'convective heat transfer coefficient'),
    sigma=('kW/(m**2*K**4)', 'Stefan Boltzmann constant'),
    T_o=('K', 'flame temperature at the opening from annex B of EN 1991-1-2'),
    T_z=('K', 'flame temperature'),
    C_1=('-', 'protection coefficient of member face 1'),
    C_2=('-', 'protection coefficient of member face 2'),
    C_3=('-', 'protection coefficient of member face 3'),
    C_4=('-', 'protection coefficient of member face 4'),
    d_1=('m', 'the cross-sectional dimension of member face 1'),
    d_2=('m', 'the cross-sectional dimension of member face 2'),
    w_t=('m', 'the width of the opening'),
    L_L=("m", "flame height (from the upper part of the window)"),
    L_H=("m", "horizontal projection of the flame (from the facade)"),
    h_eq=('m', 'weighted average of window heights on all wall ${\\textstyle \\sum_{i}}\\left(A_{v,i}h_i\\right)/A_v$'),
    is_forced_draught=('boolean', 'True if forced draught, False otherwise'),
    w_f=('m', 'flame width'),
    a_z=('-', 'the absorptivity of flames'),
    epsilon_f=('-', 'the emissivity of an opening'),
    lambda_1=('m', 'the flame thickness relevant to member face 1'),
    lambda_2=('m', 'the flame thickness relevant to member face 2'),
    lambda_3=('m', 'the flame thickness relevant to member face 3'),
    lambda_4=('m', 'the flame thickness relevant to member face 4'),
    phi_f_1=('-', 'the configuration factor of member face 1 for an opening'),
    phi_f_2=('-', 'the configuration factor of member face 2 for an opening'),
    phi_f_3=('-', 'the configuration factor of member face 3 for an opening'),
    phi_f_4=('-', 'the configuration factor of member face 4 for an opening'),
    epsilon_z_1=('-', 'the total emissivity of the flames on side 1'),
    epsilon_z_2=('-', 'the total emissivity of the flames on side 2'),
    epsilon_z_3=('-', 'the total emissivity of the flames on side 3'),
    epsilon_z_4=('-', 'the total emissivity of the flames on side 4'),
    I_z_1=('kW/m**2', 'the radiative heat flux from a flame to a column face 1'),
    I_z_2=('kW/m**2', 'the radiative heat flux from a flame to a column face 2'),
    I_z_3=('kW/m**2', 'the radiative heat flux from a flame to a column face 3'),
    I_z_4=('kW/m**2', 'the radiative heat flux from a flame to a column face 4'),
    l=('m', 'a distance from an opening, measured along the flame axis'),
    T_f=('K', 'temperature of the fire compartment'),
    T_m=('K', 'the average temperature of the steel member')
)
UNITS = {k: v[0] for k, v in SYMBOLS.items()}
DESCRIPTIONS = {k: v[1] for k, v in SYMBOLS.items()}


def clause_b_1_3_3_T_m(
        I_z,
        I_f,
        alpha,
        T_z,
        sigma: float = 56.7e-12,
        *_,
        **__
):
    """

    :param I_z:
    :param I_f:
    :param alpha:
    :param sigma:
    :return:
    """

    def func(
            T_m_,
            I_z_,
            I_f_,
            alpha_,
            T_z_,
            sigma_: float = 56.7e-12
    ):
        return I_z_ + I_f_ + alpha_ * T_z_ - sigma_ * T_m_ ** 4 - alpha_ * T_m_

    T_m = bisect(func, 0.001, 5000, (I_z, I_f, alpha, T_z, sigma))

    _latex = (
        f'\\sigma\\cdot T_{{m}}^4 + \\alpha\\cdot T_{{m}} = I_{{z}} + I_{{f}} + \\alpha\\cdot T_{{z}}',
        f'\\left({sigma:.2E}\\right)\\cdot T_m^4 + {alpha:.2f}\\cdot T_m = {I_z:.2f} + {I_f:.2f} + {alpha:.2f}\\cdot {T_z:.2f}',
        f'T_m={T_m:.2f}\\ \\left[K\\right]',
        f'T_m={T_m - 273.15:.2f}\\ \\left[^\\circ C\\right]',
    )

    return dict(T_m=T_m, _latex=_latex)


def _test_clause_b_1_3_3_T_m():
    res = clause_b_1_3_3_T_m(I_z=1000, I_f=1500, alpha=25, T_z=293.15)
    T_m = res['T_m']
    assert abs(T_m - 393.0958452) <= 1e-5


def clause_b_1_3_5_I_f(
        phi_f,
        a_z,
        sigma,
        T_f,
        epsilon_f: float = 1,
        *_,
        **__
):
    """
    Clause B.4 (5), page 49

    :param phi_f:
    :param epsilon_f:
    :param a_z:
    :param sigma:
    :param T_f:
    :param _:
    :param __:
    :return:
    """

    # Equation B.3, page 19
    I_f = phi_f * epsilon_f * (1 - a_z) * sigma * T_f ** 4

    _latex = [
        f'I_f=\\phi_f \\cdot \\varepsilon_f \\cdot \\left(1-a_z\\right) \\cdot \\sigma {{T_f}}^4',
        f'I_f={phi_f:.2f} \\cdot {epsilon_f:.2f} \\cdot \\left(1-{a_z:.2f}\\right) \\cdot \\left({sigma:.2E}\\right) \\cdot {{{T_f:.2f}}}^4',
        f'I_f={I_f:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_f=I_f, _latex=_latex)


def clause_b_4_2_epsilon_z_i(lambda_1, lambda_2, lambda_3, lambda_4, *_, **__):
    """
    Clause B.4 (2), page 61
    Emissivity of the external flames for each of the faces 1, 2, 3 and 4 of the column

    :param lambda_1:
    :param lambda_2:
    :param lambda_3:
    :param lambda_4:
    :param _:
    :param __:
    :return:
    """
    epsilon_z_1 = 1 - e ** (-0.3 * lambda_1)
    epsilon_z_2 = 1 - e ** (-0.3 * lambda_2)
    epsilon_z_3 = 1 - e ** (-0.3 * lambda_3)
    epsilon_z_4 = 1 - e ** (-0.3 * lambda_4)

    _latex = [
        f'\\varepsilon_{{z,1}}=1-e^{{-0.3\\cdot \\lambda_1}}=1-e^{{-0.3\\cdot {lambda_1:.2f}}}={epsilon_z_1:.5f}\\ \\left[ -\\right]',
        f'\\varepsilon_{{z,2}}=1-e^{{-0.3\\cdot \\lambda_2}}=1-e^{{-0.3\\cdot {lambda_2:.2f}}}={epsilon_z_2:.5f}\\ \\left[ -\\right]',
        f'\\varepsilon_{{z,3}}=1-e^{{-0.3\\cdot \\lambda_3}}=1-e^{{-0.3\\cdot {lambda_3:.2f}}}={epsilon_z_3:.5f}\\ \\left[ -\\right]',
        f'\\varepsilon_{{z,4}}=1-e^{{-0.3\\cdot \\lambda_4}}=1-e^{{-0.3\\cdot {lambda_4:.2f}}}={epsilon_z_4:.5f}\\ \\left[ -\\right]',
    ]

    return dict(epsilon_z_1=epsilon_z_1, epsilon_z_2=epsilon_z_2, epsilon_z_3=epsilon_z_3, epsilon_z_4=epsilon_z_4,
                _latex=_latex)


def clause_b_1_3_2_d(d_1, d_2, *_, **__):
    # page 47

    d = (d_1 + d_2) / 2
    _latex = [
        f'd=d_{{eq}}=\\frac{{\\left( d_1+d_2\\right)}}{{2}}',
        f'd=d_{{eq}}=\\frac{{\\left( {d_1:.2f}+{d_2:.2f}\\right)}}{{2}}',
        f'd=d_{{eq}}={d:.2f}\\ \\left[ m\\right]',
    ]

    return dict(d=d, _latex=_latex)


def clause_b_1_4_1_phi_f_i(h_eq, d_2, lambda_1, lambda_2, lambda_3, *_, **__):
    phi_f_1 = phi_perpendicular_any_br187(
        W_m=h_eq,
        H_m=lambda_1,
        w_m=0.5 * h_eq,
        h_m=0,
        S_m=lambda_3,
    )
    phi_f_2 = phi_perpendicular_any_br187(
        W_m=h_eq,
        H_m=lambda_2,
        w_m=0.5 * h_eq,
        h_m=0,
        S_m=lambda_3,
    )
    phi_f_3 = phi_parallel_any_br187(
        W_m=lambda_1 + lambda_2 + d_2,
        H_m=h_eq,
        w_m=lambda_1 + 0.5 * d_2,
        h_m=0.5 * h_eq,
        S_m=lambda_3
    )
    phi_f_4 = 0

    _latex = [
        f'\\phi_{{f,1}}={phi_f_1:.5f}\\ \\left[-\\right]',
        f'\\phi_{{f,2}}={phi_f_2:.5f}\\ \\left[-\\right]',
        f'\\phi_{{f,3}}={phi_f_3:.5f}\\ \\left[-\\right]',
        f'\\phi_{{f,4}}={phi_f_4:.5f}\\ \\left[-\\right]',
    ]

    return dict(phi_f_1=phi_f_1, phi_f_2=phi_f_2, phi_f_3=phi_f_3, phi_f_4=phi_f_4, _latex=_latex)


def clause_b_1_4_1_phi_f(
        C_1, C_2, C_3, C_4,
        phi_f_1, phi_f_2, phi_f_3, phi_f_4,
        d_1, d_2,
        *_, **__
):
    """
    Clause B.1.4 (1), page 50
    Overall configuration factor of a member for radiative heat transfer from an opening.

    :param C_1:
    :param C_2:
    :param C_3:
    :param C_4:
    :param phi_f_1:
    :param phi_f_2:
    :param phi_f_3:
    :param phi_f_4:
    :param d_1:
    :param d_2:
    :param _:
    :param __:
    :return:
    """

    # Equation B.4, page 50
    a = (C_1 * phi_f_1 + C_2 * phi_f_2) * d_1
    b = (C_3 * phi_f_3 + C_4 * phi_f_4) * d_2
    c = (C_1 + C_2) * d_1
    d = (C_3 + C_4) * d_2
    phi_f = (a + b) / (c + d)

    _latex = [
        f'\\phi_f=\\frac{{\\left(C_1 \\phi_{{f,1}}+C_2 \\phi_{{f,2}}\\right) d_1+\\left(C_3 \\phi_{{f,3}}+C_4 \\phi_{{f,4}}\\right) d_2}}{{\\left(C_1+C_2\\right) d_1+\\left(C_3+C_4\\right) d_2}}',
        f'\\phi_f=\\frac{{\\left({C_1:.1f}\\cdot {phi_f_1:.5f}+{C_2:.1f}\\cdot {phi_f_2:.5f}\\right) {d_1:.2f}+\\left({C_3:.1f} \\cdot {phi_f_3:.5f}+{C_4:.1f}\\cdot {phi_f_4:.5f}\\right) {d_2:.2f}}}{{\\left({C_1:.1f}+{C_2:.1f}\\right) {d_1:.2f}+\\left({C_3:.1f}+{C_4:.1f}\\right) {d_2:.2f}}}',
        f'\\phi_f={phi_f:.2f}\\ \\left[-\\right]',
    ]

    return dict(phi_f=phi_f, _latex=_latex)


def clause_b_4_1_I_z_i(
        C_1, C_2, C_3, C_4,
        epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4,
        sigma,
        T_z,
        T_o,
        *_, **__
):
    """
    Clause B.4 (1), page 59
    Radiative heat flux of the external flames for each of the faces 1, 2, 3 and 4 of the column

    :param C_1:
    :param C_2:
    :param C_3:
    :param C_4:
    :param epsilon_z_1:
    :param epsilon_z_2:
    :param epsilon_z_3:
    :param epsilon_z_4:
    :param sigma:
    :param T_z:
    :param T_o:
    :param _:
    :param __:
    :return:
    """
    # Equation B.18, page 59
    I_z_1 = C_1 * epsilon_z_1 * sigma * T_z ** 4
    I_z_2 = C_2 * epsilon_z_2 * sigma * T_z ** 4
    I_z_3 = C_3 * epsilon_z_3 * sigma * T_o ** 4
    I_z_4 = C_4 * epsilon_z_4 * sigma * T_z ** 4

    _latex = [
        f'I_{{z,1}}=C_1\\cdot \\varepsilon_{{z,1}}\\cdot \\sigma\\cdot T_z^4={C_1:.2f}\\cdot {epsilon_z_1:.5f}\\cdot \\left( {sigma:.2E}\\right) \\cdot {T_z:.2f}^4={I_z_1:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,2}}=C_2\\cdot \\varepsilon_{{z,2}}\\cdot \\sigma\\cdot T_z^4={C_2:.2f}\\cdot {epsilon_z_2:.5f}\\cdot \\left( {sigma:.2E}\\right) \\cdot {T_z:.2f}^4={I_z_2:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,3}}=C_3\\cdot \\varepsilon_{{z,3}}\\cdot \\sigma\\cdot T_o^4={C_3:.2f}\\cdot {epsilon_z_3:.5f}\\cdot \\left( {sigma:.2E}\\right) \\cdot {T_o:.2f}^4={I_z_3:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,4}}=C_4\\cdot \\varepsilon_{{z,4}}\\cdot \\sigma\\cdot T_z^4={C_4:.2f}\\cdot {epsilon_z_4:.5f}\\cdot \\left( {sigma:.2E}\\right) \\cdot {T_z:.2f}^4={I_z_4:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_z_1=I_z_1, I_z_2=I_z_2, I_z_3=I_z_3, I_z_4=I_z_4, _latex=_latex)


def clause_b_4_1_I_z(
        C_1, C_2, C_3, C_4,
        I_z_1, I_z_2, I_z_3, I_z_4,
        d_1, d_2,
        *_, **__
):
    """
    Clause B.4 (1), page 59

    :param C_1:
    :param C_2:
    :param C_3:
    :param C_4:
    :param epsilon_z_1:
    :param epsilon_z_2:
    :param epsilon_z_3:
    :param epsilon_z_4:
    :param sigma:
    :param T_z:
    :param T_o:
    :param d_1:
    :param d_2:
    :param _:
    :param __:
    :return:
    """

    a = (I_z_1 + I_z_2) * d_1
    b = (I_z_3 + I_z_4) * d_2
    c = (C_1 + C_2) * d_1
    d = (C_3 + C_4) * d_2
    I_z = (a + b) / (d + c)

    _latex = [
        f'I_z=\\frac{{\\left(I_{{z,1}}+I_{{z,2}}\\right) d_1+\\left(I_{{z,3}}+I_{{z,4}}\\right) d_2}}{{\\left(C_1+C_2\\right) d_1+\\left(C_3+C_4\\right) d_2}}',
        f'I_z=\\frac{{\\left({I_z_1:.2f}+{I_z_2:.2}\\right) {d_1:.2f}+\\left({I_z_3:.2f}+{I_z_4:.2f}\\right) {d_2:.2f}}}{{\\left({C_1:.2f}+{C_2:.2f}\\right) {d_1:.2f}+\\left({C_3:.2f}+{C_4:.2f}\\right) {d_2:.2f}}}',
        f'I_z={I_z:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_z=I_z, _latex=_latex)


def clause_b_4_1_lambda_2(w_t, lambda_1, d_2, *_, **__):
    lambda_2 = w_t - lambda_1 - d_2

    _latex = [
        f'\\lambda_2=w_t-\\lambda_1-d_2',
        f'\\lambda_2={w_t:.2f}-{lambda_1:.2f}-{d_2:.2f}',
        f'\\lambda_2={lambda_2:.2f}\\ \\left[ m \\right]',
    ]

    return dict(lambda_2=lambda_2, _latex=_latex)


def clause_b_4_1_lambda_4(lambda_3, L_L, L_H, h_eq, d_1, is_forced_draught: bool, *_, **__, ):
    _latex = [
        f'\\lambda_4=\n'
        f'\\begin{{dcases}}\n'
        f'\\operatorname{{max}}\\left(0, L_H-\\lambda_3-d_1\\right),    &\\text{{if no forced draught }} \\left[ {not is_forced_draught}\\right]\\\\\n'
        f'\\frac{{0.5h_{{eq}} L_H}}{{L_L}},                             & \\text{{if forced draught }} \\lambda_3 \\frac{{L_L}}{{L_H}} \\le 0.5 h_{{eq}} \\ \\left[ {is_forced_draught and lambda_3 * L_L / L_H <= 0.5 * h_eq}\\right]\\\\\n'
        f'\\frac{{h_{{eq}} L_H}}{{L_L}}-d_1-\\lambda_3,                 & \\text{{if forced draught }} \\lambda_3 \\frac{{L_L}}{{L_H}} > 0.5 h_{{eq}} \\ \\left[ {is_forced_draught and lambda_3 * L_L / L_H > 0.5 * h_eq}\\right]\\\\\n'
        f'\\end{{dcases}}'
    ]

    # Figure B.6, page 60
    if is_forced_draught:
        # if forced draught
        if lambda_3 * L_L / L_H <= 0.5 * h_eq:
            # if the engulfed steel column center point is below the opening soffit
            lambda_4 = 0.5 * h_eq * L_H / L_L
            _latex.extend([
                f'\\lambda_4=\\frac{{0.5h_{{eq}} L_H}}{{L_L}}',
                f'\\lambda_4=\\frac{{0.5\\cdot {h_eq:.2f}\\cdot {L_H:.2f}}}{{{L_L:.2f}}}',
            ])
        elif lambda_3 * L_L / L_H > 0.5 * h_eq:
            # if the engulfed steel column center point is above the opening soffit
            lambda_4 = h_eq * L_H / L_L - d_1 - lambda_3
            _latex.extend([
                f'\\lambda_4=\\frac{{h_{{eq}} L_H}}{{L_L}}-d_1-\\lambda_3',
                f'\\lambda_4=\\frac{{{h_eq:.2f}\\cdot {L_H:.2f}}}{{{L_L:.2f}}}-{d_1:.2f}-{lambda_3:.2f}',
            ])
        else:
            raise ValueError('This error shouldn\'t be possible')
    else:
        # if not forced draught
        lambda_4 = max(0, L_H - lambda_3 - d_1)
        _latex.extend([
            f'\\lambda_4=\\operatorname{{max}}\\left(0, L_H-\\lambda_3-d_1\\right)',
            f'\\lambda_4=\\operatorname{{max}}\\left(0, {L_H:.2f}-{lambda_3:.2f}-{d_1:.2f}\\right)',
        ])

    _latex.extend([f'\\lambda_4={lambda_4:.2f}\\ \\left[m\\right]'])

    return dict(lambda_4=lambda_4, _latex=_latex)


def _test_clause_b_4_1_lambda_4():
    res = clause_b_4_1_lambda_4(
        lambda_3=1,
        L_L=2.7,
        L_H=6.71,
        h_eq=3.3,
        d_1=0.8,
        is_forced_draught=True
    )
    assert abs(res['lambda_4'] - 4.1) < 1e-3


def clause_b_4_5_l(h_eq, L_H, L_L, lambda_3, d_1, is_forced_draught, *_, **__):
    """
    Clause B.4 (5), page 61
    :param h_eq:
    :param _:
    :param __:
    :return:
    """

    _latex = [
        f'l=\n'
        f'\\begin{{dcases}}\n'
        f'\\frac{{h_{{eq}}}}{{2}},                                                                                                      & \\text{{if no forced draught}}\\ \\left[{not is_forced_draught}\\right]\\\\\n'
        f'\\operatorname{{min}}\\left(\\frac{{\\left(\\lambda_3+0.5d_1\\right) L_L}}{{L_H}},\\frac{{0.5h_{{eq}} L_L}}{{L_H}}\\right),   & \\text{{if forced draught}}\\ \\left[{is_forced_draught}\\right]\\\\\n'
        f'\\end{{dcases}}'
    ]

    if not is_forced_draught:
        # Equation B.19a
        # note, original equation `l = h / 2`
        l = h_eq / 2

        _latex.extend([
            f'l=\\frac{{{h_eq:.2f}}}{{2}}',
        ])
    else:
        # Equation B.19b
        # todo, the equation below is not exactly the same as Equation B.19b in BS EN 1993-1-2.
        # todo, make sure the interpretation below is correct.
        # note, original equation `l = (lambda_3 + 0.5 * d_1) * L_L / L_H` and `l <= 0.5 * h_eq * L_L / L_H`
        l = min((lambda_3 + 0.5 * d_1) * L_L / L_H, 0.5 * h_eq * L_L / L_H)

        _latex.extend([
            f'l=\\operatorname{{min}}\\left(\\frac{{\\left({lambda_3:.2f}+0.5\\cdot {d_1:.2f}\\right) {L_L:.2f}}}{{{L_H:.2f}}}, \\frac{{0.5\\cdot {h_eq:.2f}\\cdot {L_L:.2f}}}{{{L_H:.2f}}}\\right)',
            f'l=\\operatorname{{min}}\\left({(lambda_3 + 0.5 * d_1) * L_L / L_H:.2f}, {0.5 * h_eq * L_L / L_H:.2f}\\right)',
        ])

    _latex.extend([
        f'l={l:.2f}\\ \\left[ m\\right]'
    ])

    return dict(l=l, _latex=_latex)


def clause_b_4_6_a_z(epsilon_z_1, epsilon_z_2, epsilon_z_3, *_, **__):
    """
    Clause B.4 (6), page 61

    :param epsilon_z_1:
    :param epsilon_z_2:
    :param epsilon_z_3:
    :param _:
    :param __:
    :return:
    """

    # Equation B.20
    a_z = (epsilon_z_1 + epsilon_z_2 + epsilon_z_3) / 3

    _latex = [
        f'a_z=\\frac{{\\varepsilon_{{z,1}}+\\varepsilon_{{z,2}}+\\varepsilon_{{z,3}}}}{{3}}',
        f'a_z=\\frac{{{epsilon_z_1:.2f}+{epsilon_z_2:.2f}+{epsilon_z_3:.2f}}}{{3}}',
        f'a_z={a_z:.5f}\\ \\left[-\\right]'
    ]

    return dict(a_z=a_z, _latex=_latex)


if __name__ == '__main__':
    _test_clause_b_1_3_3_T_m()
    _test_clause_b_4_1_lambda_4()
