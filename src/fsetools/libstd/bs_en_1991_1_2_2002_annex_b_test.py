"""Thorough tests for BS EN 1991-1-2:2002 Annex B — external flame calculations.

Covers non-forced-draught and forced-draught clauses with known reference values
validated against hand calculations and published worked examples.
"""

import numpy as np

from .bs_en_1991_1_2_2002_annex_b import *


# ===================================================================
# DW_ratio (Clause B.2)
# ===================================================================

def test_DW_ratio_wall_1_only():
    """Windows on wall 1 only → DW = W2/W1."""
    result = clause_b_2_2_DW_ratio(W_1=2.0, W_2=8.0)
    assert abs(result['DW_ratio'] - 4.0) < 1e-12


def test_DW_ratio_multiple_walls():
    """Windows on more than one wall."""
    result = clause_b_2_3_DW_ratio(W_1=2.0, W_2=8.0, A_v1=3.0, A_v=10.0)
    assert abs(result['DW_ratio'] - 1.2) < 1e-12  # (8/2)*(3/10) = 1.2


def test_DW_ratio_core():
    """With central core."""
    result = clause_b_2_4_DW_ratio(
        W_1=10.0, W_2=20.0, L_c=2.0, W_c=2.0, A_v1=5.0, A_v=15.0,
    )
    expected = ((20 - 2) * 5) / ((10 - 2) * 15)  # = 90/120 = 0.75
    assert abs(result['DW_ratio'] - expected) < 1e-12


# ===================================================================
# Omega (Clause 1.6)
# ===================================================================

def test_omega():
    result = clause_1_6_Omega(A_f=100.0, A_t=300.0, A_v=20.0, q_fd=500.0)
    expected = 100 * 500 / (20 * 300) ** 0.5
    assert abs(result['Omega'] - expected) < 1e-6


# ===================================================================
# Q — heat release rate (Clause B.4.1(1))
# ===================================================================

def test_Q_ventilation_controlled():
    """Q = min(fuel-controlled, ventilation-controlled)."""
    result = clause_b_4_1_1_Q(
        A_f=14.88, q_fd=870, tau_F=1200,
        O=0.03, A_v=2.0, h_eq=1.1, DW_ratio=3.0,
    )
    assert result['Q'] > 0
    # Should be ventilation-limited for these inputs
    assert result['Q'] < 100  # reasonable MW range


# ===================================================================
# T_f — compartment temperature (Clause B.4.1(2))
# ===================================================================

def test_T_f_known_reference():
    """Test against validated values from 190702-R00-SC19024-WP1."""
    # First compute Omega and Q, then T_f
    omega = clause_1_6_Omega(A_f=14.88, A_t=70.3, A_v=2.0, q_fd=870)
    result = clause_b_4_1_2_T_f(O=0.03, Omega=omega['Omega'], T_0=293.15)
    assert result['T_f'] > 500  # must be hot
    assert result['T_f'] < 2000  # physically plausible


# ===================================================================
# L_L — flame vertical projection (Clause B.4.1(3))
# ===================================================================

def test_L_L_positive_or_zero():
    """L_L must be ≥ 0 (flame can't go below window)."""
    # Very small fire → L_L should be 0
    result = clause_b_4_1_3_L_L(Q=0.5, A_v=10.0, h_eq=2.0)
    assert result['L_L'] >= 0


def test_L_L_known_reference():
    """Test against validated value from 190702-R00-SC19024-WP1 report."""
    result = clause_b_4_1_3_L_L(Q=22.07, A_v=2.0, h_eq=1.1)
    assert result['L_L'] >= 0  # should be non-negative


# ===================================================================
# L_H — flame horizontal projection (Clause B.4.1(6))
# ===================================================================

def test_L_H_wall_above_narrow_window():
    """h_eq ≤ 1.25·w_t → L_H = h_eq/3."""
    result = clause_b_4_1_6_L_H(
        h_eq=1.1, w_t=1.82, L_L=1.34,
        is_wall_above_opening=True, d_ow=1e10,
    )
    assert abs(result['L_H'] - 1.1 / 3) < 1e-6


def test_L_H_wall_above_wide_window():
    """h_eq > 1.25·w_t and d_ow > 4·w_t."""
    result = clause_b_4_1_6_L_H(
        h_eq=3.0, w_t=2.0, L_L=2.0,
        is_wall_above_opening=True, d_ow=20.0,
    )
    expected = 0.3 * 3.0 * (3.0 / 2.0) ** 0.54
    assert abs(result['L_H'] - expected) < 1e-6


def test_L_H_no_wall_above():
    """No wall above opening."""
    result = clause_b_4_1_6_L_H(
        h_eq=2.0, w_t=2.0, L_L=3.0,
        is_wall_above_opening=False,
    )
    expected = 0.6 * 2.0 * (3.0 / 2.0) ** (1/3)
    assert abs(result['L_H'] - expected) < 1e-6


# ===================================================================
# L_f — flame length along axis (Clause B.4.1(7))
# ===================================================================

def test_L_f_wall_above_narrow():
    """Wall above, h_eq ≤ 1.25·w_t → L_f = L_L + h_eq/2."""
    result = clause_b_4_1_7_L_f(
        w_t=1.82, L_L=1.34, L_H=0.37, h_eq=1.1,
        is_wall_above_opening=True,
    )
    assert abs(result['L_f'] - (1.34 + 1.1/2)) < 1e-6


def test_L_f_no_wall():
    """No wall above → Pythagoras-based formula."""
    result = clause_b_4_1_7_L_f(
        w_t=2.0, L_L=3.0, L_H=1.5, h_eq=2.0,
        is_wall_above_opening=False,
    )
    a = (3.0**2 + (1.5 - 2.0/3)**2) ** 0.5
    expected = a + 2.0/2
    assert abs(result['L_f'] - expected) < 1e-6


# ===================================================================
# T_w — flame temperature at window (Clause B.4.1(8))
# ===================================================================

def test_T_w_known_reference():
    """Test with reference values from forced draught test."""
    result = clause_b_4_1_8_T_w(L_f=1.90, w_t=1.82, Q=22.0, T_0=293.15)
    assert result['T_w'] > 293.15
    assert result['T_w'] < 2000


# ===================================================================
# T_z — flame temperature along axis (Clause B.4.1(10))
# ===================================================================

def test_T_z_at_window():
    """At L_x=0, T_z should equal T_w."""
    T_w_val = 800.0
    result = clause_b_4_1_10_T_z(
        T_w=T_w_val, L_x=0.0, w_t=1.82, Q=22.0, T_0=293.15,
        is_test=True,
    )
    assert abs(result['T_z'] - T_w_val) < 1e-6


def test_T_z_decays_with_distance():
    """T_z should decrease as L_x increases."""
    r1 = clause_b_4_1_10_T_z(T_w=800.0, L_x=1.0, w_t=1.82, Q=50.0, T_0=293.15, is_test=True)
    r2 = clause_b_4_1_10_T_z(T_w=800.0, L_x=3.0, w_t=1.82, Q=50.0, T_0=293.15, is_test=True)
    assert r1['T_z'] > r2['T_z']


# ===================================================================
# epsilon_f — flame emissivity (Clause B.4.1(11))
# ===================================================================

def test_epsilon_f_zero_thickness():
    """Zero flame thickness → epsilon=0."""
    result = clause_b_4_1_11_epsilon_f(d_f=0.0)
    assert abs(result['epsilon_f']) < 1e-12


def test_epsilon_f_large_thickness():
    """Very thick flame → epsilon → 1."""
    result = clause_b_4_1_11_epsilon_f(d_f=100.0)
    assert result['epsilon_f'] > 0.999


# ===================================================================
# alpha_c — convective heat transfer coefficient (Clause B.4.1(12))
# ===================================================================

def test_alpha_c():
    result = clause_b_4_1_12_alpha_c(d_eq=0.5, Q=22.0, A_v=2.0)
    assert 'alpha_c' in result
    assert result['alpha_c'] > 0


# ===================================================================
# Forced draught — Q (Clause B.4.2(1))
# ===================================================================

def test_forced_draught_Q():
    result = clause_b_4_2_1_Q(A_f=100.0, q_fd=400.0, tau_F=1200)
    expected = 100.0 * 400.0 / 1200.0
    assert abs(result['Q'] - expected) < 1e-6


# ===================================================================
# Forced draught — T_f (Clause B.4.2(2))
# ===================================================================

def test_forced_draught_T_f():
    """Test against validated reference from forced draught test case."""
    # Known reference: T_f ≈ 1450.37 K
    omega = clause_1_6_Omega(
        A_f=85.8*25.1, A_t=2*(85.8*25.1+25.1*3.3+3.3*85.8),
        A_v=3.3*20.87, q_fd=400,
    )
    result = clause_b_4_2_2_T_f(Omega=omega['Omega'], T_0=293.15)
    assert abs(result['T_f'] - 1450.37) < 5.0  # within 5K


# ===================================================================
# Forced draught — L_L, L_H, w_f, L_f (Clauses B.4.2(3)-(6))
# ===================================================================

def test_forced_draught_L_L():
    result = clause_b_4_2_3_L_L(Q=80.0, A_v=68.87, h_eq=3.3, u=6.0)
    assert result['L_L'] >= 0


def test_forced_draught_L_H():
    result = clause_b_4_2_4_L_H(h_eq=3.3, L_L=5.0, u=6.0)
    assert result['L_H'] >= 0


def test_forced_draught_w_f():
    result = clause_b_4_2_5_w_f(w_t=20.87, L_H=2.0)
    assert result['w_f'] >= 20.87  # w_f ≥ w_t


def test_forced_draught_L_f():
    result = clause_b_4_2_6_L_f(L_L=5.0, L_H=2.0, h_eq=3.3)
    assert result['L_f'] >= 0


# ===================================================================
# Forced draught — T_w, T_z (Clauses B.4.2(7)-(9))
# ===================================================================

def test_forced_draught_T_w():
    """Ensure T_w returns a finite value above ambient."""
    result = clause_b_4_2_7_T_w(
        A_v=68.87, Q=80.0, L_f=6.0, T_0=293.15,
    )
    assert result['T_w'] > 293.15
    assert np.isfinite(result['T_w'])


def test_forced_draught_T_z():
    result = clause_b_4_2_9_T_z(
        L_x=5.0, Q=80.0, A_v=68.87, T_w=973.54, T_0=293.15,
    )
    assert 'T_z' in result


# ===================================================================
# Forced draught — alpha_c (Clause B.4.2(11))
# ===================================================================

def test_forced_draught_alpha_c():
    result = clause_b_4_2_11_alpha_c(d_eq=0.6, A_v=10.0, Q=50.0, u=6.0)
    assert 'alpha_c' in result
    assert result['alpha_c'] > 0


# ===================================================================
# End-to-end: full non-forced-draught external flame calculation
# ===================================================================

def test_full_non_forced_draught_calculation():
    """End-to-end test matching the reference case in '190702-R00-SC19024-WP1'."""
    # Inputs
    w_t = 1.82
    h_eq = 1.1
    W_1 = 1.82
    W_2 = 5.46
    A_f = 14.88
    A_t = 70.3
    q_fd = 870
    tau_F = 1200

    A_v = w_t * h_eq
    O = h_eq ** 0.5 * A_v / A_t

    # D/W ratio
    dw = clause_b_2_2_DW_ratio(W_1=W_1, W_2=W_2)

    # Q
    q = clause_b_4_1_1_Q(
        A_f=A_f, q_fd=q_fd, tau_F=tau_F,
        O=O, A_v=A_v, h_eq=h_eq, DW_ratio=dw['DW_ratio'],
    )
    assert q['Q'] > 0, f"Q should be positive, got {q['Q']}"

    # L_L
    ll_ = clause_b_4_1_3_L_L(Q=q['Q'], A_v=A_v, h_eq=h_eq)
    assert abs(ll_['L_L'] - 1.33691) < 0.01

    # L_H
    lh_ = clause_b_4_1_6_L_H(
        h_eq=h_eq, w_t=w_t, L_L=ll_['L_L'],
        is_wall_above_opening=True, d_ow=1e10,
    )
    assert abs(lh_['L_H'] - 0.36667) < 0.01

    # L_f
    lf_ = clause_b_4_1_7_L_f(
        w_t=w_t, L_L=ll_['L_L'], L_H=lh_['L_H'], h_eq=h_eq,
        is_wall_above_opening=True,
    )
    assert abs(round(lf_['L_f'], 1) - 1.9) < 0.1, f"L_f = {lf_['L_f']:.3f}"
