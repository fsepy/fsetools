# filename: protection_solver.pyx
# To compile (requires Cython and a C compiler):
# 1. Create a setup.py file:
#    from setuptools import setup
#    from Cython.Build import cythonize
#    import numpy
#
#    setup(
#        ext_modules=cythonize("protection_solver.pyx"),
#        include_dirs=[numpy.get_include()] # If using numpy C-API extensively
#    )
# 2. Run in terminal: python setup.py build_ext --inplace

# Cython compiler directives
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# distutils: language=3

import numpy as np
cimport numpy as np # Import C-API if needed, ensures efficient buffer access

# Import C standard library functions directly
from libc.math cimport fabs


cdef double c_steel_T(double T):

    T = T - 273.15
    if T < 20:
        # warnings.warn('Temperature ({:.1f} °C) is below 20 °C'.format(temperature))
        return 425 + 0.773 * 20 - 1.69e-3 * 400 + 2.22e-6 * 8000
    if 20 <= T < 600:
        return 425 + 0.773 * T - 1.69e-3 * (T ** 2) + 2.22e-6 * (T ** 3)
    elif 600 <= T < 735:
        return 666 + 13002 / (738 - T)
    elif 735 <= T < 900:
        return 545 + 17820 / (T - 731)
    elif 900 <= T <= 1200:
        return 650
    elif T > 1200:
        return 650
    else:
        return 0


def temperature(
        fire_time,
        double[:] fire_temperature,
        double beam_rho,
        double beam_cross_section_area,
        double protection_k,
        double protection_rho,
        double protection_c,
        double protection_thickness,
        double protection_protected_perimeter,
        **__
):
    """
    SI UNITS!
    Function calculates the steel temperature for a protected steel member based upon BS EN 1993-1-2.

    :param fire_time:                       Time array [s]
    :param fire_temperature:                Gas temperature array [K]
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

    # BS EN 1993-1-2:2005, 3.4.1.2

    cdef double V = beam_cross_section_area
    cdef double rho_a = beam_rho
    cdef double lambda_p = protection_k
    cdef double rho_p = protection_rho
    cdef double d_p = protection_thickness
    cdef double A_p = protection_protected_perimeter
    cdef double c_p = protection_c

    cdef double[:] T_a = fire_time * 0.0

    # Check time step <= 30 seconds. [BS EN 1993-1-2:2005, Clauses 4.2.5.2 (3)]

    T_a[0] = fire_temperature[0]  # assign steel initial temperature
    cdef int i
    cdef double a, b, c, d, phi, c_s, T_g, dT
    for i in range(1, len(fire_time)):
        T_g = fire_temperature[i]

        c_s = c_steel_T(T_a[i - 1])

        # Steel temperature equations are from [BS EN 1993-1-2:2005, Clauses 4.2.5.2, Eq. 4.27]
        phi = (c_p * rho_p / c_s / rho_a) * d_p * A_p / V

        a = (lambda_p * A_p / V) / (d_p * c_s * rho_a)
        b = (T_g - T_a[i - 1]) / (1.0 + phi / 3.0)
        c = (2.718 ** (phi / 10.0) - 1.0) * (T_g - fire_temperature[i - 1])
        d = fire_time[i] - fire_time[i - 1]

        dT = (a * b * d - c) / d  # deviated from e4.27, converted to rate [s-1]
        if dT < 0 < (T_g - fire_temperature[i - 1]):
            dT = 0

        T_a[i] = T_a[i - 1] + dT * d

        # NOTE: Steel temperature can be in cooling phase at the beginning of calculation, even the ambient temperature
        #       (fire) is hot. This is
        #       due to the factor 'phi' which intends to address the energy locked within the protection layer.
        #       The steel temperature is forced to be increased or remain as previous when ambient temperature and
        #       its previous temperature are all higher than the current calculated temperature.
        #       A better implementation is perhaps to use a 1-D heat transfer model.

    return np.array(T_a)


def temperature_2(
        fire_time,
        double[:] fire_temperature,
        double beam_rho,
        double beam_cross_section_area,
        double protection_k,
        double protection_rho,
        double protection_c,
        double protection_thickness,
        double protection_protected_perimeter,
        double protection_activation_temperature = 0,
        double shadow_factor = 1.,
        double emissivity_factor = 0.7,
        double conductivity_factor = 25.,
):
    """
    SI UNITS!
    Function calculates the steel temperature for a protected steel member based upon BS EN 1993-1-2.

    :param fire_time:                       Time array [s]
    :param fire_temperature:                Gas temperature array [K]
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

    # BS EN 1993-1-2:2005, 3.4.1.2

    cdef double V = beam_cross_section_area
    cdef double rho_a = beam_rho
    cdef double lambda_p = protection_k
    cdef double rho_p = protection_rho
    cdef double d_p = protection_thickness
    cdef double A_p = protection_protected_perimeter
    cdef double c_p = protection_c
    cdef double T_act = protection_activation_temperature
    cdef double k_sh = shadow_factor
    cdef double e_m = emissivity_factor
    cdef double a_c = conductivity_factor  # alpha_c

    cdef double epsilon_f = 1.0  # Section 4.2.5.1 (3)
    cdef double Phi = 1.0  # Assumed, should be 1.0 within a fire compartment

    cdef double[:] T_a = fire_time * 0.0

    # Check time step <= 30 seconds. [BS EN 1993-1-2:2005, Clauses 4.2.5.2 (3)]

    T_a[0] = fire_temperature[0]  # assign steel initial temperature
    cdef int i
    cdef double a, b, c, dt, phi, c_s, T_g, dT, h_net_c, h_net_r, h_net_d,const
    cdef double t_act = -1.

    if T_act == 0.:
        t_act = 0.

    for i in range(1, len(fire_time)):
        T_g = fire_temperature[i]

        if t_act < 0 and T_a[i-1] > T_a[0] and T_a[i-1] > T_act:
            t_act = fire_time[i]

        if t_act>=0:
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

    return np.array(T_a)


cpdef tuple temperature_max(
        double[:] fire_time,
        double[:] fire_temperature,
        double beam_rho,
        double beam_cross_section_area,
        double protection_k,
        double protection_rho,
        double protection_c,
        double protection_thickness,
        double protection_protected_perimeter,
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
    :return:                                Steel beam temperature array [K]
    """

    # todo: 4.2.5.2 (2) - thermal properties for the insulation material
    # todo: revise BS EN 1993-1-2:2005, Clauses 4.2.5.2

    cdef double V = beam_cross_section_area
    cdef double rho_a = beam_rho
    cdef double lambda_p = protection_k
    cdef double rho_p = protection_rho
    cdef double d_p = protection_thickness
    cdef double A_p = protection_protected_perimeter
    cdef double c_p = protection_c

    cdef double T = fire_temperature[0]  # current steel temperature
    cdef double d = fire_time[1] - fire_time[0]

    cdef int i
    cdef double T_g, c_s, phi, a, b, c, dT
    for i in range(1, len(fire_temperature)):

        T_g = fire_temperature[i]

        c_s = c_steel_T(T)

        # Steel temperature equations are from [BS EN 1993-1-2:2005, Clauses 4.2.5.2, Eq. 4.27]
        # If below get divide by zero error, it's very likely due to T = nan and causing c_s = 0
        phi = (c_p * rho_p / c_s / rho_a) * d_p * A_p / V

        a = (lambda_p * A_p / V) / (d_p * c_s * rho_a)
        b = (T_g - T) / (1.0 + phi / 3.0)
        c = (2.718 ** (phi / 10.0) - 1.0) * (T_g - fire_temperature[i - 1])

        dT = (a * b * d - c) / d  # deviated from e4.27, converted to rate [s-1]
        if dT < 0 < (T_g - fire_temperature[i - 1]):
            dT = 0

        T = T + dT * d

        if dT < 0:
            break

    return T, fire_time[i-1]


def protection_thickness(
        *,
        double[:] fire_time,
        double[:] fire_temperature,
        double beam_rho,
        double beam_cross_section_area,
        double protection_k,
        double protection_rho,
        double protection_c,
        double protection_protected_perimeter,
        double solver_temperature_goal,
        double solver_temperature_goal_tol,
        int solver_max_iter = 20,
        double d_p_1 = 0.0001,
        double d_p_2 = 0.0300,
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
    :param d_p_1:                           Protection thickness upper bound [m]
    :param d_p_2:                           Protection thickness lower bound [m]
    :return:                                (d_p, T_a_max, t, solver_iter_count)
                                            `d_p`               is the solved protection thickness [m]
                                            `T_a_max`           is the solved maximum steel temperature [K]
                                            `t`                 is the time when maximum steel temperature occurred [s]
                                            `solver_iter_count` is the solver iteration count

    """

    # todo: 4.2.5.2 (2) - thermal properties for the insulation material
    # todo: revise BS EN 1993-1-2:2005, Clauses 4.2.5.2

    cdef double V = beam_cross_section_area
    cdef double rho_a = beam_rho
    cdef double lambda_p = protection_k
    cdef double rho_p = protection_rho
    cdef double A_p = protection_protected_perimeter
    cdef double c_p = protection_c

    cdef double d = fire_time[1] - fire_time[0]

    cdef int i
    cdef int solver_iter_count = 0
    cdef bint flag_heating_started = False
    cdef bint solver_convergence_status = False
    cdef double t, T_g, c_s, phi, a, b, c, dT, d_p_3, T, T_1, T_2, T_3

    # Ensure d_p_1 < d_p_2 (swap if needed)
    if d_p_1 > d_p_2:
        d_p_1, d_p_2 = d_p_2, d_p_1

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

    cdef double d_p = (d_p_1+d_p_2) / 2 + ((np.random.rand() - 0.5) * abs(d_p_1-d_p_2) * 0.1)  # initial

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


cpdef tuple protection_thickness_2(
        double[:] fire_time,            # Use memoryview for efficient array access
        double[:] fire_temperature,
        double beam_rho,
        double beam_cross_section_area,
        double protection_k,            # Units typically W/m/K
        double protection_rho,
        double protection_c,            # Units typically J/kg/K
        double protection_protected_perimeter,
        double solver_temperature_goal, # Target max steel temperature [K]
        double solver_temperature_goal_tol, # Tolerance [K]
        int solver_max_iter = 100,
        double d_p_1 = 0.0001,          # Lower bound of protection thickness [m]
        double d_p_2 = 0.0900,          # Upper bound of protection thickness [m]
        double d_p_i = 0.0010,          # Step size for initial linear search [m]
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
        1. Constant time interval in `fire_time` throughout (Assumed by underlying `temperature_max`?).
        2. `fire_temperature` has *one* maxima (Assumed by underlying `temperature_max`?).
        3. **Requires** `T_a_max` from `temperature_max` to be MONOTONIC DECREASING with `protection_thickness`.

    PARAMETERS:
    :param fire_time:                       Time array [s] (memoryview)
    :param fire_temperature:                Gas temperature array [K] (memoryview)
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
    cdef int STATUS_SUCCESS = 0
    cdef int STATUS_OUT_OF_LOWER_BOUND = 1
    cdef int STATUS_OUT_OF_UPPER_BOUND = 2
    cdef int STATUS_MAX_ITERATIONS_REACHED = 3
    cdef int STATUS_MONOTONICITY_FAILED = 4

    # Input validation (basic)
    if d_p_1 < 0 or d_p_2 <= d_p_1 or d_p_i <= 0:
        # Consider raising specific errors or returning a dedicated status code
        raise ValueError("Invalid bounds or step size (d_p_1 >= 0, d_p_2 > d_p_1, d_p_i > 0 required)")
    if solver_temperature_goal_tol <= 0:
        raise ValueError("Solver tolerance must be positive")
    if solver_max_iter < 2:
        raise ValueError("Solver max iterations must be at least 2")
    if fire_time.shape[0] == 0 or fire_time.shape[0] != fire_temperature.shape[0]:
        raise ValueError("fire_time and fire_temperature must be non-empty and have the same length")

    # Result tracking variables (initialize with values from d_p_1)
    cdef double best_d_p = d_p_1
    cdef double best_T = 0.0 # Will be overwritten by first call
    cdef double best_t = 0.0 # Will be overwritten by first call
    cdef double min_abs_diff_found = 1e18 # Initialize with a large value
    cdef int total_iter_count = 0

    # Individual iteration variables
    cdef double T_current, t_current
    cdef double d_p_current, d_p_previous
    cdef double T_previous, t_previous # Needed for monotonicity check
    cdef double d_p_low = -1.0  # Sentinel value indicating bracket not yet found
    cdef double d_p_high = -1.0 # Sentinel value
    cdef double d_p_mid
    cdef double current_diff
    cdef int i # Loop counter for binary search

    # Common parameters dict for temperature_max call
    # Using dict is convenient; pass args directly if call overhead is critical
    cdef dict common_params = {
        'fire_time': fire_time,
        'fire_temperature': fire_temperature,
        'beam_rho': beam_rho,
        'beam_cross_section_area': beam_cross_section_area,
        'protection_k': protection_k,
        'protection_rho': protection_rho,
        'protection_c': protection_c,
        'protection_protected_perimeter': protection_protected_perimeter,
    }

    # --- Initial Check at Lower Bound (d_p_1) ---
    (T_current, t_current) = temperature_max(protection_thickness=d_p_1, **common_params)
    total_iter_count += 1

    # Initialise best solution tracking using the first result
    min_abs_diff_found = fabs(T_current - solver_temperature_goal)
    best_d_p = d_p_1
    best_T = T_current
    best_t = t_current

    # Check if T(d_p_1) is already too low (below target - tolerance)
    if T_current < solver_temperature_goal - solver_temperature_goal_tol:
        return best_d_p, best_T, best_t, total_iter_count, STATUS_OUT_OF_LOWER_BOUND

    # Check if T(d_p_1) is within tolerance
    # Check T is between [goal - tol, goal + tol]
    if T_current <= solver_temperature_goal + solver_temperature_goal_tol:
        # Note: This also covers the case where T_current is exactly goal +/- tol
        return best_d_p, best_T, best_t, total_iter_count, STATUS_SUCCESS

    # --- Linear Step Search (from d_p_1 + d_p_i up to d_p_2) ---
    d_p_previous = d_p_1
    T_previous = T_current # Store result from d_p_1
    t_previous = t_current

    while True:
        # Check iteration count before potentially expensive calculation
        if total_iter_count >= solver_max_iter:
            return best_d_p, best_T, best_t, total_iter_count, STATUS_MAX_ITERATIONS_REACHED

        # Calculate next d_p, clamped to d_p_2
        d_p_current = d_p_previous + d_p_i
        if d_p_current >= d_p_2:
            d_p_current = d_p_2

        # Avoid infinite loop if stuck at d_p_2 (e.g., if d_p_i is tiny)
        if d_p_current == d_p_previous:
            # This means we are at d_p_2. Exit loop to check final T.
            break

        # Solve T for current d_p
        (T_current, t_current) = temperature_max(protection_thickness=d_p_current, **common_params)
        total_iter_count += 1

        # --- Monotonicity Check ---
        # Check if temperature increased (or stayed exactly same) when thickness increased.
        # Using '>' handles increase. If T_current == T_previous is also an issue, use '>='.
        if T_current > T_previous:
            # Temperature increased unexpectedly! Violates assumption.
            # Return the *previous* state, as it was the last valid point.
            return d_p_previous, T_previous, t_previous, total_iter_count, STATUS_MONOTONICITY_FAILED
        # --- End Monotonicity Check ---

        # Update best solution found so far (closest to goal)
        current_diff = fabs(T_current - solver_temperature_goal)
        if current_diff < min_abs_diff_found:
            min_abs_diff_found = current_diff
            best_d_p = d_p_current
            best_T = T_current
            best_t = t_current

        # Check if T_current is now low enough to bracket the solution or hit target
        # T_previous was > goal + tol (otherwise we'd have returned earlier)
        # We need T_current <= goal + tol to form a bracket [prev, current]
        if T_current <= solver_temperature_goal + solver_temperature_goal_tol:
            # Temperature is now potentially in range or below the target range.
            # We have found a bracket: [d_p_previous, d_p_current]
            d_p_low = d_p_previous
            d_p_high = d_p_current
            break # Exit linear search loop to start binary search

        # Prepare for next iteration of linear search
        d_p_previous = d_p_current
        T_previous = T_current
        t_previous = t_current

        # If d_p_current reached d_p_2 in this iteration, the loop condition
        # `d_p_current == d_p_previous` will catch it in the *next* iteration's check and break.

    # --- Post Linear Search ---

    # We exited the linear search. Check why.

    # Case 1: Did we exit because d_p reached d_p_2?
    # Check if T at d_p_2 (the last T_current calculated) is still too high.
    # This implies a bracket was *never* found where T_current <= goal + tol.
    if d_p_current == d_p_2 and d_p_low < 0: # Bracket not found via T <= goal+tol check
        # Verify the temperature at d_p_2 (T_current) is indeed too high
        if T_current > solver_temperature_goal + solver_temperature_goal_tol:
            # Even at max thickness d_p_2, the temperature is still too high
            # Return the best result found (which might be d_p_2 or slightly less if tolerance was large)
            return best_d_p, best_T, best_t, total_iter_count, STATUS_OUT_OF_UPPER_BOUND
        else:
            # This case is subtle: we hit d_p_2, T(d_p_2) is acceptable, but the explicit
            # T_current <= goal + tol check inside the loop was never met before hitting d_p_2.
            # This implies T_previous(d_p_2 - d_p_i) > goal + tol AND T_current(d_p_2) <= goal + tol.
            # So a bracket [d_p_previous, d_p_2] exists. Set it up for binary search.
             d_p_low = d_p_previous
             d_p_high = d_p_current # d_p_current == d_p_2 here

    # Case 2: We exited because a bracket [d_p_low, d_p_high] was found where
    # T(d_p_low) > goal + tol and T(d_p_high) <= goal + tol.
    # Proceed only if a valid bracket was established (d_p_low >= 0)
    if d_p_low >= 0 and d_p_low < d_p_high:
        # --- Binary Search Refinement ---
        for i in range(total_iter_count, solver_max_iter): # Count total iterations correctly
            # Use safer midpoint calculation to avoid potential overflow if low/high are large
            d_p_mid = d_p_low + 0.5 * (d_p_high - d_p_low)

            # Check if interval is already tiny (machine precision or negligible difference)
            if (d_p_high - d_p_low) < 1e-12: # Adjust tolerance as needed based on d_p scale
                 # Interval too small, consider it converged. Return the best found so far.
                 # Check if the midpoint temperature is actually closer than 'best' before returning
                 (T_mid, t_mid) = temperature_max(protection_thickness=d_p_mid, **common_params)
                 total_iter_count += 1 # Count this evaluation
                 mid_diff = fabs(T_mid - solver_temperature_goal)
                 if mid_diff < min_abs_diff_found:
                    return d_p_mid, T_mid, t_mid, total_iter_count, STATUS_SUCCESS
                 else:
                    # Stick with previously found best if midpoint isn't better
                    return best_d_p, best_T, best_t, total_iter_count, STATUS_SUCCESS # Converged due to interval size


            # Evaluate temperature at midpoint
            (T_current, t_current) = temperature_max(protection_thickness=d_p_mid, **common_params)
            total_iter_count += 1 # Increment AFTER the call

            # Update best solution tracking during binary search
            current_diff = fabs(T_current - solver_temperature_goal)
            if current_diff < min_abs_diff_found:
                min_abs_diff_found = current_diff
                best_d_p = d_p_mid
                best_T = T_current
                best_t = t_current

            # Check if solution is within tolerance [goal - tol, goal + tol]
            if T_current <= solver_temperature_goal + solver_temperature_goal_tol and \
               T_current >= solver_temperature_goal - solver_temperature_goal_tol:
                # Solution found within tolerance
                return d_p_mid, T_current, t_current, total_iter_count, STATUS_SUCCESS

            # Update binary search bounds based on midpoint temperature
            if T_current > solver_temperature_goal:
                # Temp too high (or above goal), need thicker protection -> increase lower bound
                d_p_low = d_p_mid
            else:
                # Temp too low (or below goal), need thinner protection -> decrease upper bound
                d_p_high = d_p_mid

            # Check iteration count *inside* binary search loop
            if total_iter_count >= solver_max_iter:
                 # Max iterations reached during binary search refinement
                 return best_d_p, best_T, best_t, total_iter_count, STATUS_MAX_ITERATIONS_REACHED

        # If binary search loop finishes without converging (should be caught by max_iter inside)
        return best_d_p, best_T, best_t, total_iter_count, STATUS_MAX_ITERATIONS_REACHED

    # --- Fallback / Unexpected Exit ---
    # This path *should* ideally not be reached if logic above is sound.
    # It might indicate an edge case not handled (e.g., linear search ended without
    # finding a bracket and without hitting d_p_2 explicitly).
    # Return the best found result and infer status cautiously.
    final_status = STATUS_MAX_ITERATIONS_REACHED # Default guess
    if d_p_current == d_p_2 and best_T > solver_temperature_goal + solver_temperature_goal_tol:
        final_status = STATUS_OUT_OF_UPPER_BOUND
    elif fabs(best_T - solver_temperature_goal) <= solver_temperature_goal_tol:
        # If the best T found happens to be within tolerance
        final_status = STATUS_SUCCESS

    # Log a warning maybe? print("Warning: Solver reached fallback return path.")
    return best_d_p, best_T, best_t, total_iter_count, final_status
