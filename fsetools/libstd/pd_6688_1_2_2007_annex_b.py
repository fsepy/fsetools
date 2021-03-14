# -*- coding: utf-8 -*-
import numpy as np


class EquivalentTimeOfFireExposure:
    """
    Equivalent time of exposure calculation in accordance with Annex B in PD 6688-1-2:2007. Static methods signatures are '{equation_no}_{short_name}'.

    Example:
        >>> teq_cls = EquivalentTimeOfFireExposure()
        >>> teq = teq_cls.calculate(
        >>>     q_f_k=900,
        >>>     m=1,
        >>>     delta_1=0.61,
        >>>     k_b=0.09,
        >>>     A_f=856.5,
        >>>     A_t=0,
        >>>     H=4,
        >>>     A_vh=0,
        >>>     A_vv=235.2,
        >>>     O=0,
        >>>     occupancy=EquivalentTimeOfFireExposure.OCCUPANCY_RESIDENTIAL_DWELLING,
        >>>     height=5
        >>> )
    """

    OCCUPANCY_RESIDENTIAL_DWELLING = 0
    OCCUPANCY_RESIDENTIAL_INSTITUTIONAL = 1
    OCCUPANCY_RESIDENTIAL_OTHER = 2
    OCCUPANCY_OFFICE = 4
    OCCUPANCY_RETAIL = 5
    OCCUPANCY_ASSEMBLY_HIGH = 6
    OCCUPANCY_ASSEMBLY_MED = 7
    OCCUPANCY_ASSEMBLY_LOW = 8
    OCCUPANCY_INDUSTRIAL_HIGH = 9
    OCCUPANCY_INDUSTRIAL_LOW = 10

    def __init__(self):
        # Derived values
        self.__t_e_d: float = np.nan
        self.__q_f_d: float = np.nan
        self.__w_f: float = np.nan

    def calculate(
            self,
            q_f_k: float, m: float, delta_1: float, k_b: float,
            A_f: float, A_t: float, H: float, A_vh: float, A_vv: float, O: float,
            occupancy: int, height: float
    ) -> float:
        """
        :param q_f_k:       [MJ/m2]     is the characteristic fire load density per unit floor area
        :param m:           [-]         is the combustion factor
        :param delta_1:     [-]         is a factor of 0.61 that can be applied to take into account sprinklers if installed for life safety purposes
        :param k_b:         [min*m2/MJ] is the conversion factor according to B.3
        :param A_f:         [m2]        is the floor area of the compartment
        :param A_t:         [m2]        is the total area of the compartment (including openings)
        :param H:           [m]         is the height of compartment
        :param A_vh:        [m2]        is the horizontal openings in the roof
        :param A_vv:        [m2]        is the vertical openings in the facade
        :param O:           [m**0.5]    is the opening factor of a compartment
        :param occupancy:   [-]         occupancy type
        :param height:      [m]         is the building height
        """

        self.q_f_d = self.a_1_fire_load(q_f_k=q_f_k, m=m, delta_1=delta_1)

        if A_f < 100. and A_vh == 0.:
            self.w_f = self.b_3_ventilation_factor(O=O, A_f=A_f, A_t=A_t)
        else:
            self.w_f = self.b_2_ventilation_factor(A_vv=A_vv, A_vh=A_vh, A_f=A_f, H=H)

        risk_factor = self.risk_factor_associated_with_height(occupancy=occupancy, height=height)

        self.t_e_d = self.b_1_equivalent_time_exposure(q_f_d=self.q_f_d, k_b=k_b, w_f=self.w_f) * risk_factor

        return self.t_e_d

    @staticmethod
    def b_1_equivalent_time_exposure(q_f_d: float, k_b: float, w_f: float):
        """
        The equivalent time of standard fire exposure in accordance with section B.2 PD 6688-1-2:2007

        :param q_f_d:   [MJ/m2]     is the design fire load density according to the UK guidance set out in Annex A
        :param k_b:     [min*m2/MJ] is the conversion factor according to B.3
        :param w_f:     [m**0.5]    is the ventilation factor according to B.4
        :return t_e_d:  [min]       is the equivalent time of standard fire exposure
        """

        t_e_d = q_f_d * k_b * w_f

        return t_e_d

    @staticmethod
    def a_1_fire_load(q_f_k: float, m: float, delta_1: float) -> float:
        """
        The design value of the fire load `q_f_d`.

        :param q_f_k:   [MJ/m2] is the characteristic fire load density per unit floor area
        :param m:       [-]     is the combustion factor
        :param delta_1: [-]     is a factor of 0.61 that can be applied to take into account sprinklers if installed for life safety purposes
        :return q_f_d:  [MJ/m2] is the design fire load
        """

        try:
            assert isinstance(q_f_k, (float, int)) and q_f_k > 0.
        except:
            raise ValueError('q_f_k should be numerical value greater than 0')

        q_f_d = q_f_k * m * delta_1

        return q_f_d

    @staticmethod
    def b_2_ventilation_factor(A_vv: float, A_vh: float, A_f: float, H: float) -> float:
        """
        Ventilation factor for large compartment or small compartment with roof openings.

        :param A_vv:    [m2]    is the vertical openings in the facade
        :param A_vh:    [m2]    is the horizontal openings in the roof
        :param A_f:     [m2]    is the floor area of the compartment
        :param H:       [m]     is the height of compartment
        :return w_f:    [-]     is the ventilation factor
        """

        if A_f < 100. and A_vh == 0.:
            raise ValueError(f'Equation B.2 is applicable for large compartment or small compartment with horizontal openings in the roof')

        # Vertical opening factor
        alpha_v = min([max([A_vv / A_f, 0.025]), 0.25])

        # horizontal opening factor
        alpha_h = A_vh / A_f

        # just a factor
        b_v = 12.5 * (1 + 10 * alpha_v - alpha_v ** 2)
        if b_v < 10:
            raise ValueError(f'b_v should be greater or equal to 10, b_v={b_v}')

        # total ventilation factor
        w_f = ((6 / H) ** 0.3) * ((0.62 + 90 * (0.4 - alpha_v) ** 4) / (1 + b_v * alpha_h))

        return w_f

    @staticmethod
    def b_3_ventilation_factor(O: float, A_f: float, A_t: float) -> float:
        """
        Ventilation factor for small compartment without roof openings.

        :param O:       [m**0.5]    is the opening factor according to Annex A
        :param A_f:     [m2]        is the floor area of the compartment
        :param A_t:     [m2]        is the total area of the compartment (including openings)
        :return w_f:    [-]         is the ventilation factor
        """

        w_f = O ** -0.5 * A_f / A_t

        return w_f

    @staticmethod
    def b_4_verify(t_e_d: float, t_fi_d: float) -> bool:
        """
        Verify calculated equivalent exposure against EN 1992-1-2, 1993-1-2, 1994-1-2, 1995-1-2 to 1996-1-2 and 1991-1-2

        :param t_e_d:
        :param t_fi_d:
        :return:
        """
        return t_e_d < t_fi_d

    @staticmethod
    def opening_factor(A_v: float, h_eq: float, A_t: float):
        """
        Opening factor in accordance with EN 1991-1-2.

        :param A_v:     [m2]        is the opening area of a compartment
        :param h_eq:    [m]         is the weighted height of all opening areas
        :param A_t:     [m2]        is the total area of a compartment
        :return O:      [m**0.5]    is the opening factor of a compartment
        """

        O = A_v * (h_eq ** 0.5) / A_t

        return O

    def risk_factor_associated_with_height(self, occupancy: int, height: float):
        def helper_function_1(height_):
            """
            Suitable for Residential (dwelling) and Residential (other).

            :param height_:     [m] is the building height
            :return:                risk factor
            """

            if height_ <= 5:
                return 1
            elif height_ <= 18:
                return 1.35
            elif height_ <= 30:
                return 2.0
            elif height_ > 30:
                return 2.65

        def helper_function_2(height_):
            """
            Suitable for Residential (institutional).

            :param height_:     [m] is the building height
            :return:                risk factor
            """
            if height_ <= 5:
                return 1.35
            elif height_ <= 18:
                return 2.0
            elif height_ <= 30:
                return 2.65
            elif height_ > 30:
                return 3.3

        def helper_function_3(height_):
            """
            Suitable for Office, Retail, Assembly (high), Assembly (med), Assembly (low), Industrial (high) and Industrial (low).

            :param height_:     [m] is the building height
            :return:                risk factor
            """
            if height_ <= 5:
                return 0.65
            elif height_ <= 18:
                return 1.0
            elif height_ <= 30:
                return 1.35
            elif height_ > 30:
                return 2.0

        if occupancy == self.OCCUPANCY_RESIDENTIAL_DWELLING:
            return helper_function_1(height)
        elif occupancy == self.OCCUPANCY_RESIDENTIAL_INSTITUTIONAL:
            return helper_function_2(height)
        elif occupancy == self.OCCUPANCY_RESIDENTIAL_OTHER:
            return helper_function_1(height)
        elif occupancy == self.OCCUPANCY_OFFICE:
            return helper_function_3(height)
        elif occupancy == self.OCCUPANCY_RETAIL:
            return helper_function_3(height)
        elif occupancy == self.OCCUPANCY_ASSEMBLY_HIGH:
            return helper_function_3(height)
        elif occupancy == self.OCCUPANCY_ASSEMBLY_MED:
            return helper_function_3(height)
        elif occupancy == self.OCCUPANCY_ASSEMBLY_LOW:
            return helper_function_3(height)
        elif occupancy == self.OCCUPANCY_INDUSTRIAL_HIGH:
            return helper_function_3(height)
        elif occupancy == self.OCCUPANCY_INDUSTRIAL_LOW:
            return helper_function_3(height)
        else:
            raise ValueError(f'Unidentified occupancy type, {occupancy}, check class property beginning with OCCUPANCY_ for available occupancy types')

    @property
    def t_e_q(self) -> float:
        return self.__t_e_d

    @property
    def q_f_d(self) -> float:
        return self.__q_f_d

    @property
    def w_f(self) -> float:
        return self.__w_f

    @t_e_q.setter
    def t_e_q(self, v: float):
        self.__t_e_d = v

    @q_f_d.setter
    def q_f_d(self, v: float):
        self.__q_f_d = v

    @w_f.setter
    def w_f(self, v: float):
        self.__w_f = v

    def tests(self):
        self.__test_1()

    def __test_1(self):
        pre_calculated = 37.13907
        calculated = self.calculate(
            q_f_k=900,
            m=1,
            delta_1=0.61,
            k_b=0.09,
            A_f=856.5,
            A_t=0,
            H=4,
            A_vh=0,
            A_vv=235.2,
            O=0,
            occupancy=self.OCCUPANCY_RESIDENTIAL_DWELLING,
            height=5
        )
        print(f'Test 1 pre_calculated = {pre_calculated} and calculated {calculated}')
        assert abs(pre_calculated - calculated) < 1e-4


if __name__ == "__main__":
    EquivalentTimeOfFireExposure().tests()
