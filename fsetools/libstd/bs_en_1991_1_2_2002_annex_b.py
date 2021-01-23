from math import e
from typing import Tuple

"""
This module contains all the equations in Annex B, BS EN 1991-1-2:2002.

A module wide variable :code:`SYMBOLS` is used to take notes all the adopted variable names, their meaning and units. Variable names are largely in accordance with 
Clause 1.6 in EC 1991-1-2:2002 unless otherwise specified in comments. :code:`SIMBOLS` is used for primarily two purposes:

    1. A handy lookup table from variable names and their meanings; and
    2. Used to generate LaTeX table.

`SYMBOLS` is dict object containing dict(variable_name=list(unit, description), ...).

Fire load densities :code:`q_f_k` [MJ/m**2] for different occupancies as per Table E.4 in BS EN 1991-1-2:2002, page 50.

| Occupancy Average        | Average | 80 % fractile* |
|--------------------------|---------|----------------|
| Dwelling                 | 780     | 948            |
| Hospital (room)          | 230     | 280            |
| Hotel (room)             | 310     | 377            |
| Library                  | 1500    | 1824           |
| Office                   | 420     | 511            |
| Classroom of a school    | 285     | 347            |
| Shopping centre          | 600     | 730            |
| Theatre (cinema)         | 300     | 365            |
| Transport (public space) | 100     | 122            |

*Gumbel II distribution

"""

SYMBOLS = dict(
    A_f=('m**2', 'the floor area of the fire compartment'),
    A_t=('m**2', 'the total area of enclosure (walls, ceiling and floor, including openings)'),
    A_v=('m**2', 'the total area of vertical openings on all walls (${\\textstyle \\sum_{i}A_{v,i}}$)'),
    A_v1=('m**2', 'sum of window areas on wall 1'),
    alpha_c=('W/(m**2*K)', 'the coefficient of heat transfer by convection'),
    D=('m', 'the depth of the fire compartment or diameter of the fire'),
    d_eq=('m', 'the geometrical characteristic of an external structural element (diameter or side)'),
    d_f=('m', 'the flame thickness'),
    d_ow=('m', 'the distance to any other window as per Clause B.9 (6) BS EN 1991-1-2:2002'),
    DW_ratio=('-', 'the $D/W$ as per Clause B.2 (2) to (4) Eurocode 1991-1-2:2002'),  # DW_ratio not in EC 1991-1-2:2002, added for convenience of external flame calculation
    epsilon_f=('-', 'the emissivity of flames, of the fire'),
    H=('m', 'the height of the fire compartment or distance between the fire source and the ceiling'),  # modified based on EC 1991-1-2:2002, added compartment height
    h_eq=('m', 'the weighted average of window heights on all wall ${\\textstyle \\sum_{i}}\\left(A_{v,i}h_i\\right)/A_v$'),
    L_1=('m', 'the flame length (angled)'),
    L_c=('m', 'the length of the core'),
    L_f=('m', 'the flame length along axis'),
    L_H=('m', 'the horizontal projection of the flame (from the facade)'),
    L_L=('m', 'the flame height (from the upper part of the window)'),
    L_x=('m', 'the axis length from the window to the point of measurement'),
    O=('m**0.5', r'the opening factor, $\sqrt{h_{eq}} \cdot \frac{A_v}{A_t}$'),
    Omega=('-', '$\\frac{A_f\\cdot q_{fd}}{\\sqrt{A_v\\cdot A_t}}$'),
    Q=('MW', 'the rate of heat release rate'),
    q_fd=('MJ/m**2', 'the design fire load density related to the floor area $A_t$'),
    q_fk=('MJ/m**2', 'the characteristic fire load density related to the floor area to $A_t$'),
    T_0=('K', 'the ambient temperature'),
    T_f=('K', 'the temperature of the fire compartment'),
    T_w=('K', 'the flame temperature at the window'),
    T_z=('K', 'the flame temperature along the axis'),
    tau_F=('s', 'the free burning fire duration'),
    u=('m/s', 'the wind speed'),
    W=('m', 'the width of wall containing window(s) ($W_1$)'),
    W_1=('m', 'the width of wall 1, assumed to contain the greatest window area'),
    W_2=('m', 'the width of the wall perpendicular to wall 1 in the fire compartment'),
    W_c=('m', 'the width of the core'),
    w_f=('m', 'the flame width'),
    w_t=('m', 'the sum of window widths on all walls (${\\textstyle \\sum_{i}}w_i$)'),
)
UNITS = {k: v[0] for k, v in SYMBOLS.items()}
DESCRIPTIONS = {k: v[1] for k, v in SYMBOLS.items()}


def clause_1_6_Omega(
        A_f: float,
        A_t: float,
        A_v: float,
        q_fd: float,
        *_,
        **__
):
    """
    Clause 1.6, page 20

    todo
    :param A_f:
    :param A_t:
    :param A_v:
    :param q_fd:
    :param _:
    :param __:
    :return:
    """
    Omega = A_f * q_fd / (A_v * A_t) ** 0.5
    _latex = [
        '\\Omega = \\frac{A_f \\cdot q_{fd}} {\\sqrt{A_v \\cdot A_t}}',
        f'\\Omega = \\frac{{{A_f:.2f}\\cdot {q_fd:.2f}}} {{\\sqrt{{{A_v:.2f}\\cdot {A_t:.2f}}}}}',
        f'\\Omega = {Omega:.2f}\\ \\left[{{MJ}}\\right]',
    ]
    return dict(Omega=Omega, _latex=_latex)


def clause_b_2_2_DW_ratio(
        W_1,
        W_2,
        *_,
        **__,
):
    """
    Equation B.1, page 33

    :param W_1:
    :param W_2:
    :param _:
    :param __:
    :return:
    """
    DW_ratio = W_2 / W_1

    _latex = [
        f'{{DW}}_{{ratio}} = \n'
        f'\\begin{{dcases}}\n'
        f'  \\dfrac{{W_2}}{{W_1}},                                                     & \\text{{if there are windows in only wall 1}} \\ \\left[{True}\\right]\\\\\n'
        f'  \\dfrac{{W_2}}{{W_1}}\\cdot \\dfrac{{A_{{v1}}}}{{A_v}},                    & \\text{{if there are windows on more than one wall}} \\ \\left[{False}\\right]\\\\\n'
        f'  \\dfrac{{\\left(W_2-L_c\\right) A_{{v1}}}}{{\\left(W_1-W_c\\right) A_v}},  & \\text{{if there is a core in the fire compartment}}\\ \\left[{False}\\right]\n'
        f'\\end{{dcases}}',

        f'{{DW}}_{{ratio}}=\\frac{{W_2}}{{W_1}}',
        f'{{DW}}_{{ratio}}=\\frac{{{W_2:.2f}}}{{{W_1:.2f}}}',
        f'{{DW}}_{{ratio}}={DW_ratio:.2f}',
    ]
    return dict(DW_ratio=DW_ratio, _latex=_latex)


def clause_b_2_3_DW_ratio(
        W_1,
        W_2,
        A_v1,
        A_v,
        *_,
        **__,
):
    """
    Equation B.2, page 33

    :param W_1:
    :param W_2:
    :param A_v1:
    :param A_v:
    :param _:
    :param __:
    :return:
    """
    # equation B.2
    DW_ratio = (W_2 / W_1) * (A_v1 / A_v)
    _latex = [
        f'{{DW}}_{{ratio}} = \n'
        f'\\begin{{dcases}}\n'
        f'  \\dfrac{{W_2}}{{W_1}},                                                     & \\text{{if there are windows in only wall 1}} \\ \\left[{False}\\right]\\\\\n'
        f'  \\dfrac{{W_2}}{{W_1}}\\cdot \\dfrac{{A_{{v1}}}}{{A_v}},                    & \\text{{if there are windows on more than one wall}} \\ \\left[{True}\\right]\\\\\n'
        f'  \\dfrac{{\\left(W_2-L_c\\right) A_{{v1}}}}{{\\left(W_1-W_c\\right) A_v}},  & \\text{{if there is a core in the fire compartment}}\\ \\left[{False}\\right]\n'
        f'\\end{{dcases}}',

        f'{{DW}}_{{ratio}}=\\frac{{W_2}}{{W_1}}\\cdot \\frac{{A_{{v1}}}}{{A_v}}',
        f'{{DW}}_{{ratio}}=\\frac{{{W_2:.2f}}}{{{W_1:.2f}}}\\cdot \\frac{{{A_v1:.2f}}}{{{A_v:.2f}}}',
        f'{{DW}}_{{ratio}}={DW_ratio:.2f}',
    ]
    return dict(DW_ratio=DW_ratio, _latex=_latex)


def clause_b_2_4_DW_ratio(
        W_1,
        W_2,
        L_c,
        W_c,
        A_v1,
        A_v,
        *_,
        **__,
):
    """
    Equation B.3, page 33

    :param W_1:
    :param W_2:
    :param L_c:
    :param W_c:
    :param A_v1:
    :param A_v:
    :param _:
    :param __:
    :return:
    """
    DW_ratio = ((W_2 - L_c) * A_v1) / ((W_1 - W_c) * A_v)

    _latex = [
        f'{{DW}}_{{ratio}} = \n'
        f'\\begin{{dcases}}\n'
        f'  \\dfrac{{W_2}}{{W_1}},                                                     & \\text{{if there are windows in only wall 1}} \\ \\left[{False}\\right]\\\\\n'
        f'  \\dfrac{{W_2}}{{W_1}}\\cdot \\dfrac{{A_{{v1}}}}{{A_v}},                    & \\text{{if there are windows on more than one wall}} \\ \\left[{False}\\right]\\\\\n'
        f'  \\dfrac{{\\left(W_2-L_c\\right) A_{{v1}}}}{{\\left(W_1-W_c\\right) A_v}},  & \\text{{if there is a core in the fire compartment}}\\ \\left[{True}\\right]\n'
        f'\\end{{dcases}}',

        f'{{DW}}_{{ratio}}=\\frac{{\\left(W_2-L_c\\right) A_{{v1}}}}{{\\left(W_1-W_c\\right) A_v}}',
        f'{{DW}}_{{ratio}}=\\frac{{\\left({W_2:.2f}-{L_c:.2f}\\right) {A_v1:.2f}}}{{\\left({W_1:.2f}-{W_c:.2f}\\right) {A_v:.2f}}}',
        f'{{DW}}_{{ratio}}={DW_ratio:.2f}',
    ]
    return dict(DW_ratio=DW_ratio, _latex=_latex)


def clause_b_4_1_1_Q(
        A_f,
        q_fd,
        tau_F,
        O,
        A_v,
        h_eq,
        DW_ratio,
        *_,
        **__,
):
    """
    Equation B.4, page 34. The rate of burning or the rate of heat release.

    :param A_f:
    :param q_fd:
    :param tau_F:
    :param O:
    :param A_v:
    :param h_eq:
    :param DW_ratio:
    :param _:
    :param __:
    :return:
    """
    a = (A_f * q_fd) / tau_F
    b = 3.15 * (1 - e ** (-0.036 / O)) * A_v * (h_eq / (DW_ratio)) ** 0.5
    Q = min(a, b)
    _latex = [
        'Q=\\operatorname{min}\\left(\\frac{A_f\\cdot q_{fd}}{\\tau_F}, 3.15\\left(1-e^{\\frac{-0.036}{O}}\\right) A_v {\\left(\\frac{h_{eq}}{\\frac{D}{W}}\\right)}^{0.5}\\right)',
        f'Q=\\operatorname{{min}}\\left(\\frac{{{A_f:.2f}\\cdot {q_fd:.2f}}}{{{tau_F:.2f}}}, 3.15\\left(1-e^{{\\frac{{-0.036}}{{{O:.2f}}}}}\\right) {A_v:.2f} {{\\left(\\frac{{{h_eq:.2f}}}{{{DW_ratio:.2f}}}\\right)}}^{{0.5}}\\right)',
        f'Q=\\operatorname{{min}}\\left({a:.2f}, {b:.2f}\\right)',
        f'Q={Q:.2f}\\ \\left[MW\\right]',
    ]
    return dict(Q=Q, _latex=_latex)


def clause_b_4_1_2_T_f(
        O,
        Omega,
        T_0: float = 293.15,
        *_,
        **__,
):
    """
    Equation B.5, page 35

    :param O:
    :param Omega:
    :param T_0:
    :param _:
    :param __:
    :return:
    """
    a = 6000 * (1 - e ** (-0.1 / O))
    b = O ** 0.5
    c = (1 - e ** (-0.00286 * Omega))
    d = T_0
    T_f = a * b * c + d

    _latex = [
        'T_f=6000\\left(1-e^{\\frac{-0.1}{O}}\\right) O^{0.5} \\left(1-e^{-0.00286\\Omega}\\right) + T_0',
        f'T_f=6000\\left(1-e^{{\\frac{{-0.1}}{{{O:.2f}}}}}\\right) {O:.2f}^{{0.5}} \\left(1-e^{{-0.00286\\cdot {Omega:.2f}}}\\right) + {T_0:.2f}',
        f'T_f={T_f:.2f}\\ \\left[K\\right]',
        f'T_f={T_f - 273.15:.2f}\\ \\left[^\\circ C\\right]',
    ]
    return dict(T_f=T_f, _latex=_latex)


def clause_b_4_1_3_d_f(
        h_eq,
        *_,
        **__,
):
    # Figure B.2, page 35
    d_f = 2 / 3 * h_eq
    _latex = [
        'd_f=\\frac{2}{3} h_{eq}',
        f'd_f=\\frac{{2}}{{3}} {h_eq:.2f}',
        f'd_f={d_f:.2f}\\ \\left[m\\right]',
    ]
    return dict(d_f=d_f, _latex=_latex)


def clause_b_4_1_3_L_L(
        Q,
        A_v,
        h_eq,
        rho_g=0.45,
        g=9.81,
        *_,
        **__,
):
    # Equation B.6, page 35
    b_ = Q / (A_v * rho_g * (h_eq * g) ** 0.5)
    b = h_eq * (2.37 * b_ ** (2 / 3) - 1)
    L_L = max(0, b)

    _latex = [
        'L_L=\\operatorname{max}\\left(0, h_{eq} \\left(2.37{\\left(\\frac{Q}{A_v \\rho_g {\\left(h_{eq} g\\right)}^{0.5}}\\right)}^{\\frac{2}{3}}-1\\right)\\right)',
        f'L_L=\\operatorname{{max}}\\left(0, {h_eq:.2f} \\left(2.37{{\\left(\\frac{{{Q:.2f}}}{{{A_v:.2f}\\cdot {rho_g:.2f} {{\\left({h_eq:.2f}\\cdot {g:.2f}\\right)}}^{{0.5}}}}\\right)}}^{{\\frac{{2}}{{3}}}}-1\\right)\\right)',
        f'L_L=\\operatorname{{max}}\\left(0, {b:.2f}\\right)',
        f'L_L={L_L:.2f}\\ \\left[m\\right]',
    ]
    return dict(L_L=L_L, _latex=_latex)


def clause_b_4_1_6_L_H(
        h_eq,
        w_t,
        L_L,
        d_ow: float = None,
        is_wall_above_opening: bool = True,
        *_,
        **__,
):
    _latex = [
        f'L_H = '
        f'\\begin{{dcases}}'
        f'\\frac{{{{1}}}}{{3}}\\cdot h_{{eq}},                                                  & \\text{{if }} h_{{eq}}\\leq 1.25\\cdot w_t\\ \\left[{is_wall_above_opening and h_eq <= 1.25 * w_t}\\right]\\\\'
        f'0.3\\cdot h_{{eq}}\\cdot {{\\left(\\frac{{h_{{eq}}}}{{w_t}}\\right)}}^{{0.54}},       & \\text{{if }} h_{{eq}}>1.25\\cdot w_t \\text{{ and }} d_{{ow}}>4\\cdot w_t\\ \\left[{is_wall_above_opening and h_eq > 1.25 * w_t and d_ow > 4 * w_t}\\right]\\\\'
        f'0.454\\cdot h_{{eq}}\\cdot {{\\left(\\frac{{h_{{eq}}}}{{2w_t}}\\right)}}^{{0.54}},    & \\text{{otherwise if wall exist above window}}\\ \\left[{is_wall_above_opening and h_eq > 1.25 * w_t and not d_ow > 4 * w_t}\\right]\\\\'
        f'0.6\\cdot h_{{eq}}\\cdot \\left(\\frac{{L_L}}{{h_{{eq}}}}\\right)^\\frac{{1}}{{3}},    & \\text{{if no wall exist above window}}\\ \\left[{not is_wall_above_opening}\\right]\\\\'
        f'\\end{{dcases}}'
    ]

    if is_wall_above_opening is True:
        if h_eq <= 1.25 * w_t:
            # Equation B.8, page 36
            L_H = h_eq / 3
            _latex.extend([
                'L_H=\\frac{{1}}{3}\\cdot h_{eq}',
                f'L_H=\\frac{{1}}{{3}}\\cdot {h_eq:.2f}',
                f'L_H={L_H:.2f}\\ \\left[m\\right]',
            ])
        elif d_ow is None:
            raise ValueError(f'`d_ow` is required if `h_eq <= 1.25 * w_t` ({h_eq} <= {1.25 * w_t})')
        elif h_eq > 1.25 * w_t and d_ow > 4 * w_t:
            # Equation B.9, page 36
            L_H = 0.3 * h_eq * (h_eq / w_t) ** 0.54
            _latex.extend([
                f'L_H=0.3\\cdot {h_eq:.2f} {{\\left(\\frac{{{h_eq:.2f}}}{{{w_t:.2f}}}\\right)}}^{{0.54}}',
                f'L_H={L_H:.2f}\\ \\left[m\\right]',
            ])
        else:
            # Equation B.10, page 36
            L_H = 0.454 * h_eq * (h_eq / (2 * w_t)) ** 0.54
            _latex.extend([
                f'L_H=0.454\\cdot {h_eq:.2f} {{\\left(\\frac{{{h_eq:.2f}}}{{2\\cdot {w_t:.2f}\\right)}}^{{0.54}}',
                f'L_H={L_H:.2f}\\ \\left[m\\right]',
            ])
    else:
        L_H = 0.6 * h_eq * (L_L / h_eq) ** (1 / 3)
        _latex.extend([
            f'L_H=0.6\\cdot {h_eq:.2f}\\cdot \\left(\\frac{{{L_L:.2f}}}{{{h_eq:.2f}}}\\right)^\\frac{{1}}{{3}}',
            f'L_H={L_H:.2f}\\ \\left[m\\right]',
        ])

    return dict(L_H=L_H, _latex=_latex)


def clause_b_4_1_7_L_f(
        w_t,
        L_L,
        L_H,
        h_eq,
        is_wall_above_opening: bool,
        *_,
        **__,
):
    _latex = [
        f'L_f = '
        f'\\begin{{dcases}}'
        f'L_L+\\frac{{h_{{eq}}}}{{2}},                                                                                  & \\text{{if wall exist above window and }} h_{{eq}}\\le 1.25\\cdot w_t \\ \\left[{is_wall_above_opening and h_eq <= 1.25 * w_t}\\right]\\\\'
        f'\\left({{L_L}}^2 + \\left(L_H-\\frac{{h_{{eq}}}}{{3}}\\right)^2\\right)^{{0.5}} +\\frac{{h_{{eq}}}}{{2}},     & \\text{{if no wall exist above window or }} h_{{eq}}>1.25\\cdot w_t \\ \\left[{not is_wall_above_opening or h_eq > 1.25 * w_t}\\right]'
        f'\\end{{dcases}}'
    ]

    if is_wall_above_opening is True and h_eq <= 1.25 * w_t:
        # equation B.12
        L_f = L_L + h_eq / 2
        _latex.extend([
            f'L_f={L_L:.2f}+\\frac{{{h_eq:.2f}}}{{2}}',
            f'L_f={L_f:.2f}\\ \\left[m\\right]',
        ])
    elif is_wall_above_opening is False or h_eq > 1.25 * w_t:
        # equation B.13
        a = (L_L ** 2 + (L_H - h_eq / 3) ** 2) ** 0.5
        b = h_eq / 2
        L_f = a + b
        _latex.extend([
            f'L_f=\\left({{{L_L:.2f}}}^2 + \\left({L_H:.2f}-\\frac{{{h_eq:.2f}}}{{3}}\\right)^2\\right)^{{0.5}} +\\frac{{{h_eq:.2f}}}{{2}}',
            f'L_f={L_f:.2f}\\ \\left[m\\right]',
        ])
    else:
        raise ValueError('No conditions are met when calculating `L_f`')

    return dict(L_f=L_f, _latex=_latex)


def clause_b_4_1_8_T_w(
        L_f: float,
        w_t: float,
        Q: float,
        T_0: float = 293.15,
        *_,
        **__,
):
    """
    Equation B.14. Flame temperature at the window opening.

    :param L_f:
    :param w_t:
    :param Q:
    :param T_0:
    :param _:
    :param __:
    :return:
    """
    try:
        assert L_f * w_t / Q < 1
    except AssertionError:
        raise AssertionError(f'Condition not satisfied L_f*w_t/Q<1 in Clause B.4.1(8) ({L_f:.2f}*{w_t:.2f}/{Q:.2f}={L_f * w_t / Q:.2f}!<{1})')

    T_w = 520 / (1 - 0.4725 * (L_f * w_t / Q)) + T_0

    _latex = [
        'T_w=\\frac{520}{1-0.4725\\frac{L_f w_t}{Q}}+T_0',
        f'T_w=\\frac{{520}}{{1-0.4725\\frac{{{L_f:.2f}\\cdot {w_t:.2f}}}{{{Q:.2f}}}}}+{T_0:.2f}',
        f'T_w={T_w:.2f}\\ \\left[K\\right]',
        f'T_w={T_w - 273.15:.2f}\\ \\left[^\\circ C\\right]'
    ]
    return dict(T_w=T_w, _latex=_latex)


def clause_b_4_1_10_T_z(
        T_w: float,
        L_x: float,
        w_t: float,
        Q: float,
        T_0: float = 293.15,
        *_,
        **__,
):
    """Equation B.15 in BS EN 1991-1-2:2002, page 38.
    Flame temperature along the axis."""
    if 'is_test' in __:
        if not __['is_test']:
            assert L_x * w_t / Q < 1

    T_z = (T_w - T_0) * (1 - 0.4725 * (L_x * w_t / Q)) + T_0

    _latex = [
        'T_z=\\left(T_w-T_0\\right) \\left(1-0.4725\\frac{L_x w_t}{Q}\\right)+T_0',
        f'T_z=\\left({T_w:.2f}-{T_0:.2f}\\right) \\left(1-0.4725\\frac{{{L_x:.2f}\\cdot {w_t:.2f}}}{{{Q:.2f}}}\\right)+{T_0:.2f}',
        f'T_z={T_z:.2f}\\ \\left[K\\right]',
        f'T_z={T_z - 273.15:.2f}\\ \\left[^\\circ C\\right]',
    ]
    return dict(T_z=T_z, _latex=_latex)


def clause_b_4_1_11_epsilon_f(
        d_f,
        *_,
        **__,
):
    epsilon_f = 1 - e ** (-0.3 * d_f)

    _latex = [
        '\\varepsilon_f=1-e^{-0.3d_f}',
        f'\\varepsilon_f=1-e^{{-0.3\\cdot {d_f:.2f}}}',
        f'\\varepsilon_f={epsilon_f:.2f}\\ \\left[-\\right]',
    ]
    return dict(epsilon_f=epsilon_f, _latex=_latex)


def clause_b_4_1_12_alpha_c(
        d_eq,
        Q,
        A_v,
        *_, **__,
):
    alpha_c = 4.67 * (1 / d_eq) ** 0.4 * (Q / A_v) ** 0.6

    _latex = [
        '\\alpha_c=4.67{\\left(\\frac{1}{d_{eq}}\\right)}^{0.4} {\\left(\\frac{Q}{A_v}\\right)}^{0.6}',
        f'\\alpha_c=4.67{{\\left(\\frac{{1}}{{{d_eq:.2f}}}\\right)}}^{{0.4}} {{\\left(\\frac{{{Q:.2f}}}{{{A_v:.2f}}}\\right)}}^{{0.6}}',
        f'\\alpha_c={alpha_c:.2f}\\ \\left[\\frac{{W}}{{m^2\\cdot K}}\\right]',
    ]
    return dict(alpha_c=alpha_c, _latex=_latex)


def clause_b_4_1_13_modification_to_flame_with_balcony_above_opening(
        L_L,
        L_H,
        W_a,
        is_wall_above_opening: bool = True,
        is_balcony_above_opening: bool = True,
        *_,
        **__,
) -> Tuple[float, float]:
    assert is_balcony_above_opening is True and is_wall_above_opening is True
    L_L = L_L - W_a * (1 + 2 ** 0.5)
    L_H = L_H + W_a
    return L_L, L_H


def clause_b_4_1_14_modification_to_flame_with_no_wall_above_opening(
        L_L,
        L_H,
        W_a,
        is_wall_above_opening: bool = False,
        is_balcony_above_opening: bool = True,
        *_,
        **__,
):
    assert is_balcony_above_opening is True and is_wall_above_opening is False
    L_L = L_L - W_a
    L_H = L_H + W_a
    return L_L, L_H


def clause_b_4_2_1_Q(
        A_f,
        q_fd,
        tau_F,
        *_,
        **__,
):
    """equation B.18, page 37"""
    Q = (A_f * q_fd) / tau_F
    _latex = [
        'Q=\\frac{A_f\\cdot q_{fd}}{\\tau_F}',
        f'Q=\\frac{{{A_f:.2f}\\cdot {q_fd:.2f}}}{{{tau_F:.2f}}}',
        f'Q={Q:.2f}\\ [MW]'
    ]
    return dict(Q=Q, _latex=_latex)


def clause_b_4_2_2_T_f(
        Omega,
        T_0,
        *_,
        **__,
):
    """equation B.19, page 37"""
    T_f = 1200 * (1 - e ** (-0.00228 * Omega)) + T_0
    _latex = [
        'T_f=1200\\left(1-e^{-0.00228\\Omega}\\right)+T_0',
        f'T_f=1200\\left(1-e^{{-0.00228\\cdot{Omega:.2f}}}\\right)+{T_0}',
        f'T_f={T_f:.2f}\\ \\left[K\\right]',
        f'T_f={T_f - 273.15:.2f}\\ \\left[^\\circ C\\right]',
    ]
    return dict(T_f=T_f, _latex=_latex)


def clause_b_4_2_3_d_f(
        h_eq,
        *_,
        **__,
):
    # Figure B.4, page 36
    d_f = h_eq
    _latex = [
        'd_f = h_{eq}',
        f'd_f = {h_eq}\\ \\left[m\\right]',
    ]
    return dict(d_f=d_f, _latex=_latex)


def clause_b_4_2_3_L_L(
        h_eq,
        Q,
        A_v,
        u,
        *_,
        **__,
):
    # equation B.20, page 37
    a = 1.366 * (1 / u) ** 0.43
    b = Q / (A_v ** 0.5)
    L_L = (a * b) - h_eq
    _latex = [
        'L_L=\\left(1.366\\left(\\frac{1}{u}\\right)^{0.43}\\frac{Q}{\\sqrt{A_v}}\\right)-h_{eq}',
        f'L_L=\\left(1.366\\left(\\frac{{1}}{{{u:.2f}}}\\right)^{{0.43}}\\frac{{{Q:.2f}}}{{\\sqrt{{{A_v:.2f}}}}}\\right)-{h_eq:.2f}',
        f'L_L={L_L:.2f}\\ \\left[m\\right]',
    ]
    return dict(L_L=L_L, _latex=_latex)


def clause_b_4_2_4_L_H(
        h_eq,
        L_L,
        u,
        *_,
        **__,
):
    # equation B.21, page 38
    a = 0.605
    b = (u ** 2 / h_eq) ** 0.22
    c = (L_L + h_eq)
    L_H = a * b * c
    _latex = [
        'L_H=0.605\\left(\\frac{u^2}{h_{eq}}\\right)^{0.22}\\left(L_L+h_{eq}\\right)',
        f'L_H=0.605\\left(\\frac{{{u:.2f}^2}}{{{h_eq:.2f}}}\\right)^{{0.22}}\\left({L_L:.2f}+{h_eq:.2f}\\right)',
        f'L_H={L_H:.2f}\\ \\left[m\\right]',
    ]
    return dict(L_H=L_H, _latex=_latex)


def clause_b_4_2_5_w_f(
        w_t,
        L_H,
        *_,
        **__,
):
    # equation B.22, page 38
    w_f = w_t + 0.4 * L_H
    _latex = [
        'w_f=w_t+0.4\\cdot L_H',
        f'w_f={w_t:.2f}+0.4\\cdot {L_H:.2f}',
        f'w_f={w_f:.2f}  \\left[m\\right]',
    ]
    return dict(w_f=w_f, _latex=_latex)


def clause_b_4_2_6_L_f(
        L_L,
        L_H,
        *_,
        **__,
):
    # equation B.23, page 38
    L_f = (L_L ** 2 + L_H ** 2) ** 0.5
    _latex = [
        'L_f=\\left(L_L^2+L_H^2\\right)^{0.5}',
        f'L_f=\\left({L_L:.2f}^2+{L_H:.2f}^2\\right)^{{0.5}}',
        f'L_f={L_f:.2f}\\ \\left[m\\right]',
    ]
    return dict(L_f=L_f, _latex=_latex)


def clause_b_4_2_7_T_w(
        A_v,
        Q,
        L_f,
        T_0,
        *_,
        **__,
):
    # equation B.24, page 38
    try:
        assert L_f * (A_v ** 0.5) / Q < 1
    except AssertionError:
        raise ValueError(f'Condition L_f * (A_v ** 0.5) / Q = {L_f * (A_v ** 0.5) / Q:.2f} < 1 not satisfied')

    T_w = 520 / (1 - 0.3325 * L_f * (A_v ** 0.5) / Q) + T_0

    _latex = [
        'T_w=520\\cdot\\left(1-\\frac{0.3325\\cdot L_f\\cdot A_v^{0.5}}{Q}\\right)^{-1}+T_0',
        f'T_w=520\\cdot\\left(1-\\frac{{0.3325\\cdot {L_f:.2f}\\cdot {A_v:.2f}^{{0.5}}}}{{{Q:.2f}}}\\right)^{{-1}}+{T_0:.2f}',
        f'T_w={T_w:.2f}\\ \\left[K\\right]',
        f'T_w={T_w - 273.15:.2f}\\ \\left[^\\circ C\\right]',
    ]
    return dict(T_w=T_w, _latex=_latex)


def clause_b_4_2_9_T_z(
        L_x,
        Q,
        A_v,
        T_w,
        T_0,
        *_,
        **__,
):
    # equation B.25, page 38
    a = (1 - 0.3325 * L_x * (A_v ** 0.5) / Q)
    b = T_w - T_0
    T_z = a * b + T_0

    _latex = [
        'T_z=\\left(1-\\frac{0.3325\\cdot L_x\\cdot A_v^{0.5}}{Q}\\right)\\left(T_w-T_0\\right)+T_0',
        f'T_z=\\left(1-\\frac{{0.3325\\cdot {L_x:.2f}\\cdot {A_v:.2f}^{{0.5}}}}{{{Q:.2f}}}\\right)\\left({T_w:.2f}-{T_0:.2f}\\right)+{T_0:.2f}',
        f'T_z={T_z:.2f}\\ \\left[K\\right]',
        f'T_z={T_z - 273.15:.2f}\\ \\left[^\\circ C\\right]',
    ]
    return dict(T_z=T_z, _latex=_latex)


def clause_b_4_2_10_epsilon(
        d_f,
        *_,
        **__,
):
    # equation B.26, page 39
    e_f = 1 - e ** (-0.3 * d_f)

    _latex = [
        '\\varepsilon_f=1-e^{-0.3\\cdot d_f}',
        f'\\varepsilon_f=1-e^{{-0.3\\cdot {d_f:.2f}}}',
        f'\\varepsilon_f={e_f:.2f}\\ \\left[-\\right]',
    ]
    return dict(e_f=e_f, _latex=_latex)


def clause_b_4_2_11_alpha_c(
        d_eq,
        A_v,
        Q,
        u,
        *_, **__,
):
    # equation B.27, page 39

    a = 9.8 * (1 / d_eq) ** 0.4
    b = (Q / (17.5 * A_v) + u / 1.6) ** 0.6
    alpha_c = a * b

    _latex = [
        '\\alpha_c=9.8\\cdot\\left(\\frac{1}{d_{eq}} \\right )^{0.4}\\cdot\\left(\\frac{Q}{17.5\\cdot A_v}+\\frac{u}{1.6} \\right ) ^ {0.6}',
        f'\\alpha_c=9.8\\cdot\\left(\\frac{{1}}{{{d_eq:.2f}}} \\right )^{{0.4}}\\cdot\\left(\\frac{{{Q:.2f}}}{{17.5\\cdot {A_v:.2f}}}+\\frac{{{u:.2f}}}{{1.6}} \\right ) ^ {{0.6}}',
        f'\\alpha_c={alpha_c:.2f}\\ \\left[\\frac{{W}}{{m^2/K}}\\right]',
    ]

    return dict(alpha_c=alpha_c, _latex=_latex)


def clause_b_5_1_phi_f(
        C_1, C_2, C_3, C_4,
        phi_f_1, phi_f_2, phi_f_3, phi_f_4,
        d_1, d_2,
        *_, **__
):
    a = (C_1 * phi_f_1 + C_2 * phi_f_2) * d_1
    b = (C_3 * phi_f_3 + C_4 * phi_f_4) * d_2
    c = (C_1 + C_2) * d_1
    d = (C_3 + C_4) * d_2
    phi_f = (a + b) / (c + d)

    _latex = [
        f'\\phi_f=\\frac{{\\left(C_1 \\phi_{{f,1}}+C_2 \\phi_{{f,2}}\\right) d_1+\\left(C_3 \\phi_{{f,3}}+C_4 \\phi_{{f,4}}\\right) d_2}}{{\\left(C_1+C_2\\right) d_1+\\left(C_3+C_4\\right) d_2}}',
        f'\\phi_f=\\frac{{\\left({C_1:.2f}\\cdot {phi_f_1:.2f}+{C_2:.2f}\\cdot {phi_f_2}\\right) {d_1:.2f}+\\left({C_3:.2f} \\cdot {phi_f_3:.2f}+{C_4:.2f}\\cdot {phi_f_4:.2f}\\right) {d_2:.2f}}}{{\\left({C_1:.2f}+{C_2:.2f}\\right) {d_1:.2f}+\\left({C_3:.2f}+{C_4:.2f}\\right) {d_2:.2f}}}',
        f'\\phi_f={phi_f:.2f}\\ \\left[-\\right]',
    ]

    return dict(phi_f=phi_f, _latex=_latex)


def _test_external_fire_no_forced_draught_1(raise_error=True):
    """
    Test against analysis carried in report '190702-R00-SC19024-WP1-Flame Projection Calculations-DN-CIC'.
    Wall above opening and no balcony above opening.
    """

    # compulsory user defined parameters
    w_t = 1.82
    h_eq = 1.1
    d_ow = 1e10
    D = 6.681317  # calculated based on floor area 14.88 and D/W = 3
    W = 2.227106  # calculated based on floor area 14.88 and D/W = 3
    W_1 = 1.82
    W_2 = 5.46
    q_fd = 870
    tau_F = 1200
    rho_g = 0.45
    g = 9.81
    T_0 = 293.15

    is_wall_above_opening = True
    is_windows_on_more_than_one_wall = False
    is_central_core = False

    # derived values below
    A_v = w_t * h_eq
    A_f = D * W
    O = 0.03

    kwargs = locals()

    # Calculate D/W
    try:
        kwargs.update(clause_b_2_2_DW_ratio(**kwargs))
    except AssertionError:
        try:
            kwargs.update(clause_b_2_3_DW_ratio(**kwargs))
        except AssertionError:
            kwargs.update(clause_b_2_4_DW_ratio(**kwargs))

    # Calculate heat release rate
    kwargs.update(clause_b_4_1_1_Q(**kwargs))

    # Calculate external flame vertical projection
    kwargs.update(clause_b_4_1_3_L_L(**kwargs))

    # Calculate external flame horizontal projection
    kwargs.update(clause_b_4_1_6_L_H(**kwargs))

    # Modify L_H and L_L
    # todo

    # Calculate flame length
    kwargs.update(clause_b_4_1_7_L_f(**kwargs))

    print(f'{kwargs["L_f"]:.1f} == 1.9')
    assert abs(round(kwargs["L_f"], 1) - 1.9) < 1e-7


if __name__ == '__main__':
    _test_external_fire_no_forced_draught_1()
