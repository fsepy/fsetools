from math import e
from typing import Tuple

from fsetools.libstd.bs_en_1991_1_2_2002_annex_e import equation_e1_design_fire_load_density, table_e1_delta_q1, \
    table_e1_delta_q2, table_e2_delta_n

SYMBOLS = dict(
    d_f=("flame thickness", "m"),
    w_t=("opening width", "m"),
    h_eq=("opening height", "m"),
    L_1=("flame length (angled)", "m"),
    L_L=("flame length (vertical)", "m"),
    L_f=("flame length (total)", "m"),
    L_H=("distance between `L_L` and wall", "m"),
    T_0=("ambient temperature", "K"),
    T_w=("flame temperature at window opening", "K"),
    T_z=("flame temperature external", "K"),
    L_x=("axis length from the window to the point of measurement", "m"),
    d_ow=("distance between this opening edge to other openings' edge", "m"),
    W=("width of wall containing windows", "m"),
    D=("depth of the fire compartment or diameter of the fire", "m"),
    O=("opening factor, h_eq ** 0.5 * A_v / A_t", "m**0.5"),
    tau_F=("free burning fire duration", "s"),
    q_f_d=("design fire load density related to the floor area A_t", "MJ/m**2"),
    q_f_k=("characteristic fire load density related to the floor area to A_t", "MJ/m**2"),
    alpha_c=("convection coefficient of external flame", "W/m**2/K"),
    Q=("the rate of heat release rate", "MW"),
    epsilon_f=("emissivity of flames", "-")
)

"""
d_f      [m]         flame thickness
w_t      [m]         opening width
h_eq     [m]         opening height
L_1      [m]         flame length (angled)
L_L      [m]         flame length (vertical)
L_f      [m]         flame length (total)
L_H      [m]         distance between `L_L` and wall
T_0      [K]         ambient temperature
T_w      [K]         flame temperature at window opening
T_z      [K]         flame temperature external
L_x      [m]         axis length from the window to the point of measurement
d_ow     [m]         distance between this opening edge to other openings' edge
W        [m]         width of wall containing windows
D        [m]         depth of the fire compartment or diameter of the fire
O        [m**0.5]    opening factor, h_eq ** 0.5 * A_v / A_t
tau_F    [s]         free burning fire duration
q_f_d    [MJ/m**2]   design fire load density related to the floor area A_t
q_f_k    [MJ/m**2]   characteristic fire load density related to the floor area to A_t
alpha_c  [W/m**2/K]  convection coefficient of external flame
Q        [MW]        the rate of heat release rate

Table E.4 in BS EN 1991-1-2:2002, page 50
Fire load densities q_f_k [MJ/m2] for different occupancies
| Occupancy Average        | Average | 80 % fractile |
|--------------------------|---------|---------------|
| Dwelling                 | 780     | 948           |
| Hospital (room)          | 230     | 280           |
| Hotel (room)             | 310     | 377           |
| Library                  | 1500    | 1824          |
| Office                   | 420     | 511           |
| Classroom of a school    | 285     | 347           |
| Shopping centre          | 600     | 730           |
| Theatre (cinema)         | 300     | 365           |
| Transport (public space) | 100     | 122           |
Gumbel distribution
"""


def equation_b4_heat_release_rate(
        A_f,
        q_f_d,
        tau_F,
        O,
        A_v,
        h_eq,
        D,
        W,
        *_,
        **__,
):
    """Equation B.4. The rate of burning or the rate of heat release"""
    a = (A_f * q_f_d) / tau_F
    b = 3.15 * (1 - e ** (-0.036 / O)) * A_v * (h_eq / (D / W)) ** 0.5
    Q = min(a, b)
    return Q


def equation_b5_compartment_temperature(
        O,
        omega,
        T_0,
        *_,
        **__,
):
    a = 6000 * (1 - 2.718282 ** (-0.1 / O))
    b = O ** 0.5
    c = (1 - 2.718282 ** (-0.00286 * omega))
    d = T_0
    T_f = a * b * c * d
    return T_f


def clause_b_4_1_3_flame_vertical_projection(
        Q,
        A_v,
        h_eq,
        w_t,
        rho_g=0.45,
        g=9.81,
        *_,
        **__,
):
    a = 0
    if rho_g == 0.45 and g == 9.81:
        b = 1.9 * (Q / w_t) ** (2 / 3) - h_eq
    else:
        b_ = Q / (A_v * rho_g * (h_eq * g) ** 0.5)
        b = h_eq * (2.37 * b_ ** (2 / 3) - 1)
    L_L = max(a, b)
    return L_L


def clause_b_4_1_6_flame_horizontal_projection(
        h_eq,
        w_t,
        d_ow,
        L_L,
        is_wall_above_opening: bool = True,
        *_,
        **__,
):
    if is_wall_above_opening:
        if h_eq <= 1.25 * w_t:
            # equation B.8
            L_H = h_eq / 3
        elif h_eq > 1.25 * w_t and d_ow > 4 * w_t:
            L_H = 0.3 * h_eq * (h_eq / w_t) ** 0.54
        else:
            L_H = 0.454 * h_eq * (h_eq / 2 / w_t) ** 0.54
    else:
        L_H = 0.6 * h_eq * (L_L / h_eq) ** 1 / 3

    return L_H


def clause_b_4_1_7_flame_length(
        w_t,
        L_L,
        L_H,
        h_eq,
        is_wall_above_opening
):
    # assert is_wall_above_opening is True and \

    if is_wall_above_opening and h_eq <= 1.25 * w_t:
        # equation B.12
        L_f = L_L + h_eq / 2
    elif is_wall_above_opening is False or h_eq > 1.25 * w_t:
        # equation B.13
        a = (L_L ** 2 * (L_H - h_eq / 3) ** 2) ** 0.5
        b = h_eq / 2
        L_f = a * b
    else:
        raise ValueError('No conditions are met when calculating `L_f`')

    return L_f


def equation_b14_flame_temperature_at_window(
        L_f,
        w_t,
        Q,
        T_0,
        *_,
        **__,
):
    """Equation B.14. Flame temperature at the window opening."""

    assert L_f * w_t / Q < 1

    T_w = 520 / (1 - 0.4725 * (L_f * w_t / Q)) + T_0
    return T_w


def equation_b15_flame_temperature_along_axis(
        T_w,
        T_0,
        L_x,
        w_t,
        Q,
        *_,
        **__,
):
    """Equation B.15 in BS EN 1991-1-2:2002, page 38.
    Flame temperature along the axis."""
    assert L_x * w_t / Q < 1
    T_z = (T_w - T_0) * (1 - 0.4725 * (L_x * w_t / Q)) + T_0
    return T_z


def equation_b16_flame_emissivity(
        d_f,
        *_,
        **__,
):
    e_t = 1 - 2.718282 ** (-0.3 * d_f)
    return e_t


def equation_b17_convective_heat_transfer_coefficient(
        d_eq,
        Q,
        A_v,
        *_,
        **__,
):
    alpha_c = 4.67 * (1 / d_eq) ** 0.5 * (Q / A_v) ** 0.6
    return alpha_c


def clause_b_4_1_13_modification_to_flame_with_balcony_above_opening(
        L_L,
        L_H,
        W_a,
        is_wall_above_opening: bool = True,
        is_balcony_above_opening: bool = True
) -> Tuple[float, float]:
    assert is_balcony_above_opening and is_wall_above_opening
    L_L = L_L - W_a * (1 + 2 ** 0.5)
    L_H = L_H + W_a
    return L_L, L_H


def clause_b_4_1_14_modification_to_flame_with_no_wall_above_opening(
        L_L,
        L_H,
        W_a,
        is_wall_above_opening: bool = False,
        is_balcony_above_opening: bool = True
):
    assert is_balcony_above_opening and is_wall_above_opening is False
    L_L = L_L - W_a
    L_H = L_H + W_a
    return L_L, L_H


def clause_b_4_2_1_heat_release_rate(
        A_f,
        q_f_d,
        tau_F
):
    """equation B.18, page 37"""
    Q = (A_f * q_f_d) / tau_F
    return Q


def clause_b_4_2_2_compartment_temperature(
        omega,
        T_0
):
    """equation B.19, page 37"""
    T_f = 1200 * (1 - e ** (-0.00228 * omega)) + T_0
    return T_f


def clause_b_4_2_3_flame_vertical_projection(
        h_eq,
        Q,
        A_v,
        u,
):
    # equation B.20, page 37
    a = 1.366 * (1 / u) ** 0.43
    b = Q / (A_v ** 0.5)
    L_L = (a * b) - h_eq
    return L_L


def clause_b_4_2_4_flame_horizontal_projection(
        h_eq,
        L_L,
        u
):
    # equation B.21, page 38
    a = 0.605
    b = (u ** 2 / h_eq) ** 0.22
    c = (L_L + h_eq)
    L_H = a * b * c
    return L_H


def clause_b_4_2_5_flame_width(
        w_t,
        L_H
):
    # equation B.22, page 38
    w_f = w_t + 0.4 * L_H
    return w_f


def clause_b_4_2_6_flame_length(
        L_L,
        L_H
):
    # equation B.23, page 38
    L_f = (L_L ** 2 + L_H ** 2) ** 0.5
    return L_f


def clause_b_4_2_7_flame_temperature_at_opening(
        A_v,
        Q,
        L_f,
        T_0
):
    # equation B.24, page 38
    assert L_f * (A_v ** 0.5) / Q < 1
    T_w = 520 / (1 - 0.3325 * L_f * (A_v ** 0.5) / Q) + T_0
    return T_w


def clause_b_4_2_9_flame_temperature_along_axis(
        L_x,
        Q,
        A_v,
        T_w,
        T_0
):
    # equation B.25, page 38
    a = (1 - 0.3325 * L_x * (A_v ** 0.5) / Q)
    b = T_w - T_0
    T_z = a * b + T_0
    return T_z


def clause_b_4_2_10_flame_emissivity(
        d_f
):
    # equation B.26, page 39
    e_f = 1 - e ** (-0.3 * d_f)
    return e_f


def clause_b_4_2_11_convective_heat_transfer_coefficient(
        d_eq,
        A_v,
        Q,
        u
):
    # equation B.27, page 39
    a = 9.8 * (1 / d_eq) ** 0.4
    b = (Q / 17.5 / A_v + u / 1.6) ** 0.6
    alpha_c = a * b
    return alpha_c


def __test_external_fire_length_1():
    """Test against analysis carried in report '190702-R00-SC19024-WP1-Flame Projection Calculations-DN-CIC'.
    Wall above opening and no balcony above opening.
    """
    # calculate flame external temperature at:
    #       (1) vertical distance above opening top edge
    #       (2) horizontal distance away from wall

    is_wall_above_opening = True

    w_t = 1.82
    h_eq = 1.1
    d_ow = 1e10
    D = 14.52  # calculated based on floor area 70.3 and D/W = 3
    W = 4.84  # calculated based on floor area 70.3 and D/W = 3
    q_f_k = 870
    tau_F = 1200

    is_sprinklered = True
    is_sprinkler_indipendent_water_supplies = True
    is_automatic_fire_detection = True
    is_detection_by_heat = False
    is_detection_by_smoke = False
    is_automatic_transmission_to_fire_brigade = True
    is_onsite_fire_brigade = False
    is_offsite_fire_brigade = True
    is_safe_access_routes = True
    is_fire_fighting_devices = True
    is_smoke_exhaust_system = True

    # derived values below
    A_v = 2.002
    A_f = 14.88
    A_t = D * W
    O = 0.03
    # todo W/H

    # ----------------------------------
    # Calculate design fire load density
    # ----------------------------------
    delta_q1 = table_e1_delta_q1(A_f=A_f)
    delta_q2 = table_e1_delta_q2(occupancy='office')
    delta_n = table_e2_delta_n(
        is_sprinklered=is_sprinklered,
        is_sprinkler_indipendent_water_supplies=is_sprinkler_indipendent_water_supplies,
        is_automatic_fire_detection=is_automatic_fire_detection,
        is_detection_by_heat=is_detection_by_heat,
        is_detection_by_smoke=is_detection_by_smoke,
        is_automatic_transmission_to_fire_brigade=is_automatic_transmission_to_fire_brigade,
        is_onsite_fire_brigade=is_onsite_fire_brigade,
        is_offsite_fire_brigade=is_offsite_fire_brigade,
        is_safe_access_routes=is_safe_access_routes,
        is_fire_fighting_devices=is_fire_fighting_devices,
        is_smoke_exhaust_system=is_smoke_exhaust_system
    )

    q_f_d = equation_e1_design_fire_load_density(
        q_f_k=q_f_k,
        m=0.8,
        delta_q1=delta_q1,
        delta_q2=delta_q2,
        delta_n=delta_n
    )

    q_f_d = 870

    # ---------------------------
    # Calculate heat release rate
    # ---------------------------
    Q = equation_b4_heat_release_rate(
        A_f=A_f,
        q_f_d=q_f_d,
        tau_F=tau_F,
        O=O,
        A_v=A_v,
        h_eq=h_eq,
        D=D,
        W=W
    )

    # --------------------------------------------
    # Calculate external flame vertical projection
    # --------------------------------------------
    L_L = clause_b_4_1_3_flame_vertical_projection(
        Q=Q,
        A_v=A_v,
        h_eq=h_eq,
        w_t=w_t
    )

    # ----------------------------------------------
    # Calculate external flame horizontal projection
    # ----------------------------------------------
    L_H = clause_b_4_1_6_flame_horizontal_projection(
        h_eq=h_eq,
        w_t=w_t,
        d_ow=d_ow,
        L_L=L_L,
    )

    # ----------------------
    # Calculate flame length
    # ----------------------
    L_f = clause_b_4_1_7_flame_length(
        w_t=w_t,
        L_L=L_L,
        L_H=L_H,
        h_eq=h_eq,
        is_wall_above_opening=is_wall_above_opening
    )

    print(f'{L_f} == 1.9')
    assert abs(L_f - 1.9) < 1e-2


def __test_external_fire_temperature_1():
    """
    0Test against analysis carried in report '190702-R00-SC19024-WP1-Flame Projection Calculations-DN-CIC'.
    Wall above opening and no balcony above opening.
    """

    is_wall_above_opening = True

    w_t = 1.82
    h_eq = 2.75
    d_ow = 1e10
    D = 64
    W = 51
    H = 2.75
    q_f_k = 511
    tau_F = 1200

    is_sprinklered = True
    is_sprinkler_independent_water_supplies = True
    is_automatic_fire_detection = True
    is_detection_by_heat = False
    is_detection_by_smoke = False
    is_automatic_transmission_to_fire_brigade = True
    is_onsite_fire_brigade = False
    is_offsite_fire_brigade = True
    is_safe_access_routes = True
    is_fire_fighting_devices = True
    is_smoke_exhaust_system = True

    T_0 = 293.15

    # derived values below
    A_v = h_eq * w_t
    A_f = D * W
    A_t = 2 * (D * W + W * H + H * D)
    O = h_eq ** 0.5 * A_v / A_t

    # todo W/H
    print('{:>10.10}: {:<.2f}'.format('A_v', A_v))
    print('{:>10.10}: {:<.2f}'.format('A_f', A_f))
    print('{:>10.10}: {:<.2f}'.format('A_t', A_t))
    print('{:>10.10}: {:<.3f}\n'.format('O', O))

    # ----------------------------------
    # Calculate design fire load density
    # ----------------------------------
    delta_q1 = table_e1_delta_q1(A_f=A_f)
    delta_q2 = table_e1_delta_q2(occupancy='office')
    delta_n = table_e2_delta_n(
        is_sprinklered=is_sprinklered,
        is_sprinkler_indipendent_water_supplies=is_sprinkler_independent_water_supplies,
        is_automatic_fire_detection=is_automatic_fire_detection,
        is_detection_by_heat=is_detection_by_heat,
        is_detection_by_smoke=is_detection_by_smoke,
        is_automatic_transmission_to_fire_brigade=is_automatic_transmission_to_fire_brigade,
        is_onsite_fire_brigade=is_onsite_fire_brigade,
        is_offsite_fire_brigade=is_offsite_fire_brigade,
        is_safe_access_routes=is_safe_access_routes,
        is_fire_fighting_devices=is_fire_fighting_devices,
        is_smoke_exhaust_system=is_smoke_exhaust_system
    )

    q_f_d = equation_e1_design_fire_load_density(
        q_f_k=q_f_k,
        m=0.8,
        delta_q1=delta_q1,
        delta_q2=delta_q2,
        delta_n=delta_n
    )
    print('{:>10.10}: {:<.2f}'.format('q_f_d', q_f_d))

    # ---------------------------
    # Calculate heat release rate
    # ---------------------------
    Q = equation_b4_heat_release_rate(
        A_f=A_f,
        q_f_d=q_f_d,
        tau_F=tau_F,
        O=O,
        A_v=A_v,
        h_eq=h_eq,
        D=D,
        W=W
    )
    print('{:>10.10}: {:<.2f}'.format('Q', Q))

    # --------------------------------------------
    # Calculate external flame vertical projection
    # --------------------------------------------
    L_L = clause_b_4_1_3_flame_vertical_projection(
        Q=Q,
        A_v=A_v,
        h_eq=h_eq,
        w_t=w_t
    )
    print('{:>10.10}: {:<.2f}'.format('L_L', L_L))

    # ----------------------------------------------
    # Calculate external flame horizontal projection
    # ----------------------------------------------
    L_H = clause_b_4_1_6_flame_horizontal_projection(
        h_eq=h_eq,
        w_t=w_t,
        d_ow=d_ow,
        L_L=L_L,
    )
    print('{:>10.10}: {:<.2f}'.format('L_H', L_H))

    # ----------------------
    # Calculate flame length
    # ----------------------
    L_f = clause_b_4_1_7_flame_length(
        w_t=w_t,
        L_L=L_L,
        L_H=L_H,
        h_eq=h_eq,
        is_wall_above_opening=is_wall_above_opening
    )
    print('{:>10.10}: {:<.2f}'.format('L_f', L_f))

    # --------------------------------------
    # Calculate flame temperature at opening
    # --------------------------------------
    T_w = equation_b14_flame_temperature_at_window(
        L_f=L_f,
        w_t=w_t,
        Q=Q,
        T_0=T_0
    )
    print('{:>10.10}: {:<.2f}'.format('T_w', T_w - 273.15))

    # ------------------------------------------
    # Calculate flame temperature beyond opening
    # ------------------------------------------
    L_x = 2.5
    T_x = equation_b15_flame_temperature_along_axis(
        T_w=T_w,
        T_0=T_0,
        L_x=L_x,
        w_t=w_t,
        Q=Q
    )
    print('{:>10.10}: {:<.2f}'.format('T_x', T_x - 273.15))

    pass


def __test_forced_draught():

    W = 50
    D = 70
    H = 3
    h_eq = 2.75
    w_t = 50
    q_f_k = 511
    L_x = 1.2

    A_f = W * D
    tau_F = 1200
    A_v = w_t * h_eq
    T_0 = 273.15
    u = 6  # check

    is_sprinklered = True
    is_sprinkler_independent_water_supplies = True
    is_automatic_fire_detection = True
    is_detection_by_heat = False
    is_detection_by_smoke = False
    is_automatic_transmission_to_fire_brigade = True
    is_onsite_fire_brigade = False
    is_offsite_fire_brigade = True
    is_safe_access_routes = True
    is_fire_fighting_devices = True
    is_smoke_exhaust_system = True

    delta_q1 = table_e1_delta_q1(A_f=A_f)
    delta_q2 = table_e1_delta_q2(occupancy='office')
    delta_n = table_e2_delta_n(
        is_sprinklered=is_sprinklered,
        is_sprinkler_indipendent_water_supplies=is_sprinkler_independent_water_supplies,
        is_automatic_fire_detection=is_automatic_fire_detection,
        is_detection_by_heat=is_detection_by_heat,
        is_detection_by_smoke=is_detection_by_smoke,
        is_automatic_transmission_to_fire_brigade=is_automatic_transmission_to_fire_brigade,
        is_onsite_fire_brigade=is_onsite_fire_brigade,
        is_offsite_fire_brigade=is_offsite_fire_brigade,
        is_safe_access_routes=is_safe_access_routes,
        is_fire_fighting_devices=is_fire_fighting_devices,
        is_smoke_exhaust_system=is_smoke_exhaust_system
    )

    q_f_d = equation_e1_design_fire_load_density(
        q_f_k=q_f_k,
        m=0.8,
        delta_q1=delta_q1,
        delta_q2=delta_q2,
        delta_n=delta_n
    )

    Q = clause_b_4_2_1_heat_release_rate(
        A_f=A_f,
        q_f_d=q_f_d,
        tau_F=tau_F,
    )

    Q = 30

    L_L = clause_b_4_2_3_flame_vertical_projection(
        h_eq=h_eq,
        Q=Q,
        A_v=A_v,
        u=u
    )

    L_H = clause_b_4_2_4_flame_horizontal_projection(
        h_eq=h_eq,
        L_L=L_L,
        u=u
    )

    L_f = clause_b_4_2_6_flame_length(
        L_L=L_L,
        L_H=L_H
    )

    T_w = clause_b_4_2_7_flame_temperature_at_opening(
        A_v=A_v,
        Q=Q,
        L_f=L_f,
        T_0=T_0
    )

    clause_b_4_2_9_flame_temperature_along_axis(
        L_x=L_x,
        Q=Q,
        A_v=A_v,
        T_w=T_w,
        T_0=T_0
    )


if __name__ == '__main__':
    l1, l2 = max([len(i) for i in SYMBOLS.keys()]), max([len(v[1]) for k, v in SYMBOLS.items()])
    print_str = [f'{k:{l1:d}.{l1:d}}  {f"[{v[1]}]":{l2 + 2:d}.{l2 + 2:d}}  {v[0]:<}' for k, v in SYMBOLS.items()]
    print('\n'.join(print_str))

    # __test_external_fire_length_1()
    # __test_external_fire_temperature_1()
    __test_forced_draught()

    pass
