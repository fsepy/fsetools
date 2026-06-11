"""Tests for BS EN 13381-8:2013 protected steel heat transfer.

Validates basic physical invariants of the iterative solver.
"""

import numpy as np

from .heat_transfer_protected_steel_bs13381 import protected_steel_bs13381


# ---------------------------------------------------------------------------
# Material property helpers
# ---------------------------------------------------------------------------

def _c_steel(T_K):
    """Specific heat of carbon steel [J/kg/K] — BS EN 1993-1-2:2005 §3.4.1.2."""
    T = T_K - 273.15
    if T < 20:
        return 425 + 0.773 * 20 - 1.69e-3 * 400 + 2.22e-6 * 8000
    elif T < 600:
        return 425 + 0.773 * T - 1.69e-3 * T**2 + 2.22e-6 * T**3
    elif T < 735:
        return 666.0 + 13002.0 / (738.0 - T)
    elif T < 900:
        return 545.0 + 17820.0 / (T - 731.0)
    else:
        return 650.0


def _c_steel_vec(T):
    """Vectorized wrapper — handles both scalar and array inputs."""
    if np.ndim(T) == 0:
        return _c_steel(float(T))
    return np.array([_c_steel(float(t)) for t in T])


def _rho_steel(T_K):
    """Density of steel [kg/m³] — constant per §3.4.1.2."""
    return 7850.0


def _lambda_protection(T_K):
    """Thermal conductivity of protection [W/m/K] — constant."""
    return 0.12


def _iso_834_fire(t):
    """ISO 834 standard fire curve [K]."""
    return 345.0 * np.log10((t / 60.0) * 8.0 + 1.0) + 293.15


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_bs13381_returns_arrays():
    """Output should be numpy arrays with matching shapes."""
    t = np.arange(0, 1800, 30.0)
    T_g = _iso_834_fire(t)

    time_out, T_steel, time_rate, temp_rate = protected_steel_bs13381(
        time=t, temperature_ambient=T_g,
        lambda_pt_T=_lambda_protection,
        d_p=0.015, A_p=2.14, V=0.017,
        c_a_T=_c_steel_vec, rho_a_T=_rho_steel,
        time_ubound=900, time_step_lbound=30.0,
    )

    assert len(time_out) > 0
    assert len(time_out) == len(T_steel)
    assert len(time_rate) == len(temp_rate)
    assert isinstance(time_out, np.ndarray)
    assert isinstance(T_steel, np.ndarray)


def test_bs13381_steel_starts_at_ambient():
    """Steel temperature at t=0 should equal initial gas temperature."""
    t = np.arange(0, 1800, 30.0)
    T_g = _iso_834_fire(t)

    time_out, T_steel, _, _ = protected_steel_bs13381(
        time=t, temperature_ambient=T_g,
        lambda_pt_T=_lambda_protection,
        d_p=0.015, A_p=2.14, V=0.017,
        c_a_T=_c_steel_vec, rho_a_T=_rho_steel,
        time_ubound=900, time_step_lbound=30.0,
    )

    assert abs(T_steel[0] - T_g[0]) < 1.0


def test_bs13381_steel_below_gas():
    """Steel temperature must be below or equal to gas temperature."""
    t = np.arange(0, 3600, 30.0)
    T_g = _iso_834_fire(t)

    time_out, T_steel, _, _ = protected_steel_bs13381(
        time=t, temperature_ambient=T_g,
        lambda_pt_T=_lambda_protection,
        d_p=0.015, A_p=2.14, V=0.017,
        c_a_T=_c_steel_vec, rho_a_T=_rho_steel,
        time_ubound=1800, time_step_lbound=30.0,
    )

    T_g_interp = np.interp(time_out, t, T_g)
    # Steel must not exceed gas by more than a small tolerance
    max_excess = np.max(T_steel - T_g_interp)
    assert max_excess < 1.0, f"Steel exceeded gas by {max_excess:.1f} K"


def test_bs13381_finite_result():
    """Temperature should be finite throughout."""
    t = np.arange(0, 1800, 30.0)
    T_g = _iso_834_fire(t)

    time_out, T_steel, _, _ = protected_steel_bs13381(
        time=t, temperature_ambient=T_g,
        lambda_pt_T=_lambda_protection,
        d_p=0.015, A_p=2.14, V=0.017,
        c_a_T=_c_steel_vec, rho_a_T=_rho_steel,
        time_ubound=900, time_step_lbound=30.0,
    )

    assert np.all(np.isfinite(T_steel))
    assert np.all(np.isfinite(time_out))
    assert np.min(T_steel) >= 273.15  # physically plausible minimum
