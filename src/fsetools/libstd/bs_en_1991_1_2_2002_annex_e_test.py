from .bs_en_1991_1_2_2002_annex_e import *


def test_1():
    obj = FireLoadDensity()

    kwargs = dict(
        A_f=1500,
        q_f_k=870,
        m=0.8,
        occupancy=obj.OCCUPANCY_OFFICE,
        is_sprinklered=True,
        sprinkler_independent_water_supplies=True,
        is_detection_by_heat=False,
        is_detection_by_smoke=True,
        is_automatic_transmission_to_fire_brigade=False,
        is_onsite_fire_brigade=False,
        is_offsite_fire_brigade=True,
        is_safe_access_routes=True,
        is_fire_fighting_devices=True,
        is_smoke_exhaust_system=True,
    )
    q_f_d = obj.calculate(**kwargs)['q_f_d']
    try:
        assert abs(q_f_d - 399.6035989920) < 1e-8
    except Exception as e:
        raise e
