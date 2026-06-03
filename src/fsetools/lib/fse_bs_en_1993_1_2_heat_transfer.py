# -*- coding: utf-8 -*-
import numpy as np


def c_steel_T(T):
    # BS EN 1993-1-2:2005, 3.4.1.2
    T -= 273.15
    if T < 20:
        return 425 + 0.773 * 20 - 1.69e-3 * 400 + 2.22e-6 * 8000
    if 20 <= T < 600:
        return 425 + 0.773 * T - 1.69e-3 * T ** 2 + 2.22e-6 * T ** 3
    elif 600 <= T < 735:
        return 666 + 13002 / (738 - T)
    elif 735 <= T < 900:
        return 545 + 17820 / (T - 731)
    elif 900 <= T <= 1200:
        return 650
    elif T > 1200:
        return 650


def temperature(
        fire_time,
        fire_temperature,
        beam_rho,
        beam_cross_section_area,
        protection_k,
        protection_rho,
        protection_c,
        protection_thickness,
        protection_protected_perimeter,
        *_,
        **__
):
    """
    SI UNITS!
    Function calculates the maximum steel temperature for a protected steel member based upon BS EN 1993-1-2.

    PARAMETERS:
    :param fire_time:                       Time array [s]
    :param T_g:                Gas temperature array [K]
    :param beam_rho:                        Steel beam density [kg/m3]
    :param beam_cross_section_area:         Steel beam cross sectional area [m2]
    :param protection_k:                    Protection thermal conductivity [K/kg/m]
    :param protection_rho:                  Protection density [kg/m3]
    :param protection_c:                    Protection specific heat capacity [J/K/kg]
    :param protection_thickness:            Protection layer thickness [m]
    :param protection_protected_perimeter:  Protection protected perimeter (of the steel beam section) [m]
    :return:                                Steel beam temperature array [K]
    """

    # todo: 4.2.5.2 (2) - thermal properties for the insulation material
    # todo: revise BS EN 1993-1-2:2005, Clauses 4.2.5.2

    T_g = fire_temperature
    V = beam_cross_section_area
    rho_a = beam_rho
    lambda_p = protection_k
    rho_p = protection_rho
    d_p = protection_thickness
    A_p = protection_protected_perimeter
    c_p = protection_c

    T_a = np.zeros_like(fire_time, dtype=np.float32)
    dT_a = np.zeros_like(fire_time, dtype=np.float32)
    c_a = np.zeros_like(fire_time, dtype=np.float32)

    # Check time step <= 30 seconds. [BS EN 1993-1-2:2005, Clauses 4.2.5.2 (3)]

    # the following parameters are used for debug purposes
    is_debug = False
    if is_debug:
        phi_, a_, b_, c_, d_ = [np.zeros_like(fire_time, dtype=np.float16) for i in range(5)]

    T_a[0] = T_g[0]  # initially, steel temperature is equal to ambient
    for i in range(1, len(fire_time)):
        c_a[i] = c_steel_T(T_a[i - 1])

        # Steel temperature equations are from [BS EN 1993-1-2:2005, Clauses 4.2.5.2, Eq. 4.27]
        # This a ratio of heat stored in the protection
        phi = (c_p * rho_p / c_a[i] / rho_a) * d_p * A_p / V

        a = (lambda_p * A_p / V) / (d_p * c_a[i] * rho_a)
        b = (T_g[i] - T_a[i - 1]) / (1.0 + phi / 3.)
        c = (2.718 ** (phi / 10.0) - 1.0) * (T_g[i] - T_g[i - 1])
        d = fire_time[i] - fire_time[i - 1]

        if is_debug:
            phi_[i] = phi
            a_[i] = a
            b_[i] = b
            c_[i] = c
            d_[i] = d

        dT_a[i] = (a * b * d - c) / d  # deviated from e4.27, converted to rate [s-1]
        if dT_a[i] < 0 < (T_g[i] - T_g[i - 1]):
            dT_a[i] = 0

        T_a[i] = T_a[i - 1] + dT_a[i] * d

        # NOTE: Steel temperature can be in cooling phase at the beginning of calculation, even the ambient temperature
        #       (fire) is hot. This is
        #       due to the factor 'phi' which intends to address the energy locked within the protection layer.
        #       The steel temperature is forced to be increased or remain as previous when ambient temperature and
        #       its previous temperature are all higher than the current calculated temperature.
        #       A better implementation is perhaps to use a 1-D heat transfer model.

    if is_debug:
        try:
            import pandas as pd
            data = pd.DataFrame.from_dict(dict(
                T_g=T_g,
                T_a=T_a,
                dT_a=dT_a,
                phi=phi_,
                a=a_,
                b=b_,
                c=c_,
                d=d_,
                c_a=c_a
            ))
        except:
            data = None

    return T_a


def temperature_max(
        fire_time,
        fire_temperature,
        beam_rho,
        beam_cross_section_area,
        protection_k,
        protection_rho,
        protection_c,
        protection_thickness,
        protection_protected_perimeter,
):
    """
    SI UNITS!
    Function calculates the maximum steel temperature for a protected steel member based upon BS EN 1993-1-2.

    LIMITATIONS:
        1. Constant time interval in `fire_time` throughout;
        2. `fire_temperature` has *one* maxima.

    PARAMETERS:
    :param fire_time:                       Time array [s]
    :param fire_temperature:                Gas temperature array [K]
    :param beam_rho:                        Steel beam density [kg/m3]
    :param beam_cross_section_area:         Steel beam cross sectional area [m2]
    :param protection_k:                    Protection thermal conductivity [K/kg/m]
    :param protection_rho:                  Protection density [kg/m3]
    :param protection_c:                    Protection specific heat capacity [J/K/kg]
    :param protection_thickness:            Protection layer thickness [m]
    :param protection_protected_perimeter:  Protection protected perimeter (of the steel beam section) [m]
    :return:                                (max_steel_temperature [K], time_at_max [s])
    """

    # todo: 4.2.5.2 (2) - thermal properties for the insulation material
    # todo: revise BS EN 1993-1-2:2005, Clauses 4.2.5.2

    V = beam_cross_section_area
    rho_a = beam_rho
    lambda_p = protection_k
    rho_p = protection_rho
    d_p = protection_thickness
    A_p = protection_protected_perimeter
    c_p = protection_c

    T = fire_temperature[0]  # current steel temperature
    d = fire_time[1] - fire_time[0]
    i = 0  # track index for time-at-max

    for i in range(1, len(fire_temperature)):

        T_g = fire_temperature[i]

        c_s = c_steel_T(T)

        # Steel temperature equations are from [BS EN 1993-1-2:2005, Clauses 4.2.5.2, Eq. 4.27]
        phi = (c_p * rho_p / c_s / rho_a) * d_p * A_p / V

        a = (lambda_p * A_p / V) / (d_p * c_s * rho_a)
        b = (T_g - T) / (1.0 + phi / 3.0)
        c = (2.718 ** (phi / 10.0) - 1.0) * (T_g - fire_temperature[i - 1])

        dT = (a * b * d - c) / d  # deviated from e4.27, converted to rate [s-1]
        if dT < 0 < (T_g - fire_temperature[i - 1]):
            dT = 0

        T = T + dT * d

        # Terminate early if maximum temperature is reached
        if dT < 0:
            T -= dT * d
            break

    return T, fire_time[i - 1]


def temperature_2(
        fire_time,
        fire_temperature,
        beam_rho,
        beam_cross_section_area,
        protection_k,
        protection_rho,
        protection_c,
        protection_thickness,
        protection_protected_perimeter,
        protection_activation_temperature=0,
        shadow_factor=1.,
        emissivity_factor=0.7,
        conductivity_factor=25.,
):
    """
    SI UNITS!
    Function calculates the steel temperature for a protected steel member based upon BS EN 1993-1-2.

    Extended version with protection activation temperature:
    - Below activation temperature: unprotected steel heating (eq 4.25).
    - Above activation temperature: protected steel heating (eq 4.27).

    :param fire_time:                           Time array [s]
    :param fire_temperature:                    Gas temperature array [K]
    :param beam_rho:                            Steel beam density [kg/m3]
    :param beam_cross_section_area:             Steel beam cross sectional area [m2]
    :param protection_k:                        Protection thermal conductivity [K/kg/m]
    :param protection_rho:                      Protection density [kg/m3]
    :param protection_c:                        Protection specific heat capacity [J/K/kg]
    :param protection_thickness:                Protection layer thickness [m]
    :param protection_protected_perimeter:      Protection protected perimeter (of the steel beam section) [m]
    :param protection_activation_temperature:   Temperature at which protection activates [K]
    :param shadow_factor:                       Shadow factor (k_sh) [-]
    :param emissivity_factor:                   Emissivity of the member surface [-]
    :param conductivity_factor:                 Convective heat transfer coefficient [W/m2/K]
    :return:                                    Steel beam temperature array [K]
    """

    # todo: 4.2.5.2 (2) - thermal properties for the insulation material
    # todo: revise BS EN 1993-1-2:2005, Clauses 4.2.5.2

    V = beam_cross_section_area
    rho_a = beam_rho
    lambda_p = protection_k
    rho_p = protection_rho
    d_p = protection_thickness
    A_p = protection_protected_perimeter
    c_p = protection_c
    T_act = protection_activation_temperature
    k_sh = shadow_factor
    e_m = emissivity_factor
    a_c = conductivity_factor  # alpha_c

    epsilon_f = 1.0  # Section 4.2.5.1 (3)
    Phi = 1.0  # Assumed, should be 1.0 within a fire compartment

    T_a = np.zeros_like(fire_time, dtype=np.float64)

    # Check time step <= 30 seconds. [BS EN 1993-1-2:2005, Clauses 4.2.5.2 (3)]

    T_a[0] = fire_temperature[0]  # assign steel initial temperature

    t_act = -1.
    if T_act == 0.:
        t_act = 0.

    for i in range(1, len(fire_time)):
        T_g = fire_temperature[i]

        if t_act < 0 and T_a[i - 1] > T_a[0] and T_a[i - 1] > T_act:
            t_act = fire_time[i]

        if t_act >= 0:
            # if above protection activation temperature, use protected correlation
            c_s = c_steel_T(T_a[i - 1])

            # Steel temperature equations are from [BS EN 1993-1-2:2005, Clauses 4.2.5.2, Eq. 4.27]
            phi = (c_p * rho_p / c_s / rho_a) * d_p * A_p / V

            a = (lambda_p * A_p / V) / (d_p * c_s * rho_a)
            b = (T_g - T_a[i - 1]) / (1.0 + phi / 3.0)
            c = (2.718 ** (phi / 10.0) - 1.0) * (T_g - fire_temperature[i - 1])
            dt = fire_time[i] - fire_time[i - 1]

            dT = (a * b * dt - c) / dt  # deviated from e4.27, converted to rate [s-1]
            if dT < 0 < (T_g - fire_temperature[i - 1]):
                dT = 0
        else:
            h_net_c = a_c * (T_g - T_a[i - 1])
            h_net_r = Phi * e_m * epsilon_f * 56.7e-9 * (T_g ** 4 - T_a[i - 1] ** 4)
            h_net_d = h_net_c + h_net_r

            # BS EN 1993-1-2:2005 (e4.25)
            const = (A_p / V) / rho_a / c_steel_T(T_a[i - 1])
            dt = fire_time[i] - fire_time[i - 1]
            dT = k_sh * const * h_net_d

        T_a[i] = T_a[i - 1] + dT * dt

        # NOTE: Steel temperature can be in cooling phase at the beginning of calculation, even the ambient temperature
        #       (fire) is hot. This is
        #       due to the factor 'phi' which intends to address the energy locked within the protection layer.
        #       The steel temperature is forced to be increased or remain as previous when ambient temperature and
        #       its previous temperature are all higher than the current calculated temperature.
        #       A better implementation is perhaps to use a 1-D heat transfer model.

    return T_a


def protection_thickness(
        *,
        fire_time,
        fire_temperature,
        beam_rho,
        beam_cross_section_area,
        protection_k,
        protection_rho,
        protection_c,
        protection_protected_perimeter,
        solver_temperature_goal,
        solver_temperature_goal_tol,
        solver_max_iter=20,
        d_p_1=0.0001,
        d_p_2=0.0300,
):
    """
    SI UNITS!
    To solve the protection thickness for the max. steel temperature, `T_a_max`, is within a predefined range:

        - `T_a_max_goal ± T_a_max_goal_tol`;
        - `T_a_max` is the max. steel temperature;
        - `T_a_max_goal` is a given max. steel temperature goal;
        - `T_a_max_goal_tol` is solver tolerance.

    The steel max. temperature is solved based upon BS EN 1993-1-2 for the given `fire_time` and `fire_temperature`.

    LIMITATIONS:
        1. Constant time interval in `fire_time` throughout;
        2. `fire_temperature` has *one* maxima.

    PARAMETERS:
    :param fire_time:                       Time array [s]
    :param fire_temperature:                Gas temperature array [K]
    :param beam_rho:                        Steel beam density [kg/m3]
    :param beam_cross_section_area:         Steel beam cross-sectional area [m2]
    :param protection_k:                    Protection thermal conductivity [K/kg/m]
    :param protection_rho:                  Protection density [kg/m3]
    :param protection_c:                    Protection specific heat capacity [J/K/kg]
    :param protection_protected_perimeter:  Protection protected perimeter (of the steel beam section) [m]
    :param solver_temperature_goal:         The max. steel temperature to be solved for [K]
    :param solver_temperature_goal_tol:     Tolerance of the max. steel temperature to be solved for [K]
    :param d_p_1:                           Protection thickness lower bound [m]
    :param d_p_2:                           Protection thickness upper bound [m]
    :return:                                (d_p, T_a_max, t, solver_iter_count)
                                            `d_p`               is the solved protection thickness [m]
                                            `T_a_max`           is the solved maximum steel temperature [K]
                                            `t`                 is the time when maximum steel temperature occurred [s]
                                            `solver_iter_count` is the solver iteration count
    """

    # todo: 4.2.5.2 (2) - thermal properties for the insulation material
    # todo: revise BS EN 1993-1-2:2005, Clauses 4.2.5.2

    V = beam_cross_section_area
    rho_a = beam_rho
    lambda_p = protection_k
    rho_p = protection_rho
    A_p = protection_protected_perimeter
    c_p = protection_c

    d = fire_time[1] - fire_time[0]

    # Ensure d_p_1 < d_p_2 (swap if needed)
    if d_p_1 > d_p_2:
        d_p_1, d_p_2 = d_p_2, d_p_1

    solver_iter_count = 0

    # -------------------------------
    # Solve maximum steel temperature
    # -------------------------------

    T_a_max_1, t = temperature_max(
        fire_time=fire_time,
        fire_temperature=fire_temperature,
        beam_rho=beam_rho,
        beam_cross_section_area=beam_cross_section_area,
        protection_k=protection_k,
        protection_rho=protection_rho,
        protection_c=protection_c,
        protection_thickness=d_p_1,
        protection_protected_perimeter=protection_protected_perimeter,
    )

    T_a_max_2, t = temperature_max(
        fire_time=fire_time,
        fire_temperature=fire_temperature,
        beam_rho=beam_rho,
        beam_cross_section_area=beam_cross_section_area,
        protection_k=protection_k,
        protection_rho=protection_rho,
        protection_c=protection_c,
        protection_thickness=d_p_2,
        protection_protected_perimeter=protection_protected_perimeter,
    )

    if T_a_max_1 < solver_temperature_goal + solver_temperature_goal_tol:
        return -np.inf, T_a_max_1, t, solver_iter_count
    if T_a_max_2 > solver_temperature_goal - solver_temperature_goal_tol:
        return np.inf, T_a_max_2, t, solver_iter_count

    d_p = (d_p_1 + d_p_2) / 2 + ((np.random.rand() - 0.5) * abs(d_p_1 - d_p_2) * 0.1)  # initial

    while True:
        T, t = temperature_max(
            fire_time=fire_time,
            fire_temperature=fire_temperature,
            beam_rho=beam_rho,
            beam_cross_section_area=beam_cross_section_area,
            protection_k=protection_k,
            protection_rho=protection_rho,
            protection_c=protection_c,
            protection_thickness=d_p,
            protection_protected_perimeter=protection_protected_perimeter,
        )

        # ---------------------------
        # Adjust protection thickness
        # ---------------------------

        if solver_iter_count <= solver_max_iter:
            if T <= solver_temperature_goal - solver_temperature_goal_tol:
                # steel temperature is too low, decrease thickness
                d_p_2 = d_p
            elif T >= solver_temperature_goal + solver_temperature_goal_tol:
                # steel temperature is too high, increase thickness
                d_p_1 = d_p
            else:
                return d_p, T, t, solver_iter_count

            d_p = (d_p_1 + d_p_2) / 2
        else:
            return np.nan, np.nan, np.nan, np.nan

        solver_iter_count += 1


def protection_thickness_2(
        fire_time,
        fire_temperature,
        beam_rho,
        beam_cross_section_area,
        protection_k,
        protection_rho,
        protection_c,
        protection_protected_perimeter,
        solver_temperature_goal,
        solver_temperature_goal_tol,
        solver_max_iter=100,
        d_p_1=0.0001,
        d_p_2=0.0900,
        d_p_i=0.0010,
):
    """
    SI UNITS! Finds protection thickness `d_p` so max steel temp `T_a_max` is near `solver_temperature_goal`.

    Assumes `T_a_max` monotonically decreases as `d_p` increases. If this behaviour
    is violated during the search, the function returns with STATUS_MONOTONICITY_FAILED.
    Uses linear step search from `d_p_1` then binary search to refine.

    Algorithm:
    1. Check T(d_p_1). Handle if already below or within goal tolerance.
    2. Linearly increase `d_p` by `d_p_i`.
    3. **In each step, verify T_current <= T_previous. If not, return failure.**
    4. Check if T_current falls within or below the goal range to trigger binary search.
    5. Perform binary search within the identified bracket [d_p_previous, d_p_current].

    LIMITATIONS:
        1. Constant time interval in `fire_time` throughout.
        2. `fire_temperature` has *one* maxima.
        3. **Requires** `T_a_max` from `temperature_max` to be MONOTONIC DECREASING with `protection_thickness`.

    PARAMETERS:
    :param fire_time:                       Time array [s]
    :param fire_temperature:                Gas temperature array [K]
    :param beam_rho:                        Steel beam density [kg/m3]
    :param beam_cross_section_area:         Steel beam cross sectional area [m2]
    :param protection_k:                    Protection thermal conductivity [W/m/K]
    :param protection_rho:                  Protection density [kg/m3]
    :param protection_c:                    Protection specific heat capacity [J/kg/K]
    :param protection_protected_perimeter:  Protection protected perimeter (of steel section) [m]
    :param solver_temperature_goal:         Target max steel temperature [K]
    :param solver_temperature_goal_tol:     Tolerance for target max steel temperature [K]
    :param solver_max_iter:                 Maximum total calls to `temperature_max`
    :param d_p_1:                           Protection thickness lower bound [m]
    :param d_p_2:                           Protection thickness upper bound [m]
    :param d_p_i:                           Step size for initial linear search [m]

    :return: tuple (d_p, T_a_max, t_at_max, iter_count, status)
        `d_p`           solved protection thickness [m] (or last valid if monotonicity failed)
        `T_a_max`       max steel temperature [K] (or last valid if monotonicity failed)
        `t_at_max`      time of max steel temperature [s] (or last valid if monotonicity failed)
        `iter_count`    total calls to `temperature_max`
        `status`        solver status code:
                        0: Success
                        1: Out of Lower Bound (temp at d_p_1 already too low)
                        2: Out of Upper Bound (temp at d_p_2 still too high)
                        3: Max Iterations Reached (returned value is best found)
                        4: Monotonicity Failed (T_max increased unexpectedly with increased d_p)
    """
    # Status constants
    STATUS_SUCCESS = 0
    STATUS_OUT_OF_LOWER_BOUND = 1
    STATUS_OUT_OF_UPPER_BOUND = 2
    STATUS_MAX_ITERATIONS_REACHED = 3
    STATUS_MONOTONICITY_FAILED = 4

    # Input validation (basic)
    if d_p_1 < 0 or d_p_2 <= d_p_1 or d_p_i <= 0:
        raise ValueError("Invalid bounds or step size (d_p_1 >= 0, d_p_2 > d_p_1, d_p_i > 0 required)")
    if solver_temperature_goal_tol <= 0:
        raise ValueError("Solver tolerance must be positive")
    if solver_max_iter < 2:
        raise ValueError("Solver max iterations must be at least 2")
    if len(fire_time) == 0 or len(fire_time) != len(fire_temperature):
        raise ValueError("fire_time and fire_temperature must be non-empty and have the same length")

    # Result tracking variables (initialize with values from d_p_1)
    best_d_p = d_p_1
    best_T = 0.0  # Will be overwritten by first call
    best_t = 0.0  # Will be overwritten by first call
    min_abs_diff_found = 1e18  # Initialize with a large value
    total_iter_count = 0

    # Sentinel values
    d_p_low = -1.0
    d_p_high = -1.0

    # Common parameters dict for temperature_max call
    common_params = dict(
        fire_time=fire_time,
        fire_temperature=fire_temperature,
        beam_rho=beam_rho,
        beam_cross_section_area=beam_cross_section_area,
        protection_k=protection_k,
        protection_rho=protection_rho,
        protection_c=protection_c,
        protection_protected_perimeter=protection_protected_perimeter,
    )

    # --- Initial Check at Lower Bound (d_p_1) ---
    T_current, t_current = temperature_max(protection_thickness=d_p_1, **common_params)
    total_iter_count += 1

    # Initialise best solution tracking using the first result
    min_abs_diff_found = abs(T_current - solver_temperature_goal)
    best_d_p = d_p_1
    best_T = T_current
    best_t = t_current

    # Check if T(d_p_1) is already too low (below target - tolerance)
    if T_current < solver_temperature_goal - solver_temperature_goal_tol:
        return best_d_p, best_T, best_t, total_iter_count, STATUS_OUT_OF_LOWER_BOUND

    # Check if T(d_p_1) is within tolerance
    if T_current <= solver_temperature_goal + solver_temperature_goal_tol:
        return best_d_p, best_T, best_t, total_iter_count, STATUS_SUCCESS

    # --- Linear Step Search (from d_p_1 + d_p_i up to d_p_2) ---
    d_p_previous = d_p_1
    T_previous = T_current
    t_previous = t_current

    while True:
        # Check iteration count before potentially expensive calculation
        if total_iter_count >= solver_max_iter:
            return best_d_p, best_T, best_t, total_iter_count, STATUS_MAX_ITERATIONS_REACHED

        # Calculate next d_p, clamped to d_p_2
        d_p_current = d_p_previous + d_p_i
        if d_p_current >= d_p_2:
            d_p_current = d_p_2

        # Avoid infinite loop if stuck at d_p_2
        if d_p_current == d_p_previous:
            break

        # Solve T for current d_p
        T_current, t_current = temperature_max(protection_thickness=d_p_current, **common_params)
        total_iter_count += 1

        # --- Monotonicity Check ---
        if T_current > T_previous:
            # Temperature increased unexpectedly! Violates assumption.
            return d_p_previous, T_previous, t_previous, total_iter_count, STATUS_MONOTONICITY_FAILED

        # Update best solution found so far (closest to goal)
        current_diff = abs(T_current - solver_temperature_goal)
        if current_diff < min_abs_diff_found:
            min_abs_diff_found = current_diff
            best_d_p = d_p_current
            best_T = T_current
            best_t = t_current

        # Check if T_current is now low enough to bracket the solution or hit target
        if T_current <= solver_temperature_goal + solver_temperature_goal_tol:
            # Temperature is now potentially in range or below the target range.
            d_p_low = d_p_previous
            d_p_high = d_p_current
            break

        # Prepare for next iteration of linear search
        d_p_previous = d_p_current
        T_previous = T_current
        t_previous = t_current

    # --- Post Linear Search ---

    # Case 1: Did we exit because d_p reached d_p_2?
    if d_p_current == d_p_2 and d_p_low < 0:
        if T_current > solver_temperature_goal + solver_temperature_goal_tol:
            # Even at max thickness d_p_2, the temperature is still too high
            return best_d_p, best_T, best_t, total_iter_count, STATUS_OUT_OF_UPPER_BOUND
        else:
            # T(d_p_2) is acceptable, bracket exists: [d_p_previous, d_p_2]
            d_p_low = d_p_previous
            d_p_high = d_p_current

    # Case 2: We exited because a bracket [d_p_low, d_p_high] was found
    if d_p_low >= 0 and d_p_low < d_p_high:
        # --- Binary Search Refinement ---
        for _ in range(total_iter_count, solver_max_iter):
            d_p_mid = d_p_low + 0.5 * (d_p_high - d_p_low)

            # Check if interval is already tiny
            if (d_p_high - d_p_low) < 1e-12:
                T_mid, t_mid = temperature_max(protection_thickness=d_p_mid, **common_params)
                total_iter_count += 1
                mid_diff = abs(T_mid - solver_temperature_goal)
                if mid_diff < min_abs_diff_found:
                    return d_p_mid, T_mid, t_mid, total_iter_count, STATUS_SUCCESS
                else:
                    return best_d_p, best_T, best_t, total_iter_count, STATUS_SUCCESS

            # Evaluate temperature at midpoint
            T_current, t_current = temperature_max(protection_thickness=d_p_mid, **common_params)
            total_iter_count += 1

            # Update best solution tracking during binary search
            current_diff = abs(T_current - solver_temperature_goal)
            if current_diff < min_abs_diff_found:
                min_abs_diff_found = current_diff
                best_d_p = d_p_mid
                best_T = T_current
                best_t = t_current

            # Check if solution is within tolerance
            if (T_current <= solver_temperature_goal + solver_temperature_goal_tol and
                    T_current >= solver_temperature_goal - solver_temperature_goal_tol):
                return d_p_mid, T_current, t_current, total_iter_count, STATUS_SUCCESS

            # Update binary search bounds based on midpoint temperature
            if T_current > solver_temperature_goal:
                # Temp too high, need thicker protection -> increase lower bound
                d_p_low = d_p_mid
            else:
                # Temp too low, need thinner protection -> decrease upper bound
                d_p_high = d_p_mid

            # Check iteration count inside binary search loop
            if total_iter_count >= solver_max_iter:
                return best_d_p, best_T, best_t, total_iter_count, STATUS_MAX_ITERATIONS_REACHED

        # If binary search loop finishes without converging
        return best_d_p, best_T, best_t, total_iter_count, STATUS_MAX_ITERATIONS_REACHED

    # --- Fallback / Unexpected Exit ---
    final_status = STATUS_MAX_ITERATIONS_REACHED
    if d_p_current == d_p_2 and best_T > solver_temperature_goal + solver_temperature_goal_tol:
        final_status = STATUS_OUT_OF_UPPER_BOUND
    elif abs(best_T - solver_temperature_goal) <= solver_temperature_goal_tol:
        final_status = STATUS_SUCCESS

    return best_d_p, best_T, best_t, total_iter_count, final_status
