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
            q_f_k: float,
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
            q_f_k: float,
            m: float,
            delta_q_1: float,
            delta_q_2: float,
            delta_n: float,
            **__
    ) -> dict:
        """The design value of the fire load, Clause E.1 (3), page 46.

        :param q_f_k:       [MJ/m2],    is the characteristic fuel load density
        :type q_f_k:        float
        :param m:           [-],        is the combustion factor (see E.3)
        :type m:            float
        :param delta_q_1:   [-],        is a factor taking into account the fire activation risk due to the size of the
                                        compartment (see Table E.1)
        :type delta_q_1:    float
        :param delta_q_2:   [-],        is a factor taking into account the fire activation risk due to the type of
                                        occupancy (see Table E.1)
        :type delta_q_2:    float
        :param delta_n:     [-],        is a factor taking into account the different active fire fighting measures i 
                                        (sprinkler, detection, automatic alarm transmission, firemen ...). These active 
                                        measures are generally imposed for life safety reason (see Table E.2 and 
                                        clauses(4) and (5))
        :type delta_n:      float
        :return:            q_fd and latex math expression
        :rtype:             dict
        """

        q_f_d = q_f_k * m * delta_q_1 * delta_q_2 * delta_n

        _latex = [
            f'q_{{fd}}=q_{{fk}}\\cdot m\\cdot \\delta_{{q1}}\\cdot \\delta_{{q2}}\\cdot \\delta_n',
            f'q_{{fd}}={q_f_k:.2f}\\cdot {m:.2f}\\cdot \\{delta_q_1:.2f}\\cdot \\{delta_q_2:.2f}\\cdot \\{delta_n:.2f}',
            f'q_{{fd}}={q_f_d:.2f}',
        ]
        return dict(q_f_d=q_f_d, _latex=_latex)

    @staticmethod
    def table_e1_delta_q1(A_f: float, **__) -> dict:
        """A factor taking into account the fire activation risk due to the size of the compartment (see Table E.1)

        :param A_f: [m2]    Compartment floor area
        :return:            delta_q1, is the factor taking into account of fire activation risk due to compartment size; and latex math expression
        """
        if A_f <= 25:
            delta_q_1 = 1.1
        elif A_f <= 250:
            delta_q_1 = 1.5
        elif A_f <= 2500:
            delta_q_1 = 1.9
        elif A_f <= 5000:
            delta_q_1 = 2
        elif A_f <= 10000:
            delta_q_1 = 2.13
        else:
            raise ValueError(f'Maximum floor area 10,000 m² exceeded {A_f}')

        _latex = [f'\\delta_{{q1}}={delta_q_1:.2f}']

        return dict(delta_q_1=delta_q_1, _latex=_latex)

    @staticmethod
    def table_e1_delta_q2(
            occupancy: Union[str, int],
            **__,
    ) -> dict:
        if isinstance(occupancy, str):
            occupancy = occupancy.lower().strip()

        if occupancy == 1 or occupancy in ['artgallery', 'musem', 'swimming pool']:
            delta_q_2 = 0.78
        elif occupancy == 2 or occupancy in ['office', 'residence', 'hotel', 'paper industry']:
            delta_q_2 = 1.0
        elif occupancy == 3 or occupancy in ['manufactory for machinery & engines']:
            delta_q_2 = 1.22
        elif occupancy == 4 or occupancy in ['chemical laboratory', 'painting workshop']:
            delta_q_2 = 1.44
        elif occupancy == 5 or occupancy in ['manufactory of fireworks or paints']:
            delta_q_2 = 1.66
        else:
            raise ValueError(f'Unknown occupancy "{occupancy}"')

        _latex = [
            f'\\delta_{{q2}}={delta_q_2:.2f}'
        ]

        return dict(delta_q_2=delta_q_2, _latex=_latex)

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

        delta_n_1 = 0.61 if is_sprinklered else 1

        if is_sprinklered and sprinkler_independent_water_supplies == 0:
            delta_n_2 = 1.0
        elif is_sprinklered and sprinkler_independent_water_supplies == 1:
            delta_n_2 = 0.87
        elif is_sprinklered and sprinkler_independent_water_supplies == 2:
            delta_n_2 = 0.7
        else:
            delta_n_2 = 1

        delta_n_3 = 0.87 if is_detection_by_heat else 1
        delta_n_4 = 0.73 if is_detection_by_smoke else 1
        delta_n_5 = 0.87 if is_automatic_transmission_to_fire_brigade else 1
        delta_n_6 = 0.61 if is_onsite_fire_brigade else 1
        delta_n_7 = 0.78 if is_offsite_fire_brigade else 1
        delta_n_8 = 1 if is_safe_access_routes else 1.5
        delta_n_9 = 1 if is_fire_fighting_devices else 1.5
        delta_n_10 = 1 if is_smoke_exhaust_system else 1.5

        delta_n = \
            delta_n_1 * delta_n_2 * delta_n_3 * delta_n_4 * delta_n_5 * \
            delta_n_6 * delta_n_7 * delta_n_8 * delta_n_9 * delta_n_10

        _latex = [
            f'\\delta_n=\\sum_{{i=1}}^{{10}}\\delta_{{ni}}',
            f'\\delta_n={delta_n_1:.2f}+{delta_n_2:.2f}+{delta_n_3:.2f}+{delta_n_4:.2f}+'
            f'{delta_n_5:.2f}+{delta_n_6:.2f}+{delta_n_7:.2f}+{delta_n_8:.2f}+{delta_n_9:.2f}+{delta_n_10:.2f}',
            f'\\delta_n={delta_n:.2f}'
        ]

        return dict(delta_n=delta_n, _latex=_latex)




if __name__ == '__main__':
    _test_1()
