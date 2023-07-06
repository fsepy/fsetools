from math import e
from typing import Union

from fsetools.etc.solver import linear_solver
from fsetools.lib.fse_thermal_radiation import phi_parallel_any_br187, phi_perpendicular_any_br187

SYMBOLS = dict(
    a_z=('-', 'the absorptivity of flames'),
    alpha=('kW/(m**2*K)', 'the convective heat transfer coefficient'),
    C_1=('-', 'the protection coefficient of member face 1'),
    C_2=('-', 'the protection coefficient of member face 2'),
    C_3=('-', 'the protection coefficient of member face 3'),
    C_4=('-', 'the protection coefficient of member face 4'),
    C_i=('-', 'the protection coefficient of member face'),
    d_1=('m', 'the cross-sectional dimension 1'),
    d_2=('m', 'the cross-sectional dimension 2'),
    d_aw=('m', 'the distance between steel member bottom and opening top edge'),
    d_i=('-', 'the cross-sectional dimension of member face $i$'),
    epsilon_f=('-', 'the emissivity of an opening'),
    epsilon_z_1=('-', 'the total emissivity of the flames on a steel member at face 1'),
    epsilon_z_2=('-', 'the total emissivity of the flames on a steel member at face 2'),
    epsilon_z_3=('-', 'the total emissivity of the flames on a steel member at face 3'),
    epsilon_z_4=('-', 'the total emissivity of the flames on a steel member at face 4'),
    epsilon_Z_i=('-', 'the emissivity of the flames with respect to face $i$ of the column'),
    h_eq=('m', 'the weighted average of window heights on all wall ${\\textstyle \\sum_{i}}\\left(A_{v,i}h_i\\right)/A_v$'),
    h_z=('m', 'the height of the top of the flame above the bottom of the beam'),
    I_f=('kW/m**2', 'the radiative heat flux from an opening'),
    I_f_1=('kW/m**2', 'the radiative heat flux from an opening to a steel member at face 1'),
    I_f_2=('kW/m**2', 'the radiative heat flux from an opening to a steel member at face 2'),
    I_f_3=('kW/m**2', 'the radiative heat flux from an opening to a steel member at face 3'),
    I_f_4=('kW/m**2', 'the radiative heat flux from an opening to a steel member at face 4'),
    I_z=('kW/m**2', 'the radiative heat flux from a flame'),
    I_z_1=('kW/m**2', 'the radiative heat flux from a flame to a steel member at face 1'),
    I_z_2=('kW/m**2', 'the radiative heat flux from a flame to a steel member at face 2'),
    I_z_3=('kW/m**2', 'the radiative heat flux from a flame to a steel member at face 3'),
    I_z_4=('kW/m**2', 'the radiative heat flux from a flame to a steel member at face 4'),
    I_Z_i=('kW/m**2', 'the radiative heat flux from the flame to column face $i$'),
    is_forced_draught=('boolean', 'True if forced draught, False otherwise'),
    l=('m', 'a distance from an opening, measured along the flame axis'),
    L_H=("m", "the horizontal projection of the flame (from the facade)"),
    L_L=("m", "the flame height (from the upper part of the window)"),
    lambda_1=('m', 'the flame thickness relevant to member face 1'),
    lambda_2=('m', 'the flame thickness relevant to member face 2'),
    lambda_3=('m', 'the flame thickness relevant to member face 3'),
    lambda_4=('m', 'the flame thickness relevant to member face 4'),
    phi_f_1=('-', 'the configuration factor of member face 1 for an opening'),
    phi_f_2=('-', 'the configuration factor of member face 2 for an opening'),
    phi_f_3=('-', 'the configuration factor of member face 3 for an opening'),
    phi_f_4=('-', 'the configuration factor of member face 4 for an opening'),
    sigma=('kW/(m**2*K**4)', 'Stefan Boltzmann constant'),
    T_f=('K', 'the temperature of the fire compartment'),
    T_m=('K', 'the average temperature of the steel member'),
    T_m_1=('K', 'the temperature of the steel member at face 1'),
    T_m_2=('K', 'the temperature of the steel member at face 2'),
    T_m_3=('K', 'the temperature of the steel member at face 3'),
    T_m_4=('K', 'the temperature of the steel member at face 4'),
    T_o=('K', 'the flame temperature at the opening from annex B of EN 1991-1-2'),
    T_z=('K', 'the flame temperature'),
    T_z_1=('K', 'the flame temperature from Annex B of EN 1991-1-2, level with the bottom of a beam'),
    T_z_2=('K', 'the flame temperature from Annex B of EN 1991-1-2, level with the top of a beam'),
    w_f=('m', 'the flame width'),
    w_t=('m', 'the width of the opening'),
)

UNITS = {k: v[0] for k, v in SYMBOLS.items()}
DESCRIPTIONS = {k: v[1] for k, v in SYMBOLS.items()}


def clause_b_1_3_3_T_m(
        I_z,
        I_f,
        alpha,
        T_z,
        sigma: float = 5.67e-11,
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
            sigma_: float = 56.7e-11
    ):
        return I_z_ + I_f_ + alpha_ * T_z_ - sigma_ * T_m_ ** 4 - alpha_ * T_m_

    # T_m = bisect(func, 0.001, 5000, (I_z, I_f, alpha, T_z, sigma))

    T_m = linear_solver(
        func=func,
        func_kwargs=dict(T_m_=293.15, I_z_=I_z, I_f_=I_f, alpha_=alpha, T_z_=T_z, ),
        x_name='T_m_',
        y_target=0,
        x_upper=2000 + 273.15,
        x_lower=273.15,
        y_tol=0.1,
        iter_max=1000,
        func_multiplier=-1
    )

    _latex = (
        f'\\sigma\\cdot T_{{m}}^4 + \\alpha\\cdot T_{{m}} = I_{{z}} + I_{{f}} + \\alpha\\cdot T_{{z}}',
        f'\\left({sigma:.2E}\\right)\\cdot T_m^4 + {alpha:.2f}\\cdot T_m = {I_z:.2f} + {I_f:.2f} + {alpha:.2f}\\cdot {T_z:.2f}',
        f'T_m={T_m:.2f}\\ \\left[K\\right]',
        f'T_m={T_m - 273.15:.2f}\\ \\left[^\\circ C\\right]',
    )

    return dict(T_m=T_m, _latex=_latex)


def clause_b_1_3_3_T_m_i_beam(
        I_z_1, I_z_2, I_z_3, I_z_4,
        I_f_1, I_f_2, I_f_3, I_f_4,
        alpha,
        T_z_1, T_z_2,
        sigma: float = 5.67e-11,
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
            sigma_: float = 56.7e-11
    ):
        return I_z_ + I_f_ + alpha_ * T_z_ - sigma_ * T_m_ ** 4 - alpha_ * T_m_

    T_m_1 = bisect(func, 0.001, 5000, (I_z_1, I_f_1, alpha, T_z_1, sigma))
    T_m_2 = bisect(func, 0.001, 5000, (I_z_2, I_f_2, alpha, T_z_2, sigma))
    T_m_3 = bisect(func, 0.001, 5000, (I_z_3, I_f_3, alpha, (T_z_1 + T_z_2) / 2, sigma))
    T_m_4 = bisect(func, 0.001, 5000, (I_z_4, I_f_4, alpha, (T_z_1 + T_z_2) / 2, sigma))

    _latex = (
        f'\\sigma\\cdot T_{{m,i}}^4 + \\alpha\\cdot T_{{m,i}} = I_{{z,i}} + I_{{f,i}} + \\alpha\\cdot T_{{z,i}}',
        f'\\left( {sigma:.2E}\\right) T_{{m,1}}^4+{alpha:.2f}T_{{m,1}}={I_z_1:.2f}+{I_f_1:.2f}+{alpha:.2f}\\cdot {T_z_1:.2f}\\Rightarrow T_{{m,1}}={T_m_1:.2f}\\ \\left[K\\right]={T_m_1 - 273.15:.2f} \\left[^\\circ C\\right]',
        f'\\left( {sigma:.2E}\\right) T_{{m,2}}^4+{alpha:.2f}T_{{m,2}}={I_z_2:.2f}+{I_f_2:.2f}+{alpha:.2f}\\cdot {T_z_2:.2f}\\Rightarrow T_{{m,2}}={T_m_2:.2f}\\ \\left[K\\right]={T_m_2 - 273.15:.2f} \\left[^\\circ C\\right]',
        f'\\left( {sigma:.2E}\\right) T_{{m,3}}^4+{alpha:.2f}T_{{m,3}}={I_z_3:.2f}+{I_f_3:.2f}+{alpha:.2f}\\cdot {(T_z_1 + T_z_2) / 2:.2f}\\Rightarrow T_{{m,3}}={T_m_3:.2f}\\ \\left[K\\right]={T_m_3 - 273.15:.2f} \\left[^\\circ C\\right]',
        f'\\left( {sigma:.2E}\\right) T_{{m,4}}^4+{alpha:.2f}T_{{m,4}}={I_z_4:.2f}+{I_f_4:.2f}+{alpha:.2f}\\cdot {(T_z_1 + T_z_2) / 2:.2f}\\Rightarrow T_{{m,4}}={T_m_4:.2f}\\ \\left[K\\right]={T_m_4 - 273.15:.2f} \\left[^\\circ C\\right]',
    )

    return dict(T_m_1=T_m_1, T_m_2=T_m_2, T_m_3=T_m_3, T_m_4=T_m_4, _latex=_latex)


def clause_b_1_3_3_T_m_i_column(
        I_z_1, I_z_2, I_z_3, I_z_4,
        I_f_1, I_f_2, I_f_3, I_f_4,
        alpha,
        T_z,
        sigma: float = 5.67e-11,
        *_, **__
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
            sigma_: float = 56.7e-11
    ):
        return I_z_ + I_f_ + alpha_ * T_z_ - sigma_ * T_m_ ** 4 - alpha_ * T_m_

    T_m_1 = bisect(func, 0.001, 5000, (I_z_1, I_f_1, alpha, T_z, sigma))
    T_m_2 = bisect(func, 0.001, 5000, (I_z_2, I_f_2, alpha, T_z, sigma))
    T_m_3 = bisect(func, 0.001, 5000, (I_z_3, I_f_3, alpha, T_z, sigma))
    T_m_4 = bisect(func, 0.001, 5000, (I_z_4, I_f_4, alpha, T_z, sigma))

    _latex = (
        f'\\sigma\\cdot T_{{m,i}}^4 + \\alpha\\cdot T_{{m,i}} = I_{{z,i}} + I_{{f,i}} + \\alpha\\cdot T_{{z}}',
        f'\\left( {sigma:.2E}\\right) T_{{m,1}}^4+{alpha:.2f}T_{{m,1}}={I_z_1:.2f}+{I_f_1:.2f}+{alpha:.2f}\\cdot {T_z:.2f}\\Rightarrow T_{{m,1}}={T_m_1:.2f}\\ \\left[K\\right]={T_m_1 - 273.15:.2f} \\left[^\\circ C\\right]',
        f'\\left( {sigma:.2E}\\right) T_{{m,2}}^4+{alpha:.2f}T_{{m,2}}={I_z_2:.2f}+{I_f_2:.2f}+{alpha:.2f}\\cdot {T_z:.2f}\\Rightarrow T_{{m,2}}={T_m_2:.2f}\\ \\left[K\\right]={T_m_2 - 273.15:.2f} \\left[^\\circ C\\right]',
        f'\\left( {sigma:.2E}\\right) T_{{m,3}}^4+{alpha:.2f}T_{{m,3}}={I_z_3:.2f}+{I_f_3:.2f}+{alpha:.2f}\\cdot {T_z:.2f}\\Rightarrow T_{{m,3}}={T_m_3:.2f}\\ \\left[K\\right]={T_m_3 - 273.15:.2f} \\left[^\\circ C\\right]',
        f'\\left( {sigma:.2E}\\right) T_{{m,4}}^4+{alpha:.2f}T_{{m,4}}={I_z_4:.2f}+{I_f_4:.2f}+{alpha:.2f}\\cdot {T_z:.2f}\\Rightarrow T_{{m,4}}={T_m_4:.2f}\\ \\left[K\\right]={T_m_4 - 273.15:.2f} \\left[^\\circ C\\right]',
    )

    return dict(T_m_1=T_m_1, T_m_2=T_m_2, T_m_3=T_m_3, T_m_4=T_m_4, _latex=_latex)


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
        *_, **__
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


def clause_b_1_3_5_I_f_i(
        phi_f_1, phi_f_2, phi_f_3, phi_f_4,
        epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4,
        sigma, T_f,
        epsilon_f=1,
        *_, **__
):
    I_f_1 = phi_f_1 * epsilon_f * (1 - epsilon_z_1) * sigma * T_f ** 4
    I_f_2 = phi_f_2 * epsilon_f * (1 - epsilon_z_2) * sigma * T_f ** 4
    I_f_3 = phi_f_3 * epsilon_f * (1 - epsilon_z_3) * sigma * T_f ** 4
    I_f_4 = phi_f_4 * epsilon_f * (1 - epsilon_z_4) * sigma * T_f ** 4

    _latex = [
        f'I_{{f,1}}=\\phi_{{f,1}} \\varepsilon_f \\left(1-\\varepsilon_{{z,1}}\\right) \\sigma T_f^4={phi_f_1:.3f}\\cdot {epsilon_f:.3f}\\cdot \\left(1-{epsilon_z_1:.3f}\\right)\\cdot \\left({sigma:.2E}\\right)\\cdot {T_f:.2f}^4={I_f_1:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{f,2}}=\\phi_{{f,2}} \\varepsilon_f \\left(1-\\varepsilon_{{z,2}}\\right) \\sigma T_f^4={phi_f_2:.3f}\\cdot {epsilon_f:.3f}\\cdot \\left(1-{epsilon_z_2:.3f}\\right)\\cdot \\left({sigma:.2E}\\right)\\cdot {T_f:.2f}^4={I_f_2:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{f,3}}=\\phi_{{f,3}} \\varepsilon_f \\left(1-\\varepsilon_{{z,3}}\\right) \\sigma T_f^4={phi_f_3:.3f}\\cdot {epsilon_f:.3f}\\cdot \\left(1-{epsilon_z_3:.3f}\\right)\\cdot \\left({sigma:.2E}\\right)\\cdot {T_f:.2f}^4={I_f_3:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{f,4}}=\\phi_{{f,4}} \\varepsilon_f \\left(1-\\varepsilon_{{z,4}}\\right) \\sigma T_f^4={phi_f_4:.3f}\\cdot {epsilon_f:.3f}\\cdot \\left(1-{epsilon_z_4:.3f}\\right)\\cdot \\left({sigma:.2E}\\right)\\cdot {T_f:.2f}^4={I_f_4:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_f_1=I_f_1, I_f_2=I_f_2, I_f_3=I_f_3, I_f_4=I_f_4, _latex=_latex)


def clause_b_1_3_2_d(d_1, d_2, *_, **__):
    # page 47

    d = (d_1 + d_2) / 2
    _latex = [
        f'd=d_{{eq}}=\\frac{{\\left( d_1+d_2\\right)}}{{2}}',
        f'd=d_{{eq}}=\\frac{{\\left( {d_1:.2f}+{d_2:.2f}\\right)}}{{2}}',
        f'd=d_{{eq}}={d:.2f}\\ \\left[ m\\right]',
    ]

    return dict(d=d, _latex=_latex)


def clause_b_1_4_1_phi_f_i_beam(
        h_eq,
        w_t,
        d_aw,
        lambda_3,
        lambda_4,
        *_,
        **__
):
    phi_f_1 = phi_perpendicular_any_br187(
        W_m=w_t,
        H_m=h_eq,
        w_m=-0.5 * w_t,
        h_m=d_aw,
        S_m=lambda_3,
    )
    phi_f_2 = 0
    phi_f_3 = 0
    phi_f_4 = phi_parallel_any_br187(
        W_m=w_t,
        H_m=h_eq,
        w_m=0.5 * w_t,
        h_m=h_eq + d_aw,
        S_m=lambda_4,
    )

    _latex = [
        f'\\phi_{{f,1}}={phi_f_1:.5f}\\ \\left[-\\right]',
        f'\\phi_{{f,2}}={phi_f_2:.5f}\\ \\left[-\\right]',
        f'\\phi_{{f,3}}={phi_f_3:.5f}\\ \\left[-\\right]',
        f'\\phi_{{f,4}}={phi_f_4:.5f}\\ \\left[-\\right]',
    ]

    return dict(phi_f_1=phi_f_1, phi_f_2=phi_f_2, phi_f_3=phi_f_3, phi_f_4=phi_f_4, _latex=_latex)


def clause_b_1_4_1_phi_f_i_column(
        h_eq,
        d_2,
        lambda_1,
        lambda_2,
        lambda_3,
        *_, **__
):
    """

    :param h_eq:
    :param d_2:
    :param lambda_1:
    :param lambda_2:
    :param lambda_3:
    :param _:
    :param __:
    :return:
    """
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


def clause_b_2_1_2_I_z(
        phi_z: float,
        epsilon_z: float,
        sigma: float,
        T_z: float,
        *_, **__,
):
    """
    B.2.1 (2), page 51. Radiative heat flux if the column is between openings.

    :param phi_z:       [-] Overall configuration factor of the column for heat from the flame
    :param epsilon_z:   [-] Emissivity of the flame
    :param sigma:       [W/m2/K4] Stefan-Boltzmann constant
    :param T_z:         [K] Flame temperature
    :param _:           Not used
    :param __:          Not used
    :return:            A dict containing `I_z` and `_latex` where `I_z` is the heat flux in [kW/m2]
    """

    I_z = phi_z * epsilon_z * sigma * (T_z ** 4)

    _latex = [
        f'I_z=\\phi_z\\varepsilon_z\\sigma T_z^4',
        f'I_z={phi_z:.3f}\\cdot{epsilon_z:.3f}\\cdot{sigma:.3e}\\cdot{T_z ** 4:.3e}',
        f'I_z={I_z:.2f}\\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_z=I_z, _latex=_latex)


def _test_clause_b_2_1_2_I_z():
    o = clause_b_2_1_2_I_z(0.1, 0.7, 5.67e-11, 1000 + 273.5)
    assert '_latex' in o
    assert abs(o['I_z'] - 10.43943) <= 1e-4


def clause_b_2_1_3_I_z(
        phi_z_m: float,
        epsilon_z_m: float,
        phi_z_n: float,
        epsilon_z_n: float,
        sigma: float,
        T_z: float,
        *_, **__,
):
    """
    B.2.1 (3), page 51. Radiative heat flux if the column is opposite an opening.

    :param phi_z_m:         Overall configuration factor of the column for heat from flames on side `m`
    :param epsilon_z_m:     Total emissivity of the flames on side m
    :param phi_z_n:         Overall configuration factor of the column for heat from flames on side `n`
    :param epsilon_z_n:     Total emissivity of the flames on side n
    :param sigma:           [W/m2/K4] Stefan-Boltzmann constant
    :param T_z:             [K], Flame temperature
    :param _:               Not used
    :param __:              Not used
    :return:                A dict containing `I_z` and `_latex` where `I_z` is the heat flux in [kW/m2]
    """

    I_z = (phi_z_m * epsilon_z_m + phi_z_n * epsilon_z_n) * sigma * (T_z ** 4)

    _latex = [
        f'I_z=\\left(\\phi_{{z,m}} \\varepsilon_{{z,m}} + \\phi_{{z,n}} \\varepsilon_{{z,n}} \\right)\\sigma T_z^4',
        f'I_z=\\left({phi_z_m:.3f} \\cdot {epsilon_z_m:.3f} + {phi_z_n:.3f} \\cdot {epsilon_z_n:.3f} \\right){sigma:.3e}\\cdot {T_z ** 4:.3e}',
        f'I_z={I_z:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_z=I_z, _latex=_latex)


def _test_clause_b_2_1_3_I_z():
    o = clause_b_2_1_3_I_z(0.1, 0.2, 0.3, 0.4, 5.67e-11, 1000 + 273.15)
    assert '_latex' in o
    assert abs(o['I_z'] - 20.86) <= 1e-2


def clause_b_2_2_1_lambda(
        h: float,
        x: float = None,
        z: float = None,
        is_forced_draught: bool = False,
):
    """
    Clause B.2.2 (1), page 51, flame thickness if the column is opposite an opening and no awning or balcony above the
    opening.

    :param h:                   [m], flame horizontal projection
    :param x:                   [m], flame horizontal projection, required if `is_forced_draught` is True
    :param z:                   [m], vertical distance from flame tip to opening upper edge, required if
                                `is_forced_draught` is True
    :param is_forced_draught:   [-], whether forced draught condition presents
    :return:                    a dict containing `lambda_` and `_latex`
    """

    _latex = [
        f'\\lambda='
        f'\\begin{{dcases}}\n'
        f'\\frac{{2}}{{3}}h,                                           &\\text{{no forced draught }} \\left[ {not is_forced_draught}\\right]\\\\\n'
        f'\\operatorname{{min}}\left({{x, \\frac{{hx}}{{z}}}}\\right)  &\\text{{forced draught }}    \\left[ {is_forced_draught}\\right]\\\\\n'
        f'\\end{{dcases}}',
    ]

    if not is_forced_draught:
        lambda_ = 2. * h / 3.
        _latex.append(f'\\lambda=\\frac{{2}}{{3}}{h:.3f}')
    else:
        lambda_ = min(x, h * x / z)
        _latex.append(f'\\lambda=\\operatorname{{min}}\left({{{x:.3f}, \\frac{{{h * x:.3f}}}{{{z:.3f}}}}}\\right)')

    _latex.append(f'\\lambda={lambda_:.3f}\\ \\left[m\\right]')

    return dict(lambda_=lambda_, _latex=_latex)


def _test_clause_b_2_2_1_lambda():
    o = clause_b_2_2_1_lambda(2, 1, 1.5, False)
    assert '_latex' in o
    assert abs(2 / 3 * 2. - o['lambda_']) < 1.e-5

    o = clause_b_2_2_1_lambda(2, 1, 1.5, True)
    assert abs(1 - o['lambda_']) < 1.e-5

    o = clause_b_2_2_1_lambda(2, 1, 4, True)
    assert abs(2 / 4 - o['lambda_']) < 1.e-5


def clause_b_2_2_2_lambda(
        w_i_m: Union[float, list],
        s_m: Union[float, list],
        is_forced_draught_m: Union[float, list],
        w_i_n: Union[float, list],
        s_n: Union[float, list],
        is_forced_draught_n: Union[float, list],
        *_, **__,
):
    """
    Clause B.2.2 (1), page 55, flame thickness if the column is between openings and no awning or balcony above the
    opening.

    :param h:                   [m], flame horizontal projection
    :param x:                   [m], flame horizontal projection, required if `is_forced_draught` is True
    :param z:                   [m], vertical distance from flame tip to opening upper edge, required if
                                `is_forced_draught` is True
    :param is_forced_draught:   [-], whether forced draught condition presents
    :return:                    a dict containing `lambda_` and `_latex`
    """

    assert all([isinstance(i, (tuple, list)) for i in [w_i_m, s_m, is_forced_draught_m]])
    assert all([isinstance(i, (tuple, list)) for i in [w_i_n, s_n, is_forced_draught_n]])

    lambda_m = [
        clause_b_2_2_3_lambda_i(
            w_i=w_i_m[i], s=s_m[i], is_forced_draught=is_forced_draught_m[i]
        ) for i in range(len(w_i_m))
    ]
    lambda_n = [
        clause_b_2_2_3_lambda_i(
            w_i=w_i_n[i], s=s_n[i], is_forced_draught=is_forced_draught_n[i]
        ) for i in range(len(w_i_n))
    ]

    lambda_m = sum([i['lambda_i'] for i in lambda_m])
    lambda_n = sum([i['lambda_i'] for i in lambda_n])

    _latex = [
        f'lambda_m={lambda_m:.3f}\\ \\left[ m\\right]',
        f'lambda_n={lambda_n:.3f}\\ \\left[ m\\right]',
    ]

    return dict(lambda_m=lambda_m, lambda_n=lambda_n, _latex=_latex)


def clause_b_2_2_3_lambda_i(
        w_i: float,
        s: float = None,
        is_forced_draught: bool = False,
        *_, **__,
):
    """
    Clause B.2.2 (3), page 55, flame thickness used in B.2.2 (2).

    :param w_i:                 Width of the opening
    :param s:                   Horizontal distance from the centre-line of the column to the wall of the fire
                                compartment
    :param is_forced_draught:   True if forced condition is present
    :param _:
    :param __:
    :return:                    A dict containing `lambda_i` and `_latex`
    """
    _latex = [
        f'\\lambda_i='
        f'\\begin{{dcases}}\n'
        f'w_i,      &\\text{{no forced draught }} \\left[ {not is_forced_draught}\\right]\\\\\n'
        f'w_i+0.4s  &\\text{{forced draught }}    \\left[ {is_forced_draught}\\right]\\\\\n'
        f'\\end{{dcases}}',
    ]
    if not is_forced_draught:
        lambda_i = w_i
    else:
        lambda_i = w_i + 0.4 * s
        _latex.append(
            f'\\lambda_i=w_i+0.4\\cdot {s:.3f}'
        )
    _latex.append(
        f'\\lambda_i={lambda_i:.3f}\\left[ m\\right]'
    )

    return dict(lambda_i=lambda_i, _latex=_latex)


def clause_b_2_3_1_l(
        h: float = None,
        s: float = None,
        X: float = None,
        x: float = None,
        is_forced_draught: bool = False,
        is_column_opposite_to_openning: bool = True,
        *_, **__,
):
    """
    Clause B.2.3 (1), page 55, distance from the opening along the flame axis, used to calculate flame temperature T_z.

    :param h: [m], flame horizontal projection
    :param s: [m], horizontal distance from the centre-line of the column to the wall of the fire compartment
    :param X: todo
    :param x: todo
    :param is_forced_draught:
    :param is_column_opposite_to_openning:
    :param _:
    :param __:
    :return:
    """
    _latex = [
        f'\\lambda_i='
        f'\\begin{{dcases}}\n'
        f'\\frac{{h}}{{2}},         &\\text{{no forced draught }} \\left[ {not is_forced_draught}\\right]\\\\\n'
        f'0                         &\\text{{forced draught, opposite to opening }}    \\left[ {is_forced_draught and is_column_opposite_to_openning}\\right]\\\\\n'
        f'\\frac{{s\\cdot X}}{{x}}  &\\text{{forced draught, not opposite to opening }}    \\left[ {is_forced_draught and is_column_opposite_to_openning}\\right]\\\\\n'
        f'\\end{{dcases}}',
    ]

    if not is_forced_draught:
        l = h / 2.
        _latex += f'l=\\frac{{h}}{{2}}'
    elif is_forced_draught and is_column_opposite_to_openning:
        l = 0
    else:
        l = s * X / x
        _latex += f'l=s\\cdot X\\frac{{X}}{{x}}'

    _latex += f'l={l:.3f}\\ \\left[ m\\right]'


def clause_b_3_1_3_I_z(
        phi_z: float,
        epsilon_z: float,
        sigma: float,
        T_z: float,
        *_, **__,
):
    """
    B.3.1 (3), page 56. Radiative heat flux for beams parallel to the external wall of the fire compartment.

    :param phi_z:       [-] Overall configuration factor of the column for heat from the flame
    :param epsilon_z:   [-] Emissivity of the flame
    :param sigma:       [W/m2/K4] Stefan-Boltzmann constant
    :param T_z:         [K] Flame temperature
    :param _:           Not used
    :param __:          Not used
    :return:            A dict containing `I_z` and `_latex` where `I_z` is the heat flux in [kW/m2]
    """

    I_z = phi_z * epsilon_z * sigma * (T_z ** 4)

    _latex = [
        f'I_z=\\phi_z\\varepsilon_z\\sigma T_z^4',
        f'I_z={phi_z:.3f}\\cdot{epsilon_z:.3f}\\cdot{sigma:.3e}\\cdot{T_z ** 4:.3e}',
        f'I_z={I_z:.2f}\\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_z=I_z, _latex=_latex)


def clause_b_3_1_4_I_z(
        phi_z_m: float,
        epsilon_z_m: float,
        phi_z_n: float,
        epsilon_z_n: float,
        sigma: float,
        T_z: float,
        *_, **__,
):
    """
    B.3.1 (4), page 56. Radiative heat flux at a beam perpendicular to the external wall of the fire compartment.

    :param phi_z_m:         Overall configuration factor of the column for heat from flames on side `m`
    :param epsilon_z_m:     Total emissivity of the flames on side m
    :param phi_z_n:         Overall configuration factor of the column for heat from flames on side `n`
    :param epsilon_z_n:     Total emissivity of the flames on side n
    :param sigma:           [W/m2/K4] Stefan-Boltzmann constant
    :param T_z:             [K], Flame temperature
    :return:                A dict containing `I_z` and `_latex` where `I_z` is the heat flux in [kW/m2]
    """

    I_z = (phi_z_m * epsilon_z_m + phi_z_n * epsilon_z_n) * sigma * (T_z ** 4)

    _latex = [
        f'I_z=\\left( \\phi_{{z,m}}\\varepsilon_{{z,m}}+\\phi_{{z,n}}\\varepsilon_{{z,n}}\\right)\\sigma T_z^4',
        f'I_z=\\left({phi_z_m:.3f}\\cdot {epsilon_z_m:.3f}+{phi_z_n:.3f}\\cdot {epsilon_z_n:.3f} \\right)\\cdot {sigma:.3e}\\cdot {T_z:.3e}',
        f'I_z={I_z:.3f}\\ \\left[ \\frac{{kW}}/{{m^2}}\\right]'
    ]

    return dict(I_z=I_z, _latex=_latex)


def clause_b_3_2_1_lambda(
        h: float,
        x: float = None,
        z: float = None,
        is_forced_draught: bool = False,
):
    """
    Clause B.2.3 (1), page 58, flame thickness if the beam is parallel to the external wall of the fire compartment.

    :param h:                   [m], flame horizontal projection
    :param x:                   [m], flame horizontal projection, required if `is_forced_draught` is True
    :param z:                   [m], vertical distance from flame tip to opening upper edge, required if
                                `is_forced_draught` is True
    :param is_forced_draught:   [-], whether forced draught condition presents
    :return:                    a dict containing `lambda_` and `_latex`
    """

    _latex = [
        f'\\lambda='
        f'\\begin{{dcases}}\n'
        f'\\frac{{2}}{{3}}h,                                           &\\text{{no forced draught }} \\left[ {not is_forced_draught}\\right]\\\\\n'
        f'\\operatorname{{min}}\left({{x, \\frac{{hx}}{{z}}}}\\right)  &\\text{{forced draught }}    \\left[ {is_forced_draught}\\right]\\\\\n'
        f'\\end{{dcases}}',
    ]

    if not is_forced_draught:
        lambda_ = 2. * h / 3.
        _latex.append(f'\\lambda=\\frac{{2}}{{3}}{h:.3f}')
    else:
        lambda_ = min(x, h * x / z)
        _latex.append(f'\\lambda=\\operatorname{{min}}\left({{{x:.3f}, \\frac{{{h * x:.3f}}}{{{z:.3f}}}}}\\right)')

    _latex.append(f'\\lambda={lambda_:.3f}\\ \\left[m\\right]')

    return dict(lambda_=lambda_, _latex=_latex)


def clause_b_3_2_2_lambda(
        w_i_m: Union[float, list],
        s_m: Union[float, list],
        is_forced_draught_m: Union[float, list],
        w_i_n: Union[float, list],
        s_n: Union[float, list],
        is_forced_draught_n: Union[float, list],
        *_, **__,
):
    """
    Clause B.3.2 (1), page 58, flame thickness if the beam is perpendicular to the external wall of the fire
    compartment.

    :param h:                   [m], flame horizontal projection
    :param x:                   [m], flame horizontal projection, required if `is_forced_draught` is True
    :param z:                   [m], vertical distance from flame tip to opening upper edge, required if
                                `is_forced_draught` is True
    :param is_forced_draught:   [-], whether forced draught condition presents
    :return:                    a dict containing `lambda_` and `_latex`
    """

    assert all([isinstance(i, (tuple, list)) for i in [w_i_m, s_m, is_forced_draught_m]])
    assert all([isinstance(i, (tuple, list)) for i in [w_i_n, s_n, is_forced_draught_n]])

    lambda_m = [
        clause_b_3_2_3_lambda_i(
            w_i=w_i_m[i], s=s_m[i], is_forced_draught=is_forced_draught_m[i]
        ) for i in range(len(w_i_m))
    ]
    lambda_n = [
        clause_b_3_2_3_lambda_i(
            w_i=w_i_n[i], s=s_n[i], is_forced_draught=is_forced_draught_n[i]
        ) for i in range(len(w_i_n))
    ]

    lambda_m = sum([i['lambda_i'] for i in lambda_m])
    lambda_n = sum([i['lambda_i'] for i in lambda_n])

    _latex = [
        f'lambda_m={lambda_m:.3f}\\ \\left[ m\\right]',
        f'lambda_n={lambda_n:.3f}\\ \\left[ m\\right]',
    ]

    return dict(lambda_m=lambda_m, lambda_n=lambda_n, _latex=_latex)


def clause_b_3_2_3_lambda_i(
        w_i: float,
        s: float = None,
        is_forced_draught: bool = False,
        *_, **__,
):
    """
    Clause B.3.2 (3), page 58, flame thickness used in B.3.2 (2).

    :param w_i:                 Width of the opening
    :param s:                   Horizontal distance from the centre-line of the column to the wall of the fire
                                compartment
    :param is_forced_draught:   True if forced condition is present
    :param _:
    :param __:
    :return:                    A dict containing `lambda_i` and `_latex`
    """
    _latex = [
        f'\\lambda_i='
        f'\\begin{{dcases}}\n'
        f'w_i,      &\\text{{no forced draught }} \\left[ {not is_forced_draught}\\right]\\\\\n'
        f'w_i+0.4s  &\\text{{forced draught }}    \\left[ {is_forced_draught}\\right]\\\\\n'
        f'\\end{{dcases}}',
    ]
    if not is_forced_draught:
        lambda_i = w_i
    else:
        lambda_i = w_i + 0.4 * s
        _latex.append(
            f'\\lambda_i=w_i+0.4\\cdot {s:.3f}'
        )
    _latex.append(
        f'\\lambda_i={lambda_i:.3f}\\left[ m\\right]'
    )

    return dict(lambda_i=lambda_i, _latex=_latex)


def clause_b_3_3_1_l(
        h: float = None,
        s: float = None,
        X: float = None,
        x: float = None,
        is_forced_draught: bool = False,
        is_beam_perpendicular_to_wall: bool = True,
        *_, **__,
):
    """
    Clause B.3.3 (1), page 55, distance from the opening along the flame axis, used to calculate flame temperature T_z.

    :param h: [m], flame horizontal projection
    :param s: [m], horizontal distance from the centre-line of the column to the wall of the fire compartment
    :param X: todo
    :param x: todo
    :param is_forced_draught:
    :param is_beam_perpendicular_to_wall:
    :param _:
    :param __:
    :return:
    """
    _latex = [
        f'\\lambda_i='
        f'\\begin{{dcases}}\n'
        f'\\frac{{h}}{{2}},         &\\text{{no forced draught }} \\left[ {not is_forced_draught}\\right]\\\\\n'
        f'0                         &\\text{{forced draught, parallel to wall }}    \\left[ {is_forced_draught and is_beam_perpendicular_to_wall}\\right]\\\\\n'
        f'\\frac{{s\\cdot X}}{{x}}  &\\text{{forced draught, perpendicular to wall }}    \\left[ {is_forced_draught and is_beam_perpendicular_to_wall}\\right]\\\\\n'
        f'\\end{{dcases}}',
    ]

    if not is_forced_draught:
        l = h / 2.
        _latex += f'l=\\frac{{h}}{{2}}'
    elif is_forced_draught and is_beam_perpendicular_to_wall:
        l = 0
    else:
        l = s * X / x
        _latex += f'l=s\\cdot X\\frac{{X}}{{x}}'

    _latex += f'l={l:.3f}\\ \\left[ m\\right]'


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
        f'I_z=\\frac{{\\left({I_z_1:.2f}+{I_z_2:.2f}\\right) {d_1:.2f}+\\left({I_z_3:.2f}+{I_z_4:.2f}\\right) {d_2:.2f}}}{{\\left({C_1:.2f}+{C_2:.2f}\\right) {d_1:.2f}+\\left({C_3:.2f}+{C_4:.2f}\\right) {d_2:.2f}}}',
        f'I_z={I_z:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_z=I_z, _latex=_latex)


def clause_b_4_1_lambda_2(
        w_t,
        lambda_1,
        d_2,
        *_, **__
):
    lambda_2 = w_t - lambda_1 - d_2

    _latex = [
        f'\\lambda_2=w_t-\\lambda_1-d_2',
        f'\\lambda_2={w_t:.2f}-{lambda_1:.2f}-{d_2:.2f}',
        f'\\lambda_2={lambda_2:.2f}\\ \\left[ m \\right]',
    ]

    return dict(lambda_2=lambda_2, _latex=_latex)


def clause_b_4_1_lambda_4(
        lambda_3,
        L_L,
        L_H,
        h_eq,
        d_1,
        is_forced_draught: bool,
        *_, **__,
):
    _latex = [
        f'\\lambda_4=\n'
        f'\\begin{{dcases}}\n'
        f'\\operatorname{{max}}\\left(0, 2 L_H-\\lambda_3-d_1\\right),  &\\text{{if no forced draught }} \\left[ {not is_forced_draught}\\right]\\\\\n'
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
        lambda_4 = max(0, 2 * L_H - lambda_3 - d_1)
        _latex.extend([
            f'\\lambda_4=\\operatorname{{max}}\\left(0, 2 L_H-\\lambda_3-d_1\\right)',
            f'\\lambda_4=\\operatorname{{max}}\\left(0, 2\\cdot {L_H:.2f}-{lambda_3:.2f}-{d_1:.2f}\\right)',
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


def clause_b_4_2_epsilon_z_i(
        lambda_1,
        lambda_2,
        lambda_3,
        lambda_4,
        *_, **__
):
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


def clause_b_4_5_l(
        h_eq: float,
        L_H: float,
        L_L: float,
        d_1: float,
        lambda_3: float,
        is_forced_draught: bool,
        *_, **__
):
    """
    Clause B.4 (5), page 61

    :param h_eq:
    :param L_H:
    :param L_L:
    :param d_1:
    :param lambda_3:
    :param is_forced_draught:
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


def clause_b_4_6_a_z(
        epsilon_z_1,
        epsilon_z_2,
        epsilon_z_3,
        *_, **__
):
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


def clause_b_5_1_1_2_lambda_1(
        L_L,
        L_H,
        h_eq,
        d_aw,
        lambda_4,
        d_1,
        is_forced_draught,
        *_, **__,
):
    _latex = [
        f'\\lambda_1=\n'
        f'\\begin{{dcases}}\n'
        f'\\frac{{2}}{{3}} h_{{eq}} + d_{{aw}},                                     &\\text{{if no forced draught }} \\left[ {not is_forced_draught}\\right]\\\\\n'
        f'd_{{aw}}+h_{{eq}}-\\left(\\lambda_4+0.5 d_1\\right)\\frac{{L_L}}{{L_H}},  &\\text{{if forced draught }}\\left[{is_forced_draught}\\right]\\\\\n'
        f'\\end{{dcases}}'
    ]

    if is_forced_draught is False:
        # for non forced draught condition
        lambda_1 = 2 / 3 * h_eq + d_aw
        _latex.extend([
            f'\\lambda_1=\\frac{{2}}{{3}} h_{{eq}} + d_{{aw}}',
            f'\\lambda_1=\\frac{{2}}{{3}}\\cdot {h_eq:.2f}+{d_aw:.2f}',
        ])
    else:
        # for forced draught condition
        lambda_1 = d_aw + h_eq - (lambda_4 + 0.5 * d_1) * (L_L / L_H)
        _latex.extend([
            f'\\lambda_1=d_{{aw}}+h_{{eq}}-\\left(\\lambda_4+0.5 d_1\\right)\\frac{{L_L}}{{L_H}}',
            f'\\lambda_1={d_aw:.2f}+{h_eq:.2f}-\\left({lambda_4:.2f}+0.5\\cdot {d_1:.2f}\\right)\\frac{{{L_L:.2f}}}{{{L_H:.2f}}}',
        ])

    _latex.extend([
        f'\\lambda_1={lambda_1:.2f}\\ \\left[m\\right]',
    ])

    return dict(lambda_1=lambda_1, _latex=_latex)


def clause_b_5_1_1_2_lambda_2(
        L_L,
        d_aw, d_2, h_eq,
        lambda_1,
        is_forced_draught,
        *_, **__,
):
    _latex = [
        f'\\lambda_2=\n'
        f'\\begin{{dcases}}\n'
        f'\\operatorname{{max}}\\left(0, L_L-d_{{aw}}-d_2\\right),        &\\text{{if no forced draught }} \\left[ {not is_forced_draught}\\right]\\\\\n'
        f'\\operatorname{{max}}\\left(0, h_{{eq}}-\\lambda_1-d_2\\right),   &\\text{{if forced draught }}\\left[{is_forced_draught}\\right]\\\\\n'
        f'\\end{{dcases}}'
    ]

    if not is_forced_draught:
        lambda_2 = max(0, L_L - d_aw - d_2)
        _latex.extend([
            f'\\lambda_2=\\operatorname{{max}}\\left(0, L_L-d_{{aw}} - d_2\\right)',
            f'\\lambda_2=\\operatorname{{max}}\\left(0, {L_L:.2f}-{d_aw:.2f}-{d_2:.2f}\\right)',
        ])
    else:
        lambda_2 = max(0, h_eq - lambda_1 - d_2)
        _latex.extend([
            f'\\lambda_2=\\operatorname{{max}}\\left(0,h_{{eq}}-\\lambda_1-d_2\\right)',
            f'\\lambda_2=\\operatorname{{max}}\\left(0,{h_eq:.2f}-{lambda_1:.2f}-{d_2:.2f}\\right)',
        ])

    _latex.extend([
        f'\\lambda_2={lambda_2:.2f}\\ \\left[m\\right]',
    ])

    return dict(lambda_2=lambda_2, _latex=_latex)


def clause_b_5_1_1_2_lambda_3(
        L_H, L_L,
        lambda_4, d_aw, h_eq, d_1, d_2,
        is_forced_draught,
        *_, **__
):
    _latex = [
        f'\\lambda_3=\n'
        f'\\begin{{dcases}}\n'
        f'2 L_H-\\lambda_4-d_1,                                                                             &\\text{{if no forced draught }} \\left[ {not is_forced_draught}\\right]\\\\\n'
        f'\\frac{{L_H}}{{L_L}}\\left(d_{{aw}}+h_{{eq}} + 0.5 d_2\\right)-\\left(d_1+\\lambda_4\\right),     &\\text{{if forced draught }}\\left[{is_forced_draught}\\right]\\\\\n'
        f'\\end{{dcases}}'
    ]
    if not is_forced_draught:
        lambda_3 = 2 * L_H - lambda_4 - d_1
        _latex.extend([
            f'\\lambda_3=2L_H-\\lambda_4-d_1',
            f'\\lambda_3=2\\cdot {L_H:.2f}-{lambda_4:.2f}-{d_1:.2f}',
        ])
    else:
        lambda_3 = (L_H / L_L) * (d_aw + h_eq + 0.5 * d_2) - (d_1 + lambda_4)
        _latex.extend([
            f'\\lambda_3=\\frac{{L_H}}{{L_L}}\\left(d_{{aw}}+h_{{eq}}+0.5 d_2\\right)-\\left(d_1+\\lambda_4\\right)',
            f'\\lambda_3=\\frac{{{L_H:.2f}}}{{{L_L:.2f}}}\\left({d_aw:.2f}+{h_eq:.2f}+0.5\\cdot {d_2:.2f}\\right)-\\left({d_1:.2f}+{lambda_4:.2f}\\right)',
        ])

    _latex.extend([
        f'\\lambda_3={lambda_3:.2f}\\ \\left[m\\right]',
    ])
    return dict(lambda_3=lambda_3, _latex=_latex)


def clause_b_5_1_1_5_I_z(
        C_1, C_2, C_3, C_4,
        I_z_1, I_z_2, I_z_3, I_z_4,
        d_1, d_2,
        *_, **__
):
    """
    Clause B.5.1.1 (5), page 62

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
        f'I_z=\\frac{{\\left({I_z_1:.2f}+{I_z_2:.2f}\\right) {d_1:.2f}+\\left({I_z_3:.2f}+{I_z_4:.2f}\\right) {d_2:.2f}}}{{\\left({C_1:.2f}+{C_2:.2f}\\right) {d_1:.2f}+\\left({C_3:.2f}+{C_4:.2f}\\right) {d_2:.2f}}}',
        f'I_z={I_z:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_z=I_z, _latex=_latex)


def clause_b_5_1_2_2_I_z_i(
        C_1, C_2, C_3, C_4,
        epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4,
        sigma,
        T_z_1, T_z_2,
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
    :param T_z_1:
    :param T_z_2:
    :param sigma:
    :param T_o:
    :param is_forced_draught:
    :param is_flame_above_top_of_beam:
    :param _:
    :param __:
    :return:
    """
    # Equation B.22a, B.22b, B.22c, B.22d, page 59
    I_z_1 = C_1 * epsilon_z_1 * sigma * T_o ** 4
    I_z_2 = C_2 * epsilon_z_2 * sigma * T_z_2 ** 4
    I_z_3 = C_3 * epsilon_z_3 * sigma * (T_z_1 ** 4 + T_z_2 ** 4) / 2
    I_z_4 = C_4 * epsilon_z_4 * sigma * (T_z_1 ** 4 + T_z_2 ** 4) / 2

    _latex = [
        f'I_{{z,1}}=C_1\\varepsilon_{{z,1}}\\sigma {{T_o}}^4={C_1:.2f}\\cdot {epsilon_z_1:.3f}\\cdot \\left({sigma:.2E}\\right) {T_o:.2f}^4={I_z_1:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,2}}=C_2\\varepsilon_{{z,2}}\\sigma {{T_{{z,2}}}}^4={C_2:.2f}\\cdot {epsilon_z_2:.3f} \\left({sigma:.2E}\\right) {T_z_2:.2f}^4={I_z_2:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,3}}=\\frac{{C_3\\varepsilon_{{z,3}}\\sigma \\left({{T_{{z,1}}}}^4+{{T_{{z,2}}}}^4\\right)}}{{2}}=\\frac{{{C_3:.2f}\\cdot {epsilon_z_3:.3f} \\left({sigma:.2E}\\right) \\left({{{T_z_1:.2f}}}^4+{{{T_z_2:.2f}}}^4\\right)}}{{2}}={I_z_3:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,4}}=\\frac{{C_4\\varepsilon_{{z,4}}\\sigma \\left({{T_{{z,1}}}}^4+{{T_{{z,2}}}}^4\\right)}}{{2}}=\\frac{{{C_4:.2f}\\cdot {epsilon_z_4:.3f} \\left({sigma:.2E}\\right) \\left({{{T_z_1:.2f}}}^4+{{{T_z_2:.2f}}}^4\\right)}}{{2}}={I_z_4:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_z_1=I_z_1, I_z_2=I_z_2, I_z_3=I_z_3, I_z_4=I_z_4, _latex=_latex)


def clause_b_5_1_2_T_z_1():
    """
    Clause B.5.1.2 (2), page 62
    Radiative heat flux of the external flames for each of the faces 1, 2, 3 and 4 of the column
    """

    pass


def clause_b_5_1_2_T_z_2():
    pass


def clause_b_5_1_2_4_I_z_i(
        C_1, C_3, C_4,
        epsilon_z_1, epsilon_z_3, epsilon_z_4,
        sigma,
        T_z_1,
        T_o,
        h_z,
        d_2,
        T_x: float = 813,  # according to B.5.1.2(4)
        *_, **__
):
    """
    Clause B.4 (1), page 59
    Radiative heat flux of the external flames for each of the faces 1, 2, 3 and 4 of the column

    :param T_x:
    :param C_1:
    :param C_2:
    :param C_3:
    :param C_4:
    :param epsilon_z_1:
    :param epsilon_z_2:
    :param epsilon_z_3:
    :param epsilon_z_4:
    :param T_z_1:
    :param T_z_2:
    :param sigma:
    :param T_o:
    :param is_forced_draught:
    :param is_flame_above_top_of_beam:
    :param _:
    :param __:
    :return:
    """
    # Equation B.23a, B.23b, B.23c, B23d, page 59
    I_z_1 = C_1 * epsilon_z_1 * sigma * T_o ** 4
    I_z_2 = 0
    I_z_3 = (h_z / d_2) * C_3 * epsilon_z_3 * sigma * (T_z_1 ** 4 + T_x ** 4) / 2
    I_z_4 = (h_z / d_2) * C_4 * epsilon_z_4 * sigma * (T_z_1 ** 4 + T_x ** 4) / 2

    _latex = [
        f'I_{{z,1}}=C_1\\varepsilon_{{z,1}}\\sigma {{T_o}}^4={C_1:.2f}\\cdot {epsilon_z_1:.3f}\\cdot \\left({sigma:.2E}\\right) {T_o:.2f}^4={I_z_1:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,2}}={I_z_2:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,3}}=\\frac{{\\frac{{h_z}}{{d_2}} C_3 \\varepsilon_{{z,3}} \\sigma \\left({{T_{{z,1}}}}^4+{{T_x}}^4\\right)}}{{2}}=\\frac{{\\frac{{{h_z:.2f}}}{{{d_2:.2f}}} {C_3:.2f} \\cdot {epsilon_z_3:.3f} \\left({sigma:.2E}\\right) \\left({{{T_z_1:.2f}}}^4+{{{T_x:.2f}}}^4\\right)}}{{2}}={I_z_3:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,4}}=\\frac{{\\frac{{h_z}}{{d_2}} C_4 \\varepsilon_{{z,4}} \\sigma \\left({{T_{{z,1}}}}^4+{{T_x}}^4\\right)}}{{2}}=\\frac{{\\frac{{{h_z:.2f}}}{{{d_2:.2f}}} {C_4:.2f} \\cdot {epsilon_z_4:.3f} \\left({sigma:.2E}\\right) \\left({{{T_z_1:.2f}}}^4+{{{T_x:.2f}}}^4\\right)}}{{2}}={I_z_4:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_z_1=I_z_1, I_z_2=I_z_2, I_z_3=I_z_3, I_z_4=I_z_4, _latex=_latex)


def clause_b_5_1_3_2_I_z_i(
        C_1, C_2, C_3, C_4,
        epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4,
        sigma,
        T_z_1, T_z_2,
        T_o,
        *_, **__
):
    """
    Clause B.5.1.3 (2), page 64
    Radiative heat flux of the external flames for each of the faces 1, 2, 3 and 4 of the column

    :param C_1:
    :param C_2:
    :param C_3:
    :param C_4:
    :param epsilon_z_1:
    :param epsilon_z_2:
    :param epsilon_z_3:
    :param epsilon_z_4:
    :param T_z_1:
    :param T_z_2:
    :param sigma:
    :param T_o:
    :param is_forced_draught:
    :param is_flame_above_top_of_beam:
    :param _:
    :param __:
    :return:
    """
    # Equation B.24a, B.24b, B.24c, B.24d, page 64
    I_z_1 = C_1 * epsilon_z_1 * sigma * T_o ** 4
    I_z_2 = C_2 * epsilon_z_2 * sigma * T_z_2 ** 4
    I_z_3 = C_3 * epsilon_z_3 * sigma * (T_z_1 ** 4 + T_z_2 ** 4) / 2
    I_z_4 = C_4 * epsilon_z_4 * sigma * (T_z_1 ** 4 + T_z_2 ** 4) / 2

    _latex = [
        f'I_{{z,1}}=C_1\\varepsilon_{{z,1}}\\sigma {{T_o}}^4={C_1:.2f}\\cdot {epsilon_z_1:.3f}\\cdot \\left({sigma:.2E}\\right) {T_o:.2f}^4={I_z_1:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,2}}=C_2\\varepsilon_{{z,2}}\\sigma {{T_{{z,2}}}}^4={C_2:.2f}\\cdot {epsilon_z_2:.3f} \\left({sigma:.2E}\\right) {T_z_2:.2f}^4={I_z_2:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,3}}=\\frac{{C_3\\varepsilon_{{z,3}}\\sigma \\left({{T_{{z,1}}}}^4+{{T_{{z,2}}}}^4\\right)}}{{2}}=\\frac{{{C_3:.2f}\\cdot {epsilon_z_3:.3f} \\left({sigma:.2E}\\right) \\left({{{T_z_1:.2f}}}^4+{{{T_z_2:.2f}}}^4\\right)}}{{2}}={I_z_3:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,4}}=\\frac{{C_4\\varepsilon_{{z,4}}\\sigma \\left({{T_{{z,1}}}}^4+{{T_{{z,2}}}}^4\\right)}}{{2}}=\\frac{{{C_4:.2f}\\cdot {epsilon_z_4:.3f} \\left({sigma:.2E}\\right) \\left({{{T_z_1:.2f}}}^4+{{{T_z_2:.2f}}}^4\\right)}}{{2}}={I_z_4:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_z_1=I_z_1, I_z_2=I_z_2, I_z_3=I_z_3, I_z_4=I_z_4, _latex=_latex)


def clause_b_5_1_3_3_I_z_i(
        C_1, C_2, C_3,
        epsilon_z_1, epsilon_z_2, epsilon_z_3,
        sigma,
        T_z_1, T_z_2,
        phi_z_2, phi_z_3,
        T_o,
        *_, **__
):
    """
    Clause B.5.1.3 (3), page 64
    Radiative heat flux of the external flames for each of the faces 1, 2, 3 and 4 of the column

    :param C_1:
    :param C_2:
    :param C_3:
    :param C_4:
    :param epsilon_z_1:
    :param epsilon_z_2:
    :param epsilon_z_3:
    :param epsilon_z_4:
    :param T_z_1:
    :param T_z_2:
    :param sigma:
    :param T_o:
    :param is_forced_draught:
    :param is_flame_above_top_of_beam:
    :param _:
    :param __:
    :return:
    """
    # Equation B.25a, B.25b, B.25c, B.25d, page 64
    I_z_1 = C_1 * epsilon_z_1 * sigma * T_o ** 4
    I_z_2 = phi_z_2 * C_2 * epsilon_z_2 * sigma * T_z_2 ** 4
    I_z_3 = phi_z_3 * C_3 * epsilon_z_3 * sigma * (T_z_1 ** 4 + T_z_2 ** 4) / 2
    I_z_4 = 0

    _latex = [
        f'I_{{z,1}}=C_1\\varepsilon_{{z,1}}\\sigma {{T_o}}^4={C_1:.2f}\\cdot {epsilon_z_1:.3f}\\cdot \\left({sigma:.2E}\\right) {T_o:.2f}^4={I_z_1:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,2}}=\\phi_{{z,2}}C_2\\varepsilon_{{z,2}}\\sigma {{T_{{z,2}}}}^4={C_2:.2f}\\cdot {epsilon_z_2:.3f} \\left({sigma:.2E}\\right) {T_z_2:.2f}^4={I_z_2:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,3}}=\\phi_{{z,3}}C_3\\varepsilon_{{z,3}}\\sigma \\frac{{{{T_{{z,1}}}}^4+T_{{z,2}}^4}}{{2}}={phi_z_3:.3f}\\cdot {C_3:.2f}\\cdot {epsilon_z_3:.3f} \\left({sigma:.2E}\\right) \\frac{{{{{T_z_1:.2f}}}^4+{T_z_2}^4}}{{2}}={I_z_3:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
        f'I_{{z,4}}={I_z_4:.2f}\\ \\left[\\frac{{kW}}{{m^2}}\\right]',
    ]

    return dict(I_z_1=I_z_1, I_z_2=I_z_2, I_z_3=I_z_3, I_z_4=I_z_4, _latex=_latex)


def clause_b_5_2_1_epsilon_z_i(
        lambda_1,
        lambda_2,
        lambda_3,
        lambda_4,
        *_,
        **__
):
    """
    Clause B.5.2 (1), page 64
    Emissivity of the external flames for each of the faces 1, 2, 3 and 4 of the beam

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


def clause_b_5_3_a_z(
        lambda_1,
        *_, **__
):
    """
    Clause B.5.3 (1), page 64
    Absorptivity of the flame.

    :param lambda_1: height of the opening
    :param _:
    :param __:
    :return:
    """

    # Equation B.26, page 64
    a_z = 1 - e ** (-0.3 * lambda_1)
    _latex = [
        f'a_z=1-e^{{-0.3h}}',
        f'a_z=1-e^{{-0.3\\cdot {lambda_1:.2f}}}',
        f'a_z={a_z:.4f}\\ \\left[-\\right]'
    ]
    return dict(a_z=a_z, _latex=_latex)


if __name__ == '__main__':
    # _test_clause_b_1_3_3_T_m()
    # _test_clause_b_4_1_lambda_4()
    _test_clause_b_2_1_2_I_z()
    _test_clause_b_2_1_3_I_z()
    _test_clause_b_2_2_1_lambda()
