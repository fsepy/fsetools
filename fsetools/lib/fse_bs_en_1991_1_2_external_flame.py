from pylatex import NoEscape, Section, Subsection, Enumerate

from fsetools.etc.latex import make_alginat_equations, make_summary_table
from fsetools.lib.fse_latex_report_template import ReportBase
from fsetools.libstd.bs_en_1991_1_2_2002_annex_b import *
from fsetools.libstd.bs_en_1993_1_2_2005_annex_b import clause_b_1_3_2_d


class ExternalFlame(ReportBase):
    def __init__(
            self,
            D: float,
            W: float,
            H: float,
            h_eq: float,
            w_t: float,
            A_v: float,
            **kwargs
    ):
        super().__init__()

        # derived values below
        if 'A_v' not in kwargs:
            A_v = w_t * h_eq
        if 'A_f' not in kwargs:
            A_f = D * W
        if 'A_t' not in kwargs:
            A_t = 2 * (D * W + W * H + H * D)
        if 'O' not in kwargs:
            O = h_eq ** 0.5 * A_v / (2 * (D * W + W * H + H * D))

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
        sections: list = list()
        if section_title:
            sections.append(Section(title=f'{section_title}'))
        else:
            sections.append(Section(title='Thermal actions for external members (no forced draught)'))
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
            '"Eurocode 1: Actions on structures – Part 1-2: General actions – Actions on structures exposed to fire" '
            '(BS EN 1991-1-2). This method allows the determination of (a) the maximum temperatures of a compartment '
            'fire; (b) the size and temperatures of the flame from openings; and (c) the thermal radiation and '
            'convection parameters.\\par'))

        sec.append(NoEscape(
            'This method considers steady-state conditions for various parameters and is only valid when the following '
            'conditions are met:'))
        section_1_enumerate_1 = Enumerate()
        section_1_enumerate_1.add_item(NoEscape('Fire load $q_{fd}$ is greater than 200 ${MJ}\\cdot m^{-2}$; and'))
        section_1_enumerate_1.add_item(NoEscape(
            'The size of the fire compartment should not exceed 70 $m$ in length, 18 $m$ in width and 5 $m$ in height.'
        ))
        sec.append(section_1_enumerate_1)
        sec.append(NoEscape('\\par'))

        sec.append(NoEscape(
            'Units, symbols and abbreviations are consistent with the referenced document unless stated.\\par'))

        sec.append(NoEscape(
            'Numerical values shown in this document are rounded as appropriate for readability, however, calculations '
            'are carried out based on the actual values.\\par'
        ))

        sec.append(NoEscape(
            'This assessment is specific to \\textit{no forced draught} condition in accordance with '
            'Clause B.4.1 in BS EN 1991-1-2.'
        ))

        return sec

    @staticmethod
    def section_2_inputs(input_kwargs: dict):
        section_2 = Subsection(title='Inputs')
        symbols = [
            'D', 'W', 'H', 'A_f', 'h_eq', 'w_t', 'A_v', 'd_ow', 'DW_ratio', 'q_fk', 'q_fd', 'L_x', 'tau_F', 'u',
            'Omega', 'O', 'Q', 'd_eq', 'T_f', 'L_L', 'L_H', 'L_f', 'T_w', 'T_z'
        ]
        section_2.append(make_summary_table(
            symbols=symbols,
            units=UNITS,
            descriptions=DESCRIPTIONS,
            values=input_kwargs
        ))
        return section_2

    @staticmethod
    def section_3_calculation(output_kwargs):
        latex_equation_header = output_kwargs['_latex_equation_header']
        latex_equation_content = output_kwargs['_latex_equation_content']
        section_3 = Subsection(title='Calculation')
        for i in range(len(latex_equation_header)):
            section_3.append(NoEscape(latex_equation_header[i]))
            section_3.append(make_alginat_equations(latex_equation_content[i]))
        return section_3

    @staticmethod
    def section_4_summary(output_kwargs: dict):
        section_4 = Subsection(title='Summary')
        section_4.append('Results of this assessment are summarised below.')
        symbols = ['Q', 'T_f', 'L_L', 'L_H', 'L_f', 'T_w', 'T_z', 'epsilon_f', 'alpha_c']
        section_4.append(make_summary_table(
            symbols=symbols,
            units=UNITS,
            descriptions=DESCRIPTIONS,
            values=output_kwargs
        ))
        return section_4

    @staticmethod
    def __calculation(**input_kwargs):

        _latex_equation_header = list()
        _latex_equation_content = list()

        # Calculate Q
        if 'Q' not in input_kwargs:
            # Calculate D/W, optional
            if 'DW_ratio' not in input_kwargs:
                # EAFP style below
                try:
                    input_kwargs.update(clause_b_2_2_DW_ratio(**input_kwargs))
                    _latex_equation_header.append(NoEscape('Clause B.2 (2), the ratio of $D/W$ is:'))
                    _latex_equation_content.append(input_kwargs['_latex'])
                except (AssertionError, TypeError):
                    try:
                        input_kwargs.update(clause_b_2_3_DW_ratio(**input_kwargs))
                        _latex_equation_header.append(NoEscape('Clause B.2 (3), the ratio of $D/W$ is:'))
                        _latex_equation_content.append(input_kwargs['_latex'])
                    except (AssertionError, TypeError):
                        try:
                            input_kwargs.update(clause_b_2_4_DW_ratio(**input_kwargs))
                            _latex_equation_header.append(NoEscape('Clause B.2 (4), the ratio of $D/W$ is:'))
                            _latex_equation_content.append(input_kwargs['_latex'])
                        except (AssertionError, TypeError):
                            raise ValueError(
                                'Failed to calculate `DW_ratio`')  # optional as only required to calculate Q
            input_kwargs.update(clause_b_4_1_1_Q(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (1), the heat release rate is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate compartment temperature
        if 'T_f' not in input_kwargs:
            if 'Omega' not in input_kwargs:
                input_kwargs.update(clause_1_6_Omega(**input_kwargs))
                _latex_equation_header.append('Clause 1.2, the variable $\\Omega$ is:')
                _latex_equation_content.append(input_kwargs['_latex'])
            input_kwargs.update(clause_b_4_1_2_T_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (2), the temperature within the fire compartment is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate external flame vertical projection
        if 'L_L' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_3_L_L(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (3), the external flame height is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate external flame horizontal projection
        if 'L_H' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_6_L_H(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (6), the horizontal project of flames is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame length
        if 'L_f' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_7_L_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (7), the flame length along the axis is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame temperature at window
        if 'T_w' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_8_T_w(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (8), the flame temperature at window opening is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame temperature beyond window
        # if 'T_z' not in input_kwargs:
        #     if 'L_x' not in input_kwargs:
        #         # __ = clause_b_4_5_l(**input_kwargs)
        #         __ = clause_b_4_5_l(
        #             h_eq=input_kwargs['h_eq'],
        #             L_H=input_kwargs['L_H'],
        #             L_L=input_kwargs['L_L'],
        #             d_fw=input_kwargs['d_fw'],
        #             d_1=input_kwargs['d_1_column'],  # note this variable name is different
        #             is_forced_draught=input_kwargs['is_forced_draught']
        #         )
        #         __['L_x'] = __.pop('l')
        #         input_kwargs.update(__)
        #         _latex_equation_header.append(
        #             'BS EN 1993-1-2 Clause B.4 (5), the distance $l$ ($L_x$ in BS EN 1991-1-2) from the opening is:')
        #         _latex_equation_content.append(input_kwargs['_latex'])
        #     input_kwargs.update(clause_b_4_1_10_T_z(**input_kwargs))
        #     _latex_equation_header.append('Clause B.4.1 (10), the flame temperature along the axis at $L_x$ is:')
        #     _latex_equation_content.append(input_kwargs['_latex'])
        #
        # # Calculate T_z_1
        # # T_z_1 is only used for estimating beam element in BS EN 1993-1-2 Annex B
        # if 'T_z_1' not in input_kwargs:
        #     def L_x_1(d_fw, d_1, d_aw, *_, **__, ):
        #         return (d_fw + 0.5 * d_1) * sqrt(2) + d_aw
        #
        #     L_x = input_kwargs.pop('L_x')
        #     # input_kwargs['L_x'] = L_x_1(**input_kwargs)
        #     input_kwargs['L_x'] = L_x_1(*[input_kwargs[i] for i in ['d_fw', 'd_1_beam', 'd_aw']])
        #     __ = clause_b_4_1_10_T_z(**input_kwargs)
        #     __['T_z_1'] = __.pop('T_z')
        #
        #     input_kwargs.update(__)
        #     input_kwargs['L_x'] = L_x
        #     _latex_equation_header.append('Clause B.4.1 (10), the flame temperature along the axis at $L_{x,1}$ (as per BS EN 1993-1-2) is:')
        #     _latex_equation_content.append(input_kwargs['_latex'])
        #
        # # Calculate T_z_2
        # # T_z_2 is only used for estimating beam element in BS EN 1993-1-2 Annex B
        # if 'T_z_2' not in input_kwargs:
        #     def L_x_2(d_fw, d_1, d_2, d_aw, *_, **__):
        #         return (d_fw + 0.5 * d_1) * sqrt(2) + d_aw + d_2
        #
        #     L_x = input_kwargs.pop('L_x')
        #     # input_kwargs['L_x'] = L_x_2(**input_kwargs)
        #     input_kwargs['L_x'] = L_x_2(*[input_kwargs[i] for i in ['d_fw', 'd_1_beam', 'd_2_beam', 'd_aw']])
        #     __ = clause_b_4_1_10_T_z(**input_kwargs)
        #     __['T_z_2'] = __.pop('T_z')
        #     input_kwargs.update(__)
        #     input_kwargs['L_x'] = L_x
        #     _latex_equation_header.append('Clause B.4.1 (10), the flame temperature along the axis at $L_{x,2}$ (as per BS EN 1993-1-2) is:')
        #     _latex_equation_content.append(input_kwargs['_latex'])

        # DEPRECIATED, `epsilon_f` IS DEFINED IN BS EN 1993-1-2
        # Calculate emissivity of flames
        # if 'epsilon_f' not in input_kwargs:
        #     # Calculate flame thickness
        #     if 'd_f' not in input_kwargs:
        #         input_kwargs.update(clause_b_4_1_3_d_f(**input_kwargs))
        #         _latex_equation_header.append('Clause B.4.1 (3), the flame thickness is:')
        #         _latex_equation_content.append(input_kwargs['_latex'])
        #     input_kwargs.update(clause_b_4_1_11_epsilon_f(**input_kwargs))
        #     _latex_equation_header.append('Clause B.4.1 (11), the emissivity of flames is:')
        #     _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate alpha_c, for column
        if 'alpha_c_column' not in input_kwargs:
            if 'd_eq' not in input_kwargs:
                __ = clause_b_1_3_2_d(d_1=input_kwargs['d_1_column'], d_2=input_kwargs['d_2_column'])
                __['d_eq'] = __.pop('d')
                input_kwargs.update(**__)
                # _latex_equation_header.append(
                #     'BS EN 1993-1-2 Clause B.1.3 (2), the geometrical characteristic of an external column $d$ ($d_{eq}$ in BS EN 1991-1-2) is:')
                # _latex_equation_content.append(input_kwargs['_latex'])
            __ = clause_b_4_1_12_alpha_c(**input_kwargs)
            __['alpha_c_column'] = __.pop('alpha_c')
            input_kwargs.update(**__)
            _latex_equation_header.append(
                'Clause B.4.1 (12), the connective heat transfer coefficient for the external column is:')
            _latex_equation_content.append(input_kwargs['_latex'])
            input_kwargs.pop(
                'd_eq')  # delete temporary `d_eq` from `input_kwargs`, `d_eq` will be calculated again later.

        # Calculate alpha_c, for beam
        if 'alpha_c_beam' not in input_kwargs:
            if 'd_eq' not in input_kwargs:
                __ = clause_b_1_3_2_d(d_1=input_kwargs['d_1_beam'], d_2=input_kwargs['d_2_beam'])
                __['d_eq'] = __.pop('d')
                input_kwargs.update(**__)
                # _latex_equation_header.append(
                #     'BS EN 1993-1-2 Clause B.1.3 (2), the geometrical characteristic of an external beam $d$ ($d_{eq}$ in BS EN 1991-1-2) is:')
                # _latex_equation_content.append(input_kwargs['_latex'])
            __ = clause_b_4_1_12_alpha_c(**input_kwargs)
            __['alpha_c_beam'] = __.pop('alpha_c')
            input_kwargs.update(**__)
            _latex_equation_header.append(
                'Clause B.4.1 (12), the connective heat transfer coefficient for the external beam is:')
            _latex_equation_content.append(input_kwargs['_latex'])
            input_kwargs.pop(
                'd_eq')  # delete temporary `d_eq` from `input_kwargs`, `d_eq` will be calculated again later.

        input_kwargs.update(_latex_equation_header=_latex_equation_header,
                            _latex_equation_content=_latex_equation_content)

        return input_kwargs


def _test_1():
    test_object_1 = ExternalFlame(
        D=85.8,
        W=25.1,
        H=3.3,
        A_f=85.8 * 25.1,
        h_eq=3.3,
        w_t=20.88,  # travelling fire maximum length
        A_v=61.1 * 3.3,
        q_fd=400,
        Q=80,  # override
        W_1=25.1,
        W_2=85.8,
        tau_F=1200,
        rho_g=0.45,
        g=9.81,
        T_0=293.15,
        is_wall_above_opening=True,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        is_forced_draught=False,
        lambda_3=1,
        d_1=0.8,
        d_2=0.42,
    )

    print(f'{test_object_1.output_kwargs["T_f"]:.5f} == 1207.71692')
    assert abs(test_object_1.output_kwargs['T_f'] - 1207.71692) < 1e-4

    print(f'{test_object_1.output_kwargs["T_w"]:.5f} == 1113.08870')
    assert abs(test_object_1.output_kwargs['T_w'] - 1113.08870) < 1e-4


if __name__ == '__main__':
    _test_1()
