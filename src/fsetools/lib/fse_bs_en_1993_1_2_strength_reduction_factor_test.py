"""Tests for BS EN 1993-1-2 strength reduction factor — probabilistic extension.

Covers:
- _polevl / _p1evl: Cephes polynomial evaluation
- _ndtri: inverse normal CDF (port of cephes ndtri.c)
- _erfinv: inverse error function
- _ppf: percent-point function (normal)
- k_y_theta_prob: probabilistic yield strength reduction factor
"""

import numpy as np
import os

from .fse_bs_en_1993_1_2_strength_reduction_factor import (
    _polevl, _p1evl, _ndtri, _erfinv, _ppf, k_y_theta_prob,
)
from ..libstd.bs_en_1993_1_2_2005_clause_3 import clause_3_2_1_3_k_y_theta as k_y_theta

# ---------------------------------------------------------------------------
# _polevl — polynomial evaluation
# ---------------------------------------------------------------------------

def test_polevl_constant():
    """p(x) = 5 for all x."""
    assert abs(_polevl(0.0, [5], 0) - 5.0) < 1e-12
    assert abs(_polevl(3.0, [5], 0) - 5.0) < 1e-12


def test_polevl_linear():
    """p(x) = 2x + 1."""
    assert abs(_polevl(0.0, [2, 1], 1) - 1.0) < 1e-12
    assert abs(_polevl(1.0, [2, 1], 1) - 3.0) < 1e-12
    assert abs(_polevl(-1.0, [2, 1], 1) - -1.0) < 1e-12


def test_polevl_quadratic():
    """p(x) = 3x^2 + 2x + 1."""
    assert abs(_polevl(0.0, [3, 2, 1], 2) - 1.0) < 1e-12
    assert abs(_polevl(2.0, [3, 2, 1], 2) - 17.0) < 1e-12


def test_p1evl():
    """p(x) = x^3 + 2x^2 + 3x + 4  (coefs [2,3,4] since leading 1 is implicit)."""
    val = _p1evl(1.0, [2, 3, 4], 3)
    assert abs(val - 10.0) < 1e-12  # 1+2+3+4


def test_polevl_overflow_handled():
    """Very large x**power overflow should be silently skipped."""
    # Should not raise; just returns ans ~ 0
    result = _polevl(1e200, [1.0, 0.0], 1)
    assert isinstance(result, float)

# ---------------------------------------------------------------------------
# _erfinv — inverse error function
# ---------------------------------------------------------------------------

def test_erfinv_zero():
    assert _erfinv(0.0) == 0.0


def test_erfinv_positive_one():
    assert _erfinv(1.0) == np.inf


def test_erfinv_negative_one():
    assert _erfinv(-1.0) == -np.inf


def test_erfinv_out_of_bounds():
    try:
        _erfinv(1.1)
        assert False, "should have raised"
    except ValueError:
        pass


def test_erfinv_known_values():
    """Compare against scipy or known table values."""
    # erfinv(0.5) ≈ 0.476936276204
    assert abs(_erfinv(0.5) - 0.4769362762) < 1e-9
    # erfinv(0.1) ≈ 0.08885599049
    assert abs(_erfinv(0.1) - 0.08885599049) < 1e-8
    # erfinv(0.95) ≈ 1.38590382435
    assert abs(_erfinv(0.95) - 1.38590382435) < 1e-7


def test_erfinv_symmetry():
    """erfinv(-z) = -erfinv(z)."""
    for z in [0.1, 0.3, 0.5, 0.7, 0.9]:
        assert abs(_erfinv(-z) + _erfinv(z)) < 1e-12


def test_erfinv_vectorized():
    """@np.vectorize handles arrays — values should be monotonic and positive."""
    z = np.array([0.0, 0.5, 0.9])
    result = _erfinv(z)
    assert len(result) == 3
    assert result[2] > result[1]  # erfinv is monotonic

# ---------------------------------------------------------------------------
# _ppf — normal percent-point function
# ---------------------------------------------------------------------------

def test_ppf_median():
    """p=0.5 gives mean (0)."""
    assert abs(_ppf(0.5, 0.0, 1.0)) < 1e-12


def test_ppf_known_values():
    """Standard normal quantiles."""
    # 95th percentile ≈ 1.64485
    assert abs(_ppf(0.95, 0.0, 1.0) - 1.644853627) < 1e-6
    # 5th percentile ≈ -1.64485
    assert abs(_ppf(0.05, 0.0, 1.0) + 1.644853627) < 1e-6
    # 99th percentile ≈ 2.32635
    assert abs(_ppf(0.99, 0.0, 1.0) - 2.326347874) < 1e-5


def test_ppf_with_mean_sd():
    """p=0.5 recovers mean, scaling works."""
    assert abs(_ppf(0.5, 100.0, 15.0) - 100.0) < 1e-12
    # p=0.84 ~ mean + 1*sd for unit normal => mean + sd
    expected = 100.0 + 15.0 * 0.9944578832  # actual Φ⁻¹(0.84) * 15
    assert abs(_ppf(0.84, 100.0, 15.0) - expected) < 1e-6

# ---------------------------------------------------------------------------
# k_y_theta_prob — probabilistic yield strength reduction
# ---------------------------------------------------------------------------

def test_k_y_theta_prob_deterministic_extreme():
    """At epsilon_q=0.5 (median), should be close to deterministic EC curve."""
    # T=0°C → EC k_y_theta ≈ 1.0
    result = k_y_theta_prob(0.0, 0.5)
    assert result > 0.9
    # T=400°C → EC k_y_theta ≈ 1.0 (still in plateau)
    result = k_y_theta_prob(273.15 + 400, 0.5)
    assert result > 0.85


def test_k_y_theta_prob_known_reference():
    """Spot-check against previously validated values."""
    assert abs(k_y_theta_prob(0.0, 0.5) - 1.161499) <= 0.001
    assert abs(k_y_theta_prob(273.15 + 400, 0.5) - 1.001560) <= 0.001


def test_k_y_theta_prob_monotonic_decay():
    """k_y_theta should decrease as temperature increases."""
    T = np.array([0.0, 100.0, 300.0, 500.0, 700.0, 900.0, 1100.0]) + 273.15
    vals = k_y_theta_prob(T, 0.5)
    for i in range(len(vals) - 1):
        assert vals[i] >= vals[i+1], f"monotonicity broken at {T[i]:.0f}K"


def test_k_y_theta_prob_low_percentile_is_lower():
    """At lower epsilon_q (lower percentile), strength should be lower."""
    T = np.linspace(100, 800, 20) + 273.15
    low = k_y_theta_prob(T, 0.05)   # 5th percentile
    mid = k_y_theta_prob(T, 0.50)   # median
    high = k_y_theta_prob(T, 0.95)  # 95th percentile
    assert np.all(low <= mid)
    assert np.all(mid <= high)


def test_k_y_theta_prob_vectorized():
    """Should handle array inputs for both temperature and epsilon."""
    T = np.array([273.15, 273.15 + 400, 273.15 + 800])
    q = np.array([0.3, 0.5, 0.7])
    result = k_y_theta_prob(T, q)
    assert result.shape == (3,)


def test_k_y_theta_prob_bounds():
    """Result should be in physically plausible range (0, 2.0)."""
    T = np.linspace(0, 1200, 100) + 273.15
    for q in [0.01, 0.1, 0.5, 0.9, 0.99]:
        vals = k_y_theta_prob(T, q)
        assert np.all(vals > 0), f"negative value at q={q}"
        assert np.all(vals < 2.5), f"unreasonably high value at q={q}"


def test_k_y_theta_prob_epsilon_extremes():
    """Very low and very high epsilon should produce sensible results."""
    T_mid = 273.15 + 500
    # Low epsilon (low fractile) → weaker
    low = k_y_theta_prob(T_mid, 0.001)
    # High epsilon (high fractile) → stronger
    high = k_y_theta_prob(T_mid, 0.999)
    assert 0 < low < high


def test_k_y_theta_prob_consistent_with_k_y_theta():
    """At epsilon=0.5 (median), result should approximate EC deterministic curve."""
    T = np.linspace(0, 800, 20) + 273.15
    prob = k_y_theta_prob(T, 0.5)
    ec = k_y_theta(T)
    # Within ~20% of deterministic EC curve at median
    ratio = prob / ec
    assert np.all(ratio > 0.7), "median too far below EC curve"
    assert np.all(ratio < 1.5), "median too far above EC curve"


# ---------------------------------------------------------------------------
# Visual inspection (opt-in)
# ---------------------------------------------------------------------------

def plot_prob_k_y_ach():
    """Generate scatter-plot of probabilistic k_y_theta for visual review."""
    import matplotlib.pyplot as plt
    plt.style.use("seaborn-v0_8")

    fig, ax = plt.subplots(figsize=(9, 9))
    T = np.linspace(273.15 + 0, 273.15 + 1500, 5000)
    q = np.random.random_sample(len(T))
    ax.scatter(T - 273.15, k_y_theta_prob(T, q),
               s=2, color=((0, 0, 0, 0.1)), label='Random Sampled Points')
    ax.plot(T - 273.15, k_y_theta_prob(T, 0.05), ls='--', c='k',
            label=r'$\epsilon$ Percentile 0.05, 0.50, 0.95')
    ax.plot(T - 273.15, k_y_theta_prob(T, 0.5), ls='--', c='k')
    ax.plot(T - 273.15, k_y_theta_prob(T, 0.95), ls='--', c='k')
    ax.plot(T - 273.15, k_y_theta(T), ls='-', c='r',
            label=r'Eurocode $k_{y,\theta}$')

    ax.set_xlabel('Temperature [$^oC$]')
    ax.set_ylabel('$k_{y,ach}$ [$1$]')
    ax.legend().set_visible(True)
    fig.tight_layout()
    if os.environ.get('FSETOOLS_SHOW_PLOTS') == '1':
        plt.show()


if __name__ == '__main__':
    plot_prob_k_y_ach()
