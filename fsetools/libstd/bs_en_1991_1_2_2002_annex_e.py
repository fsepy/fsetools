"""BS EN 1991-1-2:2002 Annex E: Fire load densities

The fire load density used in calculations should be a design value, either based on measurements or in special cases based on fire resistance requirements given in national regulations.

The design value may be determined:

    – from a national fire load classification of occupancies; and/or
    – specific for an individual project by performing a fire load survey.
"""

from typing import Union


class FireLoadDensity:
    OCCUPANCY_ART_GALLERY = 1
    OCCUPANCY_MUSEUM = 1
    OCCUPANCY_SWIMMING_POOL = 1
    OCCUPANCY_OFFICE = 2
    OCCUPANCY_RESIDENCE = 2
    OCCUPANCY_HOTEL = 2
    OCCUPANCY_PAPER_INDUSTRY = 2
    OCCUPANCY_MANUFACTORY_FOR_MACHINERY_AND_ENGINES = 3
    OCCUPANCY_CHEMICAL_LABORATORY = 4
    OCCUPANCY_PAINTING_WORKSHOP = 4
    OCCUPANCY_MANUFACTORY_OF_FIREWORKS_OR_PAINTS = 5

    def calculate(
            self,
            q_fk: float,
            A_f: float,
            m: float,
            occupancy: Union[str, int],
            is_sprinklered: bool,
            sprinkler_independent_water_supplies: int,
            is_detection_by_heat: bool,
            is_detection_by_smoke: bool,
            is_automatic_transmission_to_fire_brigade: bool,
            is_onsite_fire_brigade: bool,
            is_offsite_fire_brigade: bool,
            is_safe_access_routes: bool,
            is_fire_fighting_devices: bool,
            is_smoke_exhaust_system: bool,
    ):
        kwargs = dict(locals())
        kwargs.pop('self')
        kwargs.update(self.table_e1_delta_q1(**kwargs))
        kwargs.update(self.table_e1_delta_q2(**kwargs))
        kwargs.update(self.table_e2_delta_n(**kwargs))
        kwargs.update(self.clause_e_1_3_design_fire_load_density(**kwargs))
        return kwargs

    @staticmethod
    def clause_e_1_3_design_fire_load_density(
            q_fk: float,
            m: float,
            delta_q1: float,
            delta_q2: float,
            delta_n: float,
            **__
    ) -> dict:
        """The design value of the fire load, Clause E.1 (3), page 46.

        :param q_fk:        [MJ/m2],    is the characteristic fuel load density
        :type q_fk:         float
        :param m:           [-],        is the combustion factor (see E.3)
        :type m:            float
        :param delta_q1:    [-],        is a factor taking into account the fire activation risk due to the size of the 
                                        compartment (see Table E.1)
        :type delta_q1:     float
        :param delta_q2:    [-],        is a factor taking into account the fire activation risk due to the type of 
                                        occupancy (see Table E.1)
        :type delta_q2:     float
        :param delta_n:     [-],        is a factor taking into account the different active fire fighting measures i 
                                        (sprinkler, detection, automatic alarm transmission, firemen ...). These active 
                                        measures are generally imposed for life safety reason (see Table E.2 and 
                                        clauses(4) and (5))
        :type delta_n:      float
        :return:            q_fd and latex math expression
        :rtype:             dict
        """

        q_fd = q_fk * m * delta_q1 * delta_q2 * delta_n

        _latex = [
            f'q_{{fd}}=q_{{fk}}\\cdot m\\cdot \\delta_{{q1}}\\cdot \\delta_{{q2}}\\cdot \\delta_n',
            f'q_{{fd}}={q_fk:.2f}\\cdot {m:.2f}\\cdot \\{delta_q1:.2f}\\cdot \\{delta_q2:.2f}\\cdot \\{delta_n:.2f}',
            f'q_{{fd}}={q_fd:.2f}',
        ]
        return dict(q_fd=q_fd, _latex=_latex)

    @staticmethod
    def table_e1_delta_q1(A_f: float, **__) -> dict:
        """A factor taking into account the fire activation risk due to the size of the compartment (see Table E.1)

        :param A_f: [m2]    Compartment floor area
        :return:            delta_q1, is the factor taking into account of fire activation risk due to compartment size; and latex math expression
        """
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

        _latex = [f'\\delta_{{q1}}={delta_q1:.2f}']

        return dict(delta_q1=delta_q1, _latex=_latex)

    @staticmethod
    def table_e1_delta_q2(
            occupancy: Union[str, int],
            **__,
    ) -> dict:
        if isinstance(occupancy, str):
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

        _latex = [
            f'\\delta_{{q2}}={delta_q2:.2f}'
        ]

        return dict(delta_q2=delta_q2, _latex=_latex)

    @staticmethod
    def table_e2_delta_n(
            is_sprinklered: bool,
            sprinkler_independent_water_supplies: int,

            is_detection_by_heat: bool,
            is_detection_by_smoke: bool,
            is_automatic_transmission_to_fire_brigade: bool,

            is_onsite_fire_brigade: bool,
            is_offsite_fire_brigade: bool,

            is_safe_access_routes: bool,
            is_fire_fighting_devices: bool,
            is_smoke_exhaust_system: bool,
            **__,

    ) -> dict:
        """A factor taking into account the different active fire fighting measures i (sprinkler, detection, automatic 
        alarm transmission, firemen ...). These active measures are generally imposed for life safety reason (see 
        Table E.2 and clauses (4) and (5)).

        :param is_sprinklered:                              is automatic water suppression system provided?
        :type is_sprinklered:                               bool
        :param sprinkler_independent_water_supplies:        is the number of independent water supplies, 0 or 1 or 2
        :type sprinkler_independent_water_supplies:         int
        :param is_detection_by_heat:                        is automatic fire & smoke detection by heat?
        :type is_detection_by_heat:                         bool
        :param is_detection_by_smoke:                       is automatic fire & smoke detection by smoke?
        :type is_detection_by_smoke:                        bool
        :param is_automatic_transmission_to_fire_brigade:   is automatic alarm transmission to fire brigade?
        :type is_automatic_transmission_to_fire_brigade:    bool
        :param is_onsite_fire_brigade:                      is onsite fire brigade provided?
        :type is_onsite_fire_brigade:                       bool
        :param is_offsite_fire_brigade:                     is offsite fire brigade provided?
        :type is_offsite_fire_brigade:                      bool
        :param is_safe_access_routes:                       are safe access routes provided?
        :type is_safe_access_routes:                        bool
        :param is_fire_fighting_devices:                    are fire fighting devices provided?
        :type is_fire_fighting_devices:                     bool
        :param is_smoke_exhaust_system:                     is smoke exhaust system provided?
        :type is_smoke_exhaust_system:                      bool
        :return:                                            delta_n, the factor; and latex math expression
        :rtype:                                             dict
        """

        delta_n1 = 0.61 if is_sprinklered else 1

        if is_sprinklered and sprinkler_independent_water_supplies == 0:
            delta_n2 = 1.0
        elif is_sprinklered and sprinkler_independent_water_supplies == 1:
            delta_n2 = 0.87
        elif is_sprinklered and sprinkler_independent_water_supplies == 2:
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

        _latex = [
            f'\\delta_n=\\sum_{{i=1}}^{{10}}\\delta_{{ni}}',
            f'\\delta_n={delta_n1:.2f}+{delta_n2:.2f}+{delta_n3:.2f}+{delta_n4:.2f}+'
            f'{delta_n5:.2f}+{delta_n6:.2f}+{delta_n7:.2f}+{delta_n8:.2f}+{delta_n9:.2f}+{delta_n10:.2f}',
            f'\\delta_n={delta_n:.2f}'
        ]

        return dict(delta_n=delta_n, _latex=_latex)


class TestFireLoadDensity(FireLoadDensity):
    def __init__(self):
        super().__init__()
        self.test_1()

    def test_1(self):
        kwargs = dict(
            A_f=1500,
            q_fk=870,
            m=0.8,
            occupancy=self.OCCUPANCY_OFFICE,
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
        q_fd = self.calculate(**kwargs)['q_fd']
        assert abs(q_fd - 399.6035989920) < 1e-8


if __name__ == '__main__':
    TestFireLoadDensity()
