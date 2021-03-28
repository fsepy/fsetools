import numpy as np


def clause_3_equivalent_time(q_f_d: float, k_b: float, w_f: float, k_c: float, **__):
    """
    The equivalent time of standard fire exposure.

    :param q_f_d:   [MJ/m2] is the design fire load density according to annex E
    :param k_b:     [-]     is the conversion factor according to (4)
    :param w_f:     [-]     is the ventilation factor according to (5)
    :param k_c:     [-]     is the correction factor function of the material composing structural cross-sections and defined in Table F.1
    :param __:              Not used
    :return t_e_d:  [min]   is the equivalent time of standard fire exposure
    """
    t_e_d = (q_f_d * k_b * w_f) * k_c
    _latex = [
        f't_{{e,d}} = \\left( q_{{f,d}} \\cdot k_b \\cdot w_f \\right) \\cdot k_c',
        f't_{{e,d}} = {t_e_d} \\ \\left[ min \\right]'
    ]
    return dict(t_e_d=t_e_d, _latex=_latex)


def clause_5_ventilation_factor(H: float, A_f: float, A_t: float, A_v: float, A_h: float, O: float, **__):
    """
    The ventilation factor.

    :param H:   [m]     is the height of the fire compartment
    :param A_f: [m2]    is the floor area of the compartment
    :param A_v: [m2]    is the area of vertical openings in the facade
    :param A_h: [m2]    is the area of horizontal openings in the roof
    :param __:          Not used
    :return w_f:        is the ventilation factor
    """
    _latex = list()

    alpha_v = A_v / A_f
    alpha_h = A_h / A_f
    _latex.append([f'\\alpha_v = \\frac{{A_v}}{{A_f}} = \\frac{A_v}{A_f} = {alpha_v}'])
    _latex.append([f'\\alpha_h = \\frac{{A_h}}{{A_f}} = \\frac{A_h}{A_f} = {alpha_h}'])

    b_v = 12.5 * (1 + 10 * alpha_v - alpha_v ** 2)
    assert b_v >= 10.0
    _latex.append([
        f'b_v = 12.5 \\times \\left( 1 + 10 * \\alpha_v - \\alpha_v ** 2 \\right) = 12.5 \\times \\left( 1 + 10 * {alpha_v} - {alpha_v} ** 2 \\right) = {b_v}'
    ])

    _latex.append([
        f'w_f = \n'
        f'\\begin{{dcases}}\n'
        f'  \\dfrac{{6.0}}{{H}}^{{0.3}} \\times \\left( 0.62 + 90 \\times \\dfrac{{\\left( 0.4 - \\alpha_v \\right) ^ 4}}{{1 + b_v \\times \\alpha_h}} \\right),    & \\text{{if }}A_f\\geq100\\text{{ or openings in the roof}} \\ \\left[{A_h > 0 or A_f >= 100}\\right]\\\\\n'
        f'  O ^ {{-0.5}} \\times \\dfrac{{A_f}}{{A_t}},                                                                                                             & \\text{{if }}A_f<100\\text{{ and no openings in the roof}} \\ \\left[{A_h < 0 and A_f < 100}\\right]\n'
        f'\\end{{dcases}}',
    ])
    if A_h > 0 or A_f > 100:
        w_f = (6.0 / H) ** 0.3 * (0.62 + 90 * (0.4 - alpha_v) ** 4 / (1 + b_v * alpha_h))
        assert w_f >= 0.5
        _latex.append([
            f'w_f = \\frac{{6.0}}{H}^{{0.3}} \\times \\left( 0.62 + 90 \\times \\frac{{\\left( 0.4 - {alpha_v} \\right) ^ 4}}{{1 + {b_v} \\times {alpha_h}}} \\right)',
            f'w_f = {w_f}',
        ])
    else:
        w_f = O ** - 0.5 * A_f / A_t
        _latex.append([
            f'w_f = {O} ^ {{-0.5}} \\times \\frac{A_f}{A_t}',
            f'w_f = {w_f}',
        ])

    return dict(w_f=w_f, _latex=_latex)