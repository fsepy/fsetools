from typing import Union

SYMBOLS = dict(
    q_fk=("MJ/m**2", "characteristic fire load density related to the floor area to $A_t$"),
    m=(),
    delta_q1=(),
    delta_q2=(),
    delta_n=(),
    q_fd=(),
)


def equation_e1_design_fire_load_density(
        q_fk,
        m,
        delta_q1,
        delta_q2,
        delta_n,
        *_,
        **__
) -> dict:
    q_fd = q_fk * m * delta_q1 * delta_q2 * delta_n

    _latex = [
        f'q_{{fd}}=q_{{fk}}\\cdot m\\cdot \\delta_{{q1}}\\cdot \\delta_{{q2}}\\cdot \\delta_n',
        f'q_{{fd}}={q_fk:.2f}\\cdot {m:.2f}\\cdot \\{delta_q1:.2f}\\cdot \\{delta_q2:.2f}\\cdot \\{delta_n:.2f}',
        f'q_{{fd}}={q_fd:.2f}',
    ]
    return dict(q_fd=q_fd, _latex=_latex)


def table_e1_delta_q1(
        A_f,
        *_,
        **__,
) -> float:
    if A_f <= 25:
        delta_q1 = 1.1
    elif A_f <= 250:
        delta_q1 = 1.5
    elif A_f <= 2500:
        delta_q1 = 1.9
    elif A_f <= 5000:
        delta_q1 = 2
    elif A_f <= 10000:
        delta_q1 = 2.13
    else:
        raise ValueError(f'Maximum floor area 10,000 m² exceeded {A_f}')
    return delta_q1


def table_e1_delta_q2(
        occupancy: Union[str, int],
        *_,
        **__,
) -> float:
    occupancy = occupancy.lower().strip()

    if occupancy == 1 or occupancy in ['artgallery', 'musem', 'swimming pool']:
        delta_q2 = 0.78
    elif occupancy == 2 or occupancy in ['office', 'residence', 'hotel', 'paper industry']:
        delta_q2 = 1.0
    elif occupancy == 3 or occupancy in ['manufactory for machinery & engines']:
        delta_q2 = 1.22
    elif occupancy == 4 or occupancy in ['chemical laboratory', 'painting workshop']:
        delta_q2 = 1.44
    elif occupancy == 5 or occupancy in ['manufactory of fireworks or paints']:
        delta_q2 = 1.66
    else:
        raise ValueError(f'Unknown occupancy "{occupancy}"')

    return delta_q2


def table_e2_delta_n(
        is_sprinklered: bool,
        is_sprinkler_independent_water_supplies: Union[bool, int],

        is_detection_by_heat: bool,
        is_detection_by_smoke: bool,
        is_automatic_transmission_to_fire_brigade: bool,

        is_onsite_fire_brigade: bool,
        is_offsite_fire_brigade: bool,

        is_safe_access_routes: bool,
        is_fire_fighting_devices: bool,
        is_smoke_exhaust_system: bool,
        *_,
        **__,

) -> float:
    delta_n1 = 0.61 if is_sprinklered else 1

    if is_sprinklered and is_sprinkler_independent_water_supplies == 1:
        delta_n2 = 0.87
    elif is_sprinklered and is_sprinkler_independent_water_supplies == 2:
        delta_n2 = 0.7
    else:
        delta_n2 = 1

    delta_n3 = 0.87 if is_detection_by_heat else 1
    delta_n4 = 0.73 if is_detection_by_smoke else 1
    delta_n5 = 0.87 if is_automatic_transmission_to_fire_brigade else 1
    delta_n6 = 0.61 if is_onsite_fire_brigade else 1
    delta_n7 = 0.78 if is_offsite_fire_brigade else 1
    delta_n8 = 1 if is_safe_access_routes else 1.5
    delta_n9 = 1 if is_fire_fighting_devices else 1.5
    delta_n10 = 1 if is_smoke_exhaust_system else 1.5

    delta_n = \
        delta_n1 * delta_n2 * delta_n3 * delta_n4 * delta_n5 * \
        delta_n6 * delta_n7 * delta_n8 * delta_n9 * delta_n10

    return delta_n


def _test(is_assertion=True):
    A_f = 1500
    q_fk = 870
    m = 0.8
    is_sprinklered = True
    is_sprinkler_independent_water_supplies = True
    is_detection_by_heat = False
    is_detection_by_smoke = True
    is_automatic_transmission_to_fire_brigade = False
    is_onsite_fire_brigade = False
    is_offsite_fire_brigade = True
    is_safe_access_routes = True
    is_fire_fighting_devices = True
    is_smoke_exhaust_system = True

    str_fmt = '{:>10.10}: {:<.2f}'

    delta_q1 = table_e1_delta_q1(A_f=A_f)
    delta_q2 = table_e1_delta_q2(occupancy='office')
    delta_n = table_e2_delta_n(
        is_sprinklered=is_sprinklered,
        is_sprinkler_independent_water_supplies=is_sprinkler_independent_water_supplies,
        is_detection_by_heat=is_detection_by_heat,
        is_detection_by_smoke=is_detection_by_smoke,
        is_automatic_transmission_to_fire_brigade=is_automatic_transmission_to_fire_brigade,
        is_onsite_fire_brigade=is_onsite_fire_brigade,
        is_offsite_fire_brigade=is_offsite_fire_brigade,
        is_safe_access_routes=is_safe_access_routes,
        is_fire_fighting_devices=is_fire_fighting_devices,
        is_smoke_exhaust_system=is_smoke_exhaust_system
    )
    print(str_fmt.format('delta_q1', delta_q1))
    print(str_fmt.format('delta_q2', delta_q2))
    print(str_fmt.format('delta_n', delta_n))

    q_fd = equation_e1_design_fire_load_density(
        q_fk=q_fk,
        m=m,
        delta_q1=delta_q1,
        delta_q2=delta_q2,
        delta_n=delta_n
    )['q_fd']
    print('{:>10.10}: {:<.10f}'.format('q_fd', q_fd))

    if is_assertion:
        assert abs(q_fd - 399.6035989920) < 1e-8


if __name__ == '__main__':
    _test(False)
