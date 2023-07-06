from typing import Callable


def linear_solver(
        func: Callable,
        func_kwargs: dict,
        x_name: str,
        y_target: float,
        x_upper: float,
        x_lower: float,
        y_tol: float,
        iter_max: int = 1000,
        func_multiplier: float = 1
):
    """Solver of single-root function (single variable), i.e. f(x)=a x + b

    :param func:            The function to be solved.
    :param func_kwargs:     Additional parameters of the function.
    :param x_name:          The variable (name) to be solved for.
    :param y_target:        The target to be solved for, i.e. solve for `f(x)==y_target`.
    :param x_upper:         The upper limit of the variable.
    :param x_lower:         The lower limit of the variable.
    :param y_tol:           Solver tolerance, i.e. actually solve for `abs(f(x)-y_target)<y_tal`.
    :param iter_max:        Maximum iteration of the solver.
    :param func_multiplier: 1 if f(x) is proportional to x, -1 if f(x) is inversely proportional to x.
    :return:                The solved value, i.e. x_solved when following is true `abs(f(x_solved)-y_target)<y_tal`.

    """
    if x_lower > x_upper:
        x_lower += x_upper
        x_upper = x_lower - x_upper
        x_lower = x_lower - x_upper

    y_target *= func_multiplier

    x1 = x_lower
    x2 = (x_lower + x_upper) / 2
    x3 = x_upper

    func_kwargs[x_name] = x1
    y1 = func_multiplier * func(**func_kwargs)
    func_kwargs[x_name] = x2
    y2 = func_multiplier * func(**func_kwargs)
    func_kwargs[x_name] = x3
    y3 = func_multiplier * func(**func_kwargs)

    if y_target < y1:
        return x1
    if y_target > y3:
        return x3

    iter_count = 0
    while True:
        if abs(y2 - y_target) < y_tol:
            return x2
        elif iter_max < iter_count:
            return None
        elif y2 < y_target:
            x1 = x2
        elif y2 > y_target:
            x3 = x2
        x2 = (x1 + x3) / 2
        func_kwargs[x_name] = x2
        y2 = func_multiplier * func(**func_kwargs)
        iter_count += 1

    raise ValueError("this shouldn't be possible, should always terminate within the while loop above")
