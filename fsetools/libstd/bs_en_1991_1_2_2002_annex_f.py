class EquivalenceOfTimeExposure:
    """
    Equivalence of time exposure in accordance with Annex F in BS EN 1991-1-2:2002.

    The following approach may be used where the design of members is based on tabulated data or other simplified
    rules, related to the standard fire exposure.

    NOTE The method given in this annex is material dependent. It is not applicable to composite steel and concrete or
    timber constructions.

    If fire load densities are specified without specific consideration of the combustion behaviour (see annex E),
    then this approach should be limited to fire compartments with mainly cellulosic type fire loads.
    """

    def __init__(self):
        pass

    def calculate(
            self,
            q_f_d: float, k_b: float, k_c: float, H: float, A_f: float, A_t: float, A_v: float, A_h: float, O: float,
    ):
        kwargs = locals().copy()
        kwargs.pop('self')
        kwargs.update(self.clause_5_ventilation_factor(**kwargs))
        kwargs.update(self.clause_3_equivalent_time(**kwargs))
        return kwargs

    @staticmethod
    def clause_3_equivalent_time(q_f_d: float, k_b: float, w_f: float, k_c: float, **__):
        """
        The equivalent time of standard fire exposure.

        :param q_f_d:   [MJ/m2] is the design fire load density according to annex E
        :param k_b:     [-]     is the conversion factor according to (4)
        :param w_f:     [-]     is the ventilation factor according to (5)
        :param k_c:     [-]     is the correction factor function of the material composing structural cross-sections
                                and defined in Table F.1
        :param __:              Not used
        :return t_e_d:  [min]   is the equivalent time of standard fire exposure
        """
        t_e_d = (q_f_d * k_b * w_f) * k_c
        _latex = [
            f't_{{e,d}} = \\left( q_{{f,d}} \\cdot k_b \\cdot w_f \\right) \\cdot k_c',
            f't_{{e,d}} = {t_e_d:.2f} \\ \\left[ min \\right]'
        ]
        return dict(t_e_d=t_e_d, _latex=_latex)

    @staticmethod
    def clause_5_ventilation_factor(H: float, A_f: float, A_t: float, A_v: float, A_h: float, O: float, **__):
        """
        The ventilation factor.

        :param H:   [m]     is the height of the fire compartment
        :param A_f: [m2]    is the floor area of the compartment
        :param A_v: [m2]    is the area of vertical openings in the facade
        :param A_h: [m2]    is the area of horizontal openings in the roof
        :param __:          Not used
        :return w_f:        is the ventilation factor
        """
        _latex = list()

        alpha_v = A_v / A_f
        alpha_h = A_h / A_f
        _latex.append([f'\\alpha_v = \\frac{{A_v}}{{A_f}} = \\frac{A_v}{A_f} = {alpha_v}'])
        _latex.append([f'\\alpha_h = \\frac{{A_h}}{{A_f}} = \\frac{A_h}{A_f} = {alpha_h}'])

        b_v = 12.5 * (1 + 10 * alpha_v - alpha_v ** 2)
        assert b_v >= 10.0
        _latex.append([
            f'b_v = 12.5 \\times \\left( 1 + 10 * \\alpha_v - \\alpha_v ** 2 \\right) = 12.5 \\times \\left( 1 + 10 * {alpha_v} - {alpha_v} ** 2 \\right) = {b_v}'
        ])

        _latex.append([
            f'w_f = \n'
            f'\\begin{{dcases}}\n'
            f'  \\dfrac{{6.0}}{{H}}^{{0.3}} \\times \\left( 0.62 + 90 \\times \\dfrac{{\\left( 0.4 - \\alpha_v \\right) ^ 4}}{{1 + b_v \\times \\alpha_h}} \\right),    & \\text{{if }}A_f\\geq100\\text{{ or openings in the roof}} \\ \\left[{A_h > 0 or A_f >= 100}\\right]\\\\\n'
            f'  O ^ {{-0.5}} \\times \\dfrac{{A_f}}{{A_t}},                                                                                                             & \\text{{if }}A_f<100\\text{{ and no openings in the roof}} \\ \\left[{A_h < 0 and A_f < 100}\\right]\n'
            f'\\end{{dcases}}',
        ])
        if A_h > 0 or A_f > 100:
            w_f = (6.0 / H) ** 0.3 * (0.62 + 90 * (0.4 - alpha_v) ** 4 / (1 + b_v * alpha_h))
            assert w_f >= 0.5
            _latex.append([
                f'w_f = \\frac{{6.0}}{H}^{{0.3}} \\times \\left( 0.62 + 90 \\times \\frac{{\\left( 0.4 - {alpha_v} \\right) ^ 4}}{{1 + {b_v} \\times {alpha_h}}} \\right)',
                f'w_f = {w_f}',
            ])
        else:
            w_f = O ** - 0.5 * A_f / A_t
            _latex.append([
                f'w_f = {O} ^ {{-0.5}} \\times \\frac{A_f}{A_t}',
                f'w_f = {w_f}',
            ])

        return dict(w_f=w_f, _latex=_latex)


class TestEquivalenceOfTimeExposure(EquivalenceOfTimeExposure):
    def __init__(self):
        super().__init__()
        self.test_1()

    def test_1(self):
        from fsetools.libstd.bs_en_1991_1_2_2002_annex_e import FireLoadDensity
        q_fd_cls = FireLoadDensity()
        q_fd = q_fd_cls.calculate(
            A_f=1500,
            q_f_k=870,
            m=0.8,
            occupancy=FireLoadDensity.OCCUPANCY_OFFICE,
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
        )['q_fd']

        res = self.calculate(
            q_f_d=q_fd,
            k_b=0.07,
            k_c=1.0,
            H=3,
            A_f=1500,
            A_t=(30 * 50 + 50 * 3 + 3 * 30) * 2,
            A_v=15 * 3,
            A_h=0,
            O=(15 * 3) * (3 ** 0.5) / ((30 * 50 + 50 * 3 + 3 * 30) * 2),
        )

        print(res)


if __name__ == '__main__':
    TestEquivalenceOfTimeExposure()
