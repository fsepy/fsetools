"""Tests for the generic linear solver."""

from ..etc.solver import linear_solver


def _quadratic(x, a=1.0, b=0.0, c=0.0):
    """f(x) = a*x² + b*x + c (for solver testing)."""
    return a * x ** 2 + b * x + c


def _linear(x, m=1.0, b=0.0):
    """f(x) = m*x + b."""
    return m * x + b


# ---------------------------------------------------------------------------
# Basic solving
# ---------------------------------------------------------------------------

def test_solve_linear_exact():
    """Solve f(x) = 2x + 1 = 5  →  x = 2."""
    result = linear_solver(
        func=_linear, func_kwargs=dict(m=2.0, b=1.0),
        x_name='x', y_target=5.0,
        x_upper=10.0, x_lower=0.0, y_tol=1e-9, iter_max=100,
    )
    assert result is not None
    assert abs(result - 2.0) < 1e-6


def test_solve_linear_with_multiplier():
    """With func_multiplier=-1, f(x)=10-x=3  →  x=7."""
    result = linear_solver(
        func=_linear, func_kwargs=dict(m=-1.0, b=10.0),
        x_name='x', y_target=3.0,
        x_upper=10.0, x_lower=0.0, y_tol=1e-9, iter_max=100,
        func_multiplier=-1,
    )
    assert result is not None
    assert abs(result - 7.0) < 1e-6


def test_solve_quadratic():
    """Solve f(x) = x² = 4  →  x = 2."""
    result = linear_solver(
        func=_quadratic, func_kwargs=dict(a=1.0),
        x_name='x', y_target=4.0,
        x_upper=10.0, x_lower=0.0, y_tol=1e-9, iter_max=100,
    )
    assert result is not None
    assert abs(result - 2.0) < 1e-6


# ---------------------------------------------------------------------------
# Boundary conditions
# ---------------------------------------------------------------------------

def test_target_below_lower():
    """When target is below f(x_lower), returns x_lower."""
    result = linear_solver(
        func=_linear, func_kwargs=dict(m=1.0, b=10.0),
        x_name='x', y_target=5.0,  # f(0)=10 > 5, so target=5 is below range
        x_upper=10.0, x_lower=0.0, y_tol=1e-9, iter_max=100,
    )
    assert result == 0.0  # x_lower


def test_target_above_upper():
    """When target is above f(x_upper), returns x_upper."""
    result = linear_solver(
        func=_linear, func_kwargs=dict(m=1.0, b=0.0),
        x_name='x', y_target=100.0,  # f(10)=10 < 100, target above range
        x_upper=10.0, x_lower=0.0, y_tol=1e-9, iter_max=100,
    )
    assert result == 10.0  # x_upper


# ---------------------------------------------------------------------------
# Max iterations
# ---------------------------------------------------------------------------

def test_max_iter_exceeded():
    """With too few iterations, returns None."""
    # Use a non-trivial function so binary search doesn't land on answer immediately
    result = linear_solver(
        func=_linear, func_kwargs=dict(m=1.0, b=1.0),
        x_name='x', y_target=6.3,  # f(5.3)=6.3, won't hit exactly with bisection
        x_upper=10.0, x_lower=0.0, y_tol=1e-15, iter_max=1,
    )
    assert result is None


# ---------------------------------------------------------------------------
# Swapped bounds
# ---------------------------------------------------------------------------

def test_swapped_bounds():
    """Solver should swap lower/upper if provided backwards."""
    result = linear_solver(
        func=_linear, func_kwargs=dict(m=1.0, b=0.0),
        x_name='x', y_target=5.0,
        x_upper=0.0, x_lower=10.0,  # swapped
        y_tol=1e-9, iter_max=100,
    )
    assert result is not None
    assert abs(result - 5.0) < 1e-6


# ---------------------------------------------------------------------------
# Dict copy (no side-effect on caller)
# ---------------------------------------------------------------------------

def test_no_side_effect_on_caller():
    """verify that the solver does not mutate the caller's kwargs dict."""
    kwargs = dict(m=2.0, b=1.0, x=None)
    original = kwargs.copy()
    linear_solver(
        func=_linear, func_kwargs=kwargs,
        x_name='x', y_target=5.0,
        x_upper=10.0, x_lower=0.0, y_tol=1e-9, iter_max=100,
    )
    # After solver returns, kwargs['x'] should be None (unchanged)
    assert kwargs['x'] is None
    assert kwargs == original
