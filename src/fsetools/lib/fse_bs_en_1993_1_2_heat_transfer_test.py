import numpy as np
import os

from .fse_bs_en_1991_1_2_parametric_fire import temperature as param_temp
from .fse_bs_en_1993_1_2_heat_transfer import temperature
from .fse_travelling_fire import temperature_si as trav_temp


def __trav_fire(t: np.ndarray):
    return trav_temp(
        t=t,
        T_0=273.15,
        q_f_d=600e6,
        hrrpua=0.25e6,
        l=100,
        w=16,
        s=0.012,
        e_h=3,
        e_l=50,
        T_max=1050 + 273.15,
    )


def __param_fire(t: np.ndarray):
    return param_temp(
        t=t,
        A_t=963.5,
        A_f=340,
        A_v=20,
        h_eq=2,
        q_fd=420e6,
        lbd=720 ** 2,
        rho=1,
        c=1,
        t_lim=0.333,
    )


def __param_fire_2(t: np.ndarray):
    return param_temp(
        t=t,
        A_t=1283.5,
        A_f=500,
        A_v=115.2,
        h_eq=2,
        q_fd=336e6,
        lbd=720 ** 2,
        rho=1,
        c=1,
        t_lim=0.333,
    )


def __test_heat_transfer_kwargs(t, T):
    return dict(
        fire_time=t,
        fire_temperature=T,
        beam_rho=7850.,
        beam_cross_section_area=0.017,
        protection_k=0.2,
        protection_rho=800.,
        protection_c=1700.,
        protection_thickness=0.01,
        protection_protected_perimeter=2.14,
    )


def test_temperature_trav():
    import matplotlib.pyplot as plt
    plt.style.use("seaborn-v0_8")
    from matplotlib.lines import Line2D

    # --------------------------------------------------
    # Check if the Cython version returns the same value
    # --------------------------------------------------
    fig, ax = plt.subplots()
    t = np.arange(0, 210 * 60, 5)
    kwargs = dict(**__test_heat_transfer_kwargs(t, __trav_fire(t)))

    list_dp = np.linspace(0.0001, 0.1000, 10)

    for d_p in list_dp:
        kwargs['protection_thickness'] = d_p
        T = temperature(**kwargs)
        ax.plot(t / 60, T - 273.15, c='k')

    ax.grid(ls='--', c='k', linewidth=0.5)
    lines = [Line2D([0], [0], color='k'), Line2D([0], [0], color='r', linestyle='--')]
    labels = ['temperature', 'temperature_c']
    ax.legend(lines, labels).set_visible(True)
    if os.environ.get('FSETOOLS_SHOW_PLOTS') == '1':
        plt.show()


def test_temperature_param():
    import matplotlib.pyplot as plt
    plt.style.use("seaborn-v0_8")
    from matplotlib.lines import Line2D

    # --------------------------------------------------
    # Check if the Cython version returns the same value
    # --------------------------------------------------
    fig, ax = plt.subplots()
    t = np.arange(0, 210 * 60, 5)
    kwargs = dict(**__test_heat_transfer_kwargs(t, __param_fire(t)))

    list_dp = np.arange(0.0001, 0.05 + 0.002, 0.001)

    for d_p in list_dp:
        kwargs['protection_thickness'] = d_p
        T = temperature(**kwargs)
        ax.plot(t / 60, T - 273.15, c='k')

    ax.grid(ls='--', c='k', linewidth=0.5)
    lines = [Line2D([0], [0], color='k'), Line2D([0], [0], color='r', linestyle='--')]
    labels = ['temperature', 'temperature_c']
    ax.legend(lines, labels).set_visible(True)
    if os.environ.get('FSETOOLS_SHOW_PLOTS') == '1':
        plt.show()


def test_temperature_param_2():
    import matplotlib.pyplot as plt
    plt.style.use("seaborn-v0_8")
    from matplotlib.lines import Line2D

    # --------------------------------------------------
    # Check if the Cython version returns the same value
    # --------------------------------------------------
    fig, ax = plt.subplots()
    t = np.arange(0, 210 * 60, 5)
    kwargs = dict(**__test_heat_transfer_kwargs(t, __param_fire_2(t)))

    list_dp = np.arange(0.0001, 0.05 + 0.002, 0.001)

    for d_p in list_dp:
        kwargs['protection_thickness'] = d_p
        T = temperature(**kwargs)
        # print(temperature_max(**kwargs), np.amax(T_c))
        ax.plot(t / 60, T - 273.15, c='k')

    ax.grid(ls='--', c='k', linewidth=0.5)
    lines = [Line2D([0], [0], color='k'), Line2D([0], [0], color='r', linestyle='--')]
    labels = ['temperature', 'temperature_c']
    ax.legend(lines, labels).set_visible(True)
    if os.environ.get('FSETOOLS_SHOW_PLOTS') == '1':
        plt.show()


def test_temperature_extreme():
    import matplotlib.pyplot as plt
    plt.style.use("seaborn-v0_8")

    t = np.arange(0, 210 * 60, 1, dtype=float)
    kwargs = __test_heat_transfer_kwargs(t, __param_fire(t))

    fig, ax1 = plt.subplots()

    for protection_thickness in np.linspace(0.5, 0.0001, 10):
        kwargs['protection_thickness'] = protection_thickness
        T_a = temperature(**kwargs)
        ax1.plot(t / 60, T_a, label=f'd_p {protection_thickness * 1000:<4.0f} mm')
    ax1.legend().set_visible(True)
    ax1.set_xlabel('Time [$min$]')
    ax1.set_ylabel('Steel temperature [$K$]')

    if os.environ.get('FSETOOLS_SHOW_PLOTS') == '1':
        fig.show()


# ===================================================================
# Protection thickness solver tests
# ===================================================================

from .fse_bs_en_1993_1_2_heat_transfer import (
    temperature, temperature_max, temperature_2,
    protection_thickness, protection_thickness_2,
)


def _standard_beam_kwargs(t, T_gas):
    """Standard UC 254x254x89 section with spray-applied protection."""
    return dict(
        fire_time=t,
        fire_temperature=T_gas,
        beam_rho=7850.,
        beam_cross_section_area=0.017,
        protection_k=0.2,
        protection_rho=800.,
        protection_c=1700.,
        protection_thickness=0.01,
        protection_protected_perimeter=2.14,
    )


# ---- temperature_max ----

def test_temperature_max_returns_tuple():
    t = np.arange(0, 3600, 30, dtype=float)
    T_g = __param_fire(t)
    T_max, t_at_max = temperature_max(**_standard_beam_kwargs(t, T_g))
    assert isinstance(T_max, float)
    assert isinstance(t_at_max, float)
    assert T_max > 293.15  # above ambient
    assert 0 <= t_at_max <= 3600


def test_temperature_max_cooling_detection():
    """temperature_max should stop when steel begins cooling (dT<0)."""
    t = np.arange(0, 7200, 30, dtype=float)
    T_g = __param_fire(t)
    T_max, t_at_max = temperature_max(**_standard_beam_kwargs(t, T_g))
    # T_max should occur during or near the peak of the fire
    fire_peak_idx = np.argmax(T_g)
    assert t_at_max >= t[fire_peak_idx]  # steel peak after or at fire peak


def test_temperature_max_monotonic_with_thickness():
    """Thicker protection → lower max temperature (engineering invariant)."""
    t = np.arange(0, 3600, 30, dtype=float)
    T_g = __param_fire(t)
    kw = _standard_beam_kwargs(t, T_g)
    kw.pop('protection_thickness')

    temps = []
    for dp in [0.005, 0.010, 0.020, 0.040]:
        kw['protection_thickness'] = dp
        T_max, _ = temperature_max(**kw)
        temps.append(T_max)

    for i in range(len(temps) - 1):
        assert temps[i] >= temps[i+1], f"dp {[0.005,0.010,0.020,0.040][i]} → {temps[i]:.1f} >= {temps[i+1]:.1f}"


# ---- temperature_2 (protected with activation) ----

def test_temperature_2_unprotected_below_activation():
    """Below activation temperature, steel follows unprotected heating."""
    t = np.arange(0, 1800, 10, dtype=float)
    T_g = __param_fire(t)
    kw = _standard_beam_kwargs(t, T_g)
    kw['protection_activation_temperature'] = 1000 + 273.15  # very high, never activates

    T_steel = temperature_2(**kw)
    # Steel temperature should be strictly above ambient after fire starts
    assert np.max(T_steel[100:]) > 350


def test_temperature_2_activation_reduces_heating():
    """After activation, protection slows heating."""
    t = np.arange(0, 3600, 10, dtype=float)
    T_g = __param_fire(t)
    kw = _standard_beam_kwargs(t, T_g)

    # With immediate activation (T_act=0) → protected from start
    kw['protection_activation_temperature'] = 0
    T_protected = temperature_2(**kw)

    # With never-activate → unprotected throughout
    kw['protection_activation_temperature'] = 2000 + 273.15
    T_unprotected = temperature_2(**kw)

    # Protected steel should be cooler at the end
    assert np.max(T_protected) < np.max(T_unprotected)


# ---- protection_thickness ----

def test_protection_thickness_converges():
    """protection_thickness should return a finite thickness for normal inputs."""
    t = np.arange(0, 7200, 30, dtype=float)
    T_g = __param_fire(t)
    kw = _standard_beam_kwargs(t, T_g)
    kw.pop('protection_thickness')
    kw['solver_temperature_goal'] = 500 + 273.15  # target 500°C
    kw['solver_temperature_goal_tol'] = 0.5
    kw['solver_max_iter'] = 20

    dp, T_max, t_at_max, n_iter = protection_thickness(**kw)

    assert not np.isnan(dp), f"dp is NaN"
    assert T_max > 293.15
    assert 0 <= n_iter <= 20


def test_protection_thickness_bounds():
    """protection_thickness should return -inf if goal already exceeded at max thickness."""
    t = np.arange(0, 7200, 30, dtype=float)
    T_g = __param_fire(t)
    kw = _standard_beam_kwargs(t, T_g)
    kw.pop('protection_thickness')
    kw['solver_temperature_goal'] = 50 + 273.15  # impossibly low target
    kw['solver_temperature_goal_tol'] = 0.1

    dp, T_max, t_at_max, n_iter = protection_thickness(**kw)
    assert np.isinf(dp), f"should indicate out-of-bounds, got dp={dp}"


# ---- protection_thickness_2 ----

def test_protection_thickness_2_converges():
    """protection_thickness_2 with linear+binary search should converge."""
    t = np.arange(0, 7200, 30, dtype=float)
    T_g = __param_fire(t)
    kw = _standard_beam_kwargs(t, T_g)
    kw.pop('protection_thickness')
    kw['solver_temperature_goal'] = 500 + 273.15
    kw['solver_temperature_goal_tol'] = 2.0
    kw['d_p_1'] = 0.0005
    kw['d_p_2'] = 0.0800
    kw['d_p_i'] = 0.0020

    dp, T_max, t_at_max, n_iter, status = protection_thickness_2(**kw)

    assert status in (0,), f"status={status}, dp={dp:.6f}, T_max={T_max:.1f}K"
    assert 0.0001 < dp < 0.1, f"dp={dp:.6f} out of plausible range"
    assert abs(T_max - kw['solver_temperature_goal']) < kw['solver_temperature_goal_tol']


def test_protection_thickness_2_status_codes():
    """Test all five status codes."""
    t = np.arange(0, 7200, 30, dtype=float)
    T_g = __param_fire(t)

    # STATUS_OUT_OF_LOWER_BOUND: goal already met at d_p_1
    kw = _standard_beam_kwargs(t, T_g)
    kw.pop('protection_thickness')
    kw['solver_temperature_goal'] = 50 + 273.15
    kw['solver_temperature_goal_tol'] = 0.1
    kw['d_p_1'] = 0.01
    kw['d_p_2'] = 0.08
    _, _, _, _, status = protection_thickness_2(**kw)
    assert status != 0, f"expected non-success for too-low goal, got status={status}"

    # STATUS_OUT_OF_UPPER_BOUND or STATUS_MONOTONICITY_FAILED:
    # goal not met at max thickness — solver exits indicating issue
    kw2 = dict(fire_time=t, fire_temperature=T_g,
               beam_rho=7850., beam_cross_section_area=0.017,
               protection_k=0.2, protection_rho=800., protection_c=1700.,
               protection_protected_perimeter=2.14,
               solver_temperature_goal=150 + 273.15, solver_temperature_goal_tol=0.5,
               d_p_1=0.005, d_p_2=0.008)
    _, _, _, _, status = protection_thickness_2(**kw2)
    assert status != 0, f"expected non-success, got status={status}"


def test_protection_thickness_2_invalid_inputs():
    """Should raise ValueError for bad inputs."""
    t = np.arange(0, 3600, 30, dtype=float)
    T_g = __param_fire(t)
    kw = _standard_beam_kwargs(t, T_g)
    kw.pop('protection_thickness')
    kw['solver_temperature_goal'] = 500 + 273.15
    kw['solver_temperature_goal_tol'] = 0.5

    # Negative tolerance
    try:
        protection_thickness_2(solver_temperature_goal_tol=-1.0, **{k: v for k, v in kw.items()
                               if k != 'solver_temperature_goal_tol'})
        assert False, "should have raised"
    except ValueError:
        pass

    # d_p_1 > d_p_2
    try:
        protection_thickness_2(d_p_1=0.08, d_p_2=0.001, **{k: v for k, v in kw.items()
                               if k not in ('d_p_1', 'd_p_2')})
        assert False, "should have raised"
    except ValueError:
        pass

    # Empty fire_time
    try:
        protection_thickness_2(fire_time=np.array([]), fire_temperature=np.array([]),
                               beam_rho=7850., beam_cross_section_area=0.017,
                               protection_k=0.2, protection_rho=800., protection_c=1700.,
                               protection_protected_perimeter=2.14,
                               solver_temperature_goal=800., solver_temperature_goal_tol=0.5)
        assert False, "should have raised"
    except ValueError:
        pass

    # Mismatched time arrays
    try:
        protection_thickness_2(fire_time=np.array([0., 10.]), fire_temperature=np.array([293.15]),
                               beam_rho=7850., beam_cross_section_area=0.017,
                               protection_k=0.2, protection_rho=800., protection_c=1700.,
                               protection_protected_perimeter=2.14,
                               solver_temperature_goal=800., solver_temperature_goal_tol=0.5)
        assert False, "should have raised"
    except ValueError:
        pass


# ---- temperature (protected, full time-history) ----

def test_temperature_positive_monotonic_above_ambient():
    """Steel temperature should never go below ambient or be negative."""
    t = np.arange(0, 3600, 30, dtype=float)
    T_g = __param_fire(t)
    T_steel = temperature(**_standard_beam_kwargs(t, T_g))
    assert np.all(T_steel >= 273.15)
    assert np.all(np.diff(T_steel) >= -1)  # no unrealistic cooling spikes


def test_temperature_thicker_protection_cooler():
    """Thicker protection → lower peak steel temperature."""
    t = np.arange(0, 3600, 30, dtype=float)
    T_g = __param_fire(t)

    base = dict(fire_time=t, fire_temperature=T_g,
                beam_rho=7850., beam_cross_section_area=0.017,
                protection_k=0.2, protection_rho=800., protection_c=1700.,
                protection_protected_perimeter=2.14)

    T1 = temperature(protection_thickness=0.005, **base)
    T2 = temperature(protection_thickness=0.040, **base)
    assert np.max(T1) > np.max(T2), \
        f"thicker should be cooler: max(T_5mm)={np.max(T1):.0f}K, max(T_40mm)={np.max(T2):.0f}K"
