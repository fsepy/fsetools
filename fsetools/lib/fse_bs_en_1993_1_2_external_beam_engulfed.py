from math import sqrt

from pylatex import NoEscape, Section, Subsection

from fsetools.etc.latex import make_alginat_equations, make_summary_table
from fsetools.lib.fse_latex_report_template import ReportBase
from fsetools.libstd.bs_en_1991_1_2_2002_annex_b import clause_b_4_1_10_T_z, clause_b_4_2_9_T_z, clause_b_4_1_12_alpha_c, clause_b_4_2_11_alpha_c
from fsetools.libstd.bs_en_1993_1_2_2005_annex_b import *


class ExternalSteelTemperatureEngulfedBeam(ReportBase):
    def __init__(
            self,
            is_forced_draught: bool,
            **kwargs
    ):
        super().__init__()
        # derived values below

        input_kwargs = locals()
        input_kwargs.pop('self')
        input_kwargs.pop('kwargs')
        input_kwargs.update(**kwargs)
        self.input_kwargs = input_kwargs
        self.output_kwargs = self.__calculation(**input_kwargs)

    def make_latex(self):
        doc = self.make_document_template(**self.input_kwargs)
        for i in self.make_latex_sections():
            doc.append(i)
        return doc

    def make_latex_sections(self, section_title: str = None) -> list:
        sections = list()
        if section_title:
            sections.append(Section(title=f'{section_title}'))
        else:
            sections.append(Section(title='Heat transfer to external steel beam'))
        sections.append(self.section_1_introduction())
        sections.append(self.section_2_inputs(self.input_kwargs))
        sections.append(self.section_3_calculation(self.output_kwargs))
        sections.append(self.section_4_summary(self.output_kwargs))
        return sections

    @staticmethod
    def section_1_introduction():
        sec = Subsection(title='Introduction')

        sec.append(NoEscape(
            'Calculation documented herein follows Annex B in '
            '"Eurocode 3: Design of steel structures — Part 1-2: General rules — Structural fire design" '
            '(BS EN 1991-1-3). '
            'This method allows the determination of the average temperature of an external steel member.\\par'))

        sec.append(NoEscape(
            'The determination of the temperature of the compartment fire, the dimensions and temperature of the '
            'flames projecting from the openings, and the radiation and convection parameters should be performed '
            'according to annex B of BS EN 1991-1-2.\\par'))

        sec.append(NoEscape(
            'Units, symbols and abbreviations are consistent with BS EN 1991-1-3 unless stated.\\par'))

        sec.append(NoEscape(
            'Numerical values shown in this document are rounded as appropriate for readability, however, calculations '
            'are carried out based on the actual values.\\par'
        ))

        sec.append(NoEscape(
            'This assessment is specific to an external steel beam which is fully or partially engulfed in flame '
            'in accordance with Clause B.5 in BS EN 1993-1-2.'
        ))

        return sec

    @staticmethod
    def section_2_inputs(input_kwargs: dict):
        sec = Subsection(title='Inputs')
        symbols = [
            # user defined parameters
            'w_t', 'h_eq', 'd_1', 'd_2',
            # user defined parameters specific to BS EN 1993-1-2 Annex B, beam calcs
            'lambda_4', 'd_aw', 'C_1', 'C_2', 'C_3', 'C_4',
            # derived parameters, i.e. from BS EN 1991-1-2 Annex B
            'L_H', 'L_L', 'T_f', 'T_o', 'T_z_1', 'T_z_2', 'T_z', 'alpha', 'w_f',
        ]
        sec.append(make_summary_table(
            symbols=symbols,
            units=UNITS,
            descriptions=DESCRIPTIONS,
            values=input_kwargs
        ))
        return sec

    @staticmethod
    def section_3_calculation(output_kwargs):
        latex_equation_header = output_kwargs['_latex_equation_header']
        latex_equation_content = output_kwargs['_latex_equation_content']
        sec = Subsection(title='Calculation')
        for i in range(len(latex_equation_header)):
            sec.append(NoEscape(latex_equation_header[i]))
            sec.append(make_alginat_equations(latex_equation_content[i]))
        return sec

    @staticmethod
    def section_4_summary(output_kwargs: dict):
        sec = Subsection(title='Summary')
        sec.append('Results are summarised below.')
        symbols = [
            'I_z_1', 'I_z_2', 'I_z_3', 'I_z_4', 'I_z',
            'I_f_1', 'I_f_2', 'I_f_3', 'I_f_4', 'I_f',
            'T_m_1', 'T_m_2', 'T_m_3', 'T_m_4', 'T_m'
        ]
        sec.append(make_summary_table(
            symbols=symbols,
            units=UNITS,
            descriptions=DESCRIPTIONS,
            values=output_kwargs
        ))
        return sec

    @staticmethod
    def __calculation(**input_kwargs):

        # ==============================================
        # Helper functions not defined in BS EN 1993-1-2
        # ==============================================
        def helper_L_x(
                d_1: float,
                d_2: float,
                d_aw: float,
                h_eq: float,
                L_L: float,
                L_H: float,
                lambda_4: float,
                *_, **__,
        ) -> dict:
            if is_forced_draught is False:
                if d_aw + 0.5 * d_2 > 0:
                    # if the location L_x_1 is engulfed in flame
                    L_x = sqrt(((2. / 3. * h_eq) / (2 * L_H) * (lambda_4 + 0.5 * d_1)) ** 2 + (lambda_4 + 0.5 * d_1) ** 2) + (d_aw + 0.5 * d_2)
                else:
                    # if the location L_x_1 is outside of the flame
                    L_x = sqrt(((2 / 3 * h_eq) / (2 * L_H) * (lambda_4 + 0.5 * d_1)) ** 2 + (lambda_4 + 0.5 * d_1) ** 2)
            elif is_forced_draught is True:
                L_x = sqrt((lambda_4 + 0.5 * d_1) ** 2 + (L_H / L_L * (lambda_4 + 0.5 * d_1) ** 2))
            else:
                raise ValueError

            return dict(L_x=L_x)

        def helper_L_x_1(
                h_eq: float,
                L_L: float,
                L_H: float,
                d_1: float,
                d_aw: float,
                lambda_4,
                is_forced_draught: bool,
                *_, **__
        ) -> dict:
            """
            To calculate `L_x_1`, the length along the flame axis between the beam's top to the window opening under `forced draught` or `no forced draught` conditions.

            Nota bene this function does not check for wither L_x_1 is within the L_f range (i.e. whether the location is within flame).

            :param h_eq: [m], window height (weighted average)
            :param L_L: [m], flame vertical projection
            :param L_H: [m], flame horizontal projection
            :param d_1: [m], beam horizontal dimension, e.g. the direction parallel to ground or perpendicular to window opening
            :param d_aw: [m], vertical distance between the beam's bottom to the top of the window opening
            :param lambda_4: [m], horizontal distance between the beam to the window opening
            :return: a dict containing `L_x_1`
            """

            if is_forced_draught is True:
                L_x_1 = sqrt((lambda_4 + 0.5 * d_1) ** 2 + (L_H / L_L * (lambda_4 + 0.5 * d_1) ** 2))
            elif is_forced_draught is False:
                if d_aw > 0.:
                    # if the location L_x_1 is engulfed in flame
                    L_x_1 = sqrt(((2. / 3. * h_eq) / (2 * L_H) * (lambda_4 + 0.5 * d_1)) ** 2 + (lambda_4 + 0.5 * d_1) ** 2) + d_aw
                elif d_aw <= 0:
                    # if the location L_x_1 is outside of the flame
                    L_x_1 = sqrt(((2 / 3 * h_eq) / (2 * L_H) * (lambda_4 + 0.5 * d_1)) ** 2 + (lambda_4 + 0.5 * d_1) ** 2)
                else:
                    raise ValueError
            else:
                raise ValueError

            return dict(L_x_1=L_x_1)

        def helper_L_x_2(
                h_eq: float,
                L_L: float,
                L_H: float,
                d_1: float,
                d_2: float,
                d_aw: float,
                lambda_4,
                is_forced_draught: bool,
                *_, **__
        ) -> dict:
            """
            To calculate `L_x_2`, the length along the flame axis between the beam's top to the window opening under `forced draught` or `no forced draught` conditions.

            Nota bene this function does not check for wither L_x_1 is within the L_f range (i.e. whether the location is within flame).

            :param h_eq: [m], window height (weighted average)
            :param L_L: [m], flame vertical projection
            :param L_H: [m], flame horizontal projection
            :param d_1: [m], beam horizontal dimension, e.g. the direction perpendicular to window opening
            :param d_2: [m], beam vertical dimension, e.g. the direction parallel to window opening
            :param d_aw: [m], vertical distance between the beam's bottom to the top of the window opening
            :param lambda_4: [m], horizontal distance between the beam to the window opening
            :return: a dict containing `L_x_2`
            """

            if is_forced_draught is True:
                L_x_2 = helper_L_x_1(h_eq=h_eq, L_L=L_L, L_H=L_H, d_1=d_1, d_aw=d_aw, lambda_4=lambda_4, is_forced_draught=is_forced_draught)['L_x_1']
            elif is_forced_draught is False:
                L_x_2 = helper_L_x_1(h_eq=h_eq, L_L=L_L, L_H=L_H, d_1=d_1, d_aw=d_aw, lambda_4=lambda_4, is_forced_draught=is_forced_draught)['L_x_1'] + d_2
            else:
                raise ValueError

            return dict(L_x_2=L_x_2)

        # Work out if flame above the beam's top surface
        def helper_check_if_fully_engulfed_in_flame(
                L_L: float,
                d_aw: float,
                d_2: float,
                *_, **__
        ):
            """
            To check whether a beam is fully engulfed within external flame.

            :param L_L: [m], flame vertical projection above above the window opening top edge
            :param d_aw: [m], vertical distance between beam bottom and window opening top edge
            :param d_2: [m], beam's vertical dimension
            :return: `True` if fully engulfed and `False` otherwise.
            """

            if L_L > (d_aw + d_2):
                return True
            else:
                return False

        # =================================
        # Main calculation procedure starts
        # =================================
        _latex_equation_header, _latex_equation_content = list(), list()

        # Calculate lambda_1
        if 'lambda_1' not in input_kwargs:
            input_kwargs.update(clause_b_5_1_1_2_lambda_1(**input_kwargs))
            _latex_equation_header.append('Clause B.5.1.1 (2), the flame thickness $\\lambda_1$ is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate lambda_2
        if 'lambda_2' not in input_kwargs:
            input_kwargs.update(clause_b_5_1_1_2_lambda_2(**input_kwargs))
            _latex_equation_header.append('Clause B.5.1.1 (2), the flame thickness $\\lambda_2$ is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate lambda_3
        if 'lambda_3' not in input_kwargs:
            input_kwargs.update(clause_b_5_1_1_2_lambda_3(**input_kwargs))
            _latex_equation_header.append('Clause B.5.1.1 (2), the flame thickness $\\lambda_3$ is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate L_x_1 (only used to calculate T_z_1)
        if 'L_x_1' not in input_kwargs and 'T_z_1' not in input_kwargs:
            input_kwargs.update(helper_L_x_1(**input_kwargs))

        # Calculate T_z_1
        if 'T_z_1' not in input_kwargs:
            # `helper_L_x_1` returns a dict containing key `L_x_1` but the variable name `L_x` is used here.
            __ = clause_b_4_1_10_T_z(L_x=input_kwargs['L_x_1'], T_w=input_kwargs['T_o'], **input_kwargs)

            if input_kwargs['is_forced_draught'] is False:
                __['T_z_1'] = __.pop('T_z')
                input_kwargs.update(__)
                _latex_equation_header.append(
                    'BS EN 1991-1-2 Clause B.4.1 (10), the flame temperature along the axis at $L_{x,1}$ is:')
                _latex_equation_content.append(input_kwargs['_latex'])
            elif input_kwargs['is_forced_draught'] is True:
                # for forced draught condition, `L_x_1` and `L_x_2` are the same.
                __['T_z_1'] = __.pop('T_z')
                __['T_z_2'] = __['T_z_1']
                input_kwargs.update(__)
                _latex_equation_header.append(
                    'BS EN 1991-1-2 Clause B.4.1 (10), the flame temperature along the axis at $L_{x,1}$ and $L_{x,2}$ is:')
                _latex_equation_content.append(input_kwargs['_latex'])
            else:
                raise ValueError(f'`is_forced_draught` should be boolean, {input_kwargs["is_forced_draught"]}')

        # Calculate L_x_2 (only used to calculate T_z_2)
        if 'L_x_2' not in input_kwargs and 'T_z_2' not in input_kwargs:
            input_kwargs.update(helper_L_x_2(**input_kwargs))

        # Calculate T_z_2
        if 'T_z_2' not in input_kwargs:
            # `helper_L_x_1` returns a dict containing key `L_x_1` but the variable name `L_x` is used here.
            if input_kwargs['is_forced_draught'] is False:
                __ = clause_b_4_1_10_T_z(L_x=input_kwargs['L_x_2'], T_w=input_kwargs['T_o'], **input_kwargs)
                __['T_z_2'] = __.pop('T_z')
                input_kwargs.update(__)
                _latex_equation_header.append(
                    'BS EN 1991-1-2 Clause B.4.1 (10), the flame temperature along the axis at $L_{x,2}$ is:')
                _latex_equation_content.append(input_kwargs['_latex'])
            elif input_kwargs['is_forced_draught'] is True:
                pass
            else:
                raise ValueError(f'`is_forced_draught` should be boolean, {input_kwargs["is_forced_draught"]}')

        # Calculate phi_f_1 ... phi_f_4
        if not all([i in input_kwargs for i in ['phi_z_1', 'phi_z_2', 'phi_z_3', 'phi_z_4']]):
            input_kwargs.update(clause_b_1_4_1_phi_f_i_beam(**input_kwargs))
            _latex_equation_header.append('Clause B.1.4 (1), the radiative heat flux from an opening for each of the faces 1, 2, 3 and 4 of the beam is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate epsilon_z_1 ... epsilon_z_4
        if not all([i in input_kwargs for i in ['epsilon_z_1', 'epsilon_z_2', 'epsilon_z_3', 'epsilon_z_4']]):
            input_kwargs.update(clause_b_5_2_1_epsilon_z_i(**input_kwargs))
            _latex_equation_header.append(
                'Clause B.5.2 (1), the emissivity of the flames for each of the faces 1, 2, 3 and 4 of the beam are:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate I_z_1 ... I_z_4
        if not all([i in input_kwargs for i in ['I_z_1', 'I_z_2', 'I_z_3', 'I_z_4']]):
            is_forced_draught = input_kwargs['is_forced_draught']
            is_immediately_next_to_facade = input_kwargs['lambda_4'] <= 0.
            is_flame_above_steel = helper_check_if_fully_engulfed_in_flame(**input_kwargs)

            if is_forced_draught is False:  # for no forced draught conditions

                if is_flame_above_steel is True and is_immediately_next_to_facade is False:  # for beam fully engulfed and located away from the facade, i.e. `lambda_4` > 0
                    input_kwargs.update(clause_b_5_1_2_2_I_z_i(**input_kwargs))
                    _latex_equation_header.append(
                        'Clause B.5.1.2 (2), the emissivity of the flames for each of the faces 1, 2, 3 and 4 of the column are:')
                    _latex_equation_content.append(input_kwargs['_latex'])

                elif is_flame_above_steel is True and is_immediately_next_to_facade is True:  # for beam fully engulfed and located immediately next to facade, i.e. `lambda_4`==0
                    C_4 = input_kwargs['C_4']  # override C_4 to zero according the Clause B.5.1.2 (3)
                    input_kwargs['C_4'] = 0
                    input_kwargs.update(clause_b_5_1_2_2_I_z_i(**input_kwargs))
                    input_kwargs['C_4'] = C_4  # revert C_4 to original input
                    _latex_equation_header.append('Clause B.5.1.2 (3), the emissivity of the flames for each of the faces 1, 2, 3 and 4 of the column are ($C_4$ is set to 0):')
                    _latex_equation_content.append(input_kwargs['_latex'])

                elif is_flame_above_steel is False and is_immediately_next_to_facade is False:  # for beam partially engulfed and located away to facade
                    h_z = input_kwargs['L_L'] - input_kwargs['d_aw'] - input_kwargs['d_2']
                    input_kwargs.update(clause_b_5_1_2_4_I_z_i(h_z=h_z, **input_kwargs))
                    _latex_equation_header.append('Clause B.5.1.2 (4), the emissivity of the flames for each of the faces 1, 2, 3 and 4 of the column are:')
                    _latex_equation_content.append(input_kwargs['_latex'])

                elif is_flame_above_steel is False and is_immediately_next_to_facade is True:  # for beam partially engulfed and located next immediately to facade
                    C_4 = input_kwargs['C_4']  # override C_4 to zero according the Clause B.5.1.2 (3)
                    input_kwargs['C_4'] = 0
                    input_kwargs.update(clause_b_5_1_2_4_I_z_i(**input_kwargs))
                    input_kwargs['C_4'] = C_4  # revert C_4 to original input
                    _latex_equation_header.append('Clause B.5.1.2 (4), the emissivity of the flames for each of the faces 1, 2, 3 and 4 of the column are ($C_4$ is set to 0):')

                else:
                    raise ValueError

            elif is_forced_draught is True:  # for forced draught conditions
                if is_immediately_next_to_facade is False:  # for beam located away from the facade, i.e. `d_1` > 0
                    input_kwargs.update(clause_b_5_1_3_2_I_z_i(**input_kwargs))
                    _latex_equation_header.append(
                        'Clause B.5.1.3 (2), the emissivity of the flames for each of the faces 1, 2, 3 and 4 of the column are:')
                    _latex_equation_content.append(input_kwargs['_latex'])
                else:
                    raise NotImplementedError('Beam parallel and adjacent to wall is not supported')
            else:
                raise ValueError

        # Calculate I_f_1 ... I_f_4
        if not all([i in input_kwargs for i in ['I_f_1', 'I_f_2', 'I_f_3', 'I_f_4']]):
            input_kwargs.update(clause_b_1_3_5_I_f_i(**input_kwargs))
            _latex_equation_header.append(
                'Clause B.1.3 (5), the radiative heat flux from an opening for each of the faces 1, 2, 3, and 4 of the column are:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # calculate alpha
        # if not all([i in input_kwargs for i in ['T_m', 'T_m_1', 'T_m_2', 'T_m_3', 'T_m_4']]):
        if 'alpha' not in input_kwargs:
            if input_kwargs['is_forced_draught'] is False:
                __ = clause_b_4_1_12_alpha_c(**input_kwargs)
                __['alpha'] = __.pop('alpha_c')
                __['alpha'] /= 1000.  # W/m2/K -> kW/m2/K, BS EN 1991-1-2 uses W/m2/K and BS EN 1993-1-2 uses kW/m2/K
                input_kwargs.update(__)
                _latex_equation_header.append(
                    'BS EN 1991-1-2 Clause B.4.1 (12), the convective heat transfer coefficient $\\alpha$ ($\\alpha_c$ $\\frac{W}{m^2\\cdot K}$ in BS EN 1991-1-2, '
                    'this is converted to $\\frac{kW}{m^2\\cdot K}$ at later parts of this assessment) is:')
            elif input_kwargs['is_forced_draught'] is True:
                __ = clause_b_4_2_11_alpha_c(**input_kwargs)
                __['alpha'] = __.pop('alpha_c')
                __['alpha'] /= 1000.  # W/m2/K -> kW/m2/K, BS EN 1991-1-2 uses W/m2/K and BS EN 1993-1-2 uses kW/m2/K
                input_kwargs.update(__)
                _latex_equation_header.append(
                    'BS EN 1991-1-2 Clause B.4.2 (11), the convective heat transfer coefficient $\\alpha$ ($\\alpha_c$ $\\frac{W}{m^2\\cdot K}$ in BS EN 1991-1-2, '
                    'this is converted to $\\frac{kW}{m^2\\cdot K}$ at later parts of this assessment) is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate T_m_1 ... T_m_4
        if not all([i in input_kwargs for i in ['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4']]):
            input_kwargs.update(clause_b_1_3_3_T_m_i_beam(**input_kwargs))
            _latex_equation_header.append(
                'Clause B.1.3 (3), the temperature of the steel member for each of its faces 1, 2, 3, and 4 are:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate L_x (only used to calculate T_z)
        if 'L_x' not in input_kwargs and 'T_z' not in input_kwargs:
            input_kwargs.update(helper_L_x(**input_kwargs))

        # Calculate phi_f
        if 'phi_f' not in input_kwargs:
            input_kwargs.update(clause_b_1_4_1_phi_f(**input_kwargs))
            _latex_equation_header.append('Clause B.1.4 (1), the radiative heat flux from an opening is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate a_z
        if 'a_z' not in input_kwargs:
            input_kwargs.update(clause_b_5_3_a_z(**input_kwargs))
            _latex_equation_header.append('Clause B.5 (3), the absorptivity of the flames is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate I_f
        if 'I_f' not in input_kwargs:
            input_kwargs.update(clause_b_1_3_5_I_f(**input_kwargs))
            _latex_equation_header.append('Clause B.1.3 (5), the radiative heat flux from an opening is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate I_z
        if 'I_z' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_I_z(**input_kwargs))
            _latex_equation_header.append('Clause B.4 (1), the radiative heat flux from the flames is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate T_z
        if 'T_z' not in input_kwargs:
            if input_kwargs['is_forced_draught'] is False:
                # non forced draught
                input_kwargs.update(clause_b_4_1_10_T_z(T_w=input_kwargs['T_o'], **input_kwargs))
                _latex_equation_header.append('BS EN 1991-1-2 Clause B.4.1 (10), the flame temperature along the axis at the centroid of the beam section, $L_{x}$, is:')
            elif input_kwargs['is_forced_draught'] is True:
                # forced draught
                input_kwargs.update(clause_b_4_2_9_T_z(T_w=input_kwargs['T_o'], **input_kwargs))
                _latex_equation_header.append('BS EN 1991-1-2 Clause B.4.2 (9), the flame temperature along the axis at the centroid of the beam section, $L_{x}$, is:')
            else:
                raise ValueError('Unkown condition')

            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate T_m
        if 'T_m' not in input_kwargs:
            input_kwargs.update(clause_b_1_3_3_T_m(**input_kwargs))
            _latex_equation_header.append('Clause B.1.3 (3), the average temperature of the steel member is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        input_kwargs.update(_latex_equation_header=_latex_equation_header,
                            _latex_equation_content=_latex_equation_content)

        return input_kwargs


def _test_fully_or_partially_engulfed_beam():
    test = ExternalSteelTemperatureEngulfedBeam(
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        lambda_4=1,
        sigma=5.67e-11,
        T_z=700,
        T_o=1000,
        d_1=0.4,
        d_2=0.8,
        # d_eq=(0.8+0.4)/2,
        d_aw=0,
        w_t=10,
        L_H=5,
        L_L=5,
        h_eq=3.3,
        is_forced_draught=True,
        is_flame_above_steel_member=True,
        is_steel_member_adjacent_to_wall=False,
        T_f=1400,
        T_z_1=900,  # todo
        T_z_2=800,  # todo
        # phi_z_1=0.1,  # todo
        # phi_z_2=0.2,  # todo
        # phi_z_3=0.3,  # todo
        alpha=20,
        w_f=12.5,
        sec_title_prefix='B.4.',
        T_m=None,
        I_z=None,
        I_f=None,
    )
    test.make_pdf_web('test')


if __name__ == '__main__':
    _test_fully_or_partially_engulfed_beam()
