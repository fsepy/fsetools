from pylatex import NoEscape, Section

from fsetools.lib.fse_bs_en_1991_1_2_external_flame import ExternalFlame as ExternalFlame
from fsetools.lib.fse_latex_report_template import ReportBase
from fsetools.libstd.bs_en_1991_1_2_2002_annex_b import *
from fsetools.libstd.bs_en_1993_1_2_2005_annex_b import clause_b_4_5_l, clause_b_1_3_2_d


class ExternalFlameForcedDraught(ReportBase):
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
        sections = list()
        if section_title:
            sections.append(Section(title=f'{section_title}'))
        else:
            sections.append(Section(title='Thermal actions for external members (forced draught)'))
        sections.append(self.section_1_introduction())
        sections.append(ExternalFlame.section_2_inputs(self.input_kwargs))
        sections.append(ExternalFlame.section_3_calculation(self.output_kwargs))
        sections.append(ExternalFlame.section_4_summary(self.output_kwargs))
        return sections

    @staticmethod
    def section_1_introduction():
        sec = ExternalFlame.section_1_introduction()
        sec[-1] = NoEscape(
            'This assessment is specific to forced draught condition in accordance with '
            'Clause B.4.2 in BS EN 1991-1-2.'
        )
        return sec

    @staticmethod
    def __calculation(**input_kwargs):

        _latex_equation_header = list()
        _latex_equation_content = list()

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
                        pass  # optional as only required to calculate Q

        # Calculate Q
        if 'Q' not in input_kwargs:
            input_kwargs.update(clause_b_4_2_1_Q(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (1), the heat release rate is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate compartment temperature
        if 'T_f' not in input_kwargs:
            if 'Omega' not in input_kwargs:
                input_kwargs.update(clause_1_6_Omega(**input_kwargs))
                _latex_equation_header.append('Clause 1.2, the variable $\\Omega$ is:')
                _latex_equation_content.append(input_kwargs['_latex'])
            input_kwargs.update(clause_b_4_2_2_T_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (3), the temperature within the fire compartment is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame vertical projection
        if 'L_L' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_3_L_L(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (3), the flame height is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame horizontal projection
        if 'L_H' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_4_L_H(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (4), the horizontal projection of flames is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame width
        if 'w_f' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_5_w_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (5), the flame width is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame length
        if 'L_f' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_6_L_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (6), the flame length along axis is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame temperature at window
        if 'T_w' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_7_T_w(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (7), the flame temperature at the window is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame temperature beyond window
        if 'T_z' not in input_kwargs:
            if 'L_x' not in input_kwargs:
                # __ = clause_b_4_5_l(**input_kwargs)
                __ = clause_b_4_5_l(
                    h_eq=input_kwargs['h_eq'],
                    L_H=input_kwargs['L_H'],
                    L_L=input_kwargs['L_L'],
                    d_fw=input_kwargs['d_fw'],
                    d_1=input_kwargs['d_1_column'],  # note this variable name is different
                    is_forced_draught=input_kwargs['is_forced_draught']
                )
                __['L_x'] = __.pop('l')
                input_kwargs.update(__)
                _latex_equation_header.append(
                    'BS EN 1993-1-2 Clause B.4 (5), the distance $l$ ($L_x$ in BS EN 1991-1-2) from the opening is:')
                _latex_equation_content.append(input_kwargs['_latex'])
            input_kwargs.update(**clause_b_4_2_9_T_z(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (9), the flame temperature along the axis is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate T_z_1 and T_z_2
        # T_z_1 is only used for estimating beam element in BS EN 1993-1-2 Annex B
        if not all([i in input_kwargs for i in ['T_z_1', 'T_z_2']]):
            def L_x_1_and_2(L_L, L_H, d_1, d_fw, *_, **__):
                return sqrt((d_fw + 0.5 * d_1) ** 2 + ((d_fw + 0.5 * d_1) * (L_L / L_H)) ** 2)

            L_x = input_kwargs.pop('L_x')  # reserve L_x from input_kwargs
            # input_kwargs['L_x'] = L_x_1_and_2(**input_kwargs)
            input_kwargs['L_x'] = L_x_1_and_2(*[input_kwargs[i] for i in ['L_L', 'L_H', 'd_1_beam', 'd_fw']])
            __ = clause_b_4_1_10_T_z(**input_kwargs)
            __['T_z_1'] = __.pop('T_z')
            __['T_z_2'] = __['T_z_1']
            input_kwargs.update(__)
            input_kwargs['L_x'] = L_x  # revert L_x in input_kwargs to the reserved value
            _latex_equation_header.append(
                'Clause B.4.1 (10), the flame temperature along the axis at $L_{x,1}$ and $L_{x,2}$ is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # DEPRECIATED, NOT NECESSARY WITHOUT `d_f` WHICH IS DEFINED IN BS EN 1993-1-2
        # Calculate emissivity of flames
        # if 'epsilon_f' not in input_kwargs:
        #     # Calculate flame vertical projection
        #     if 'd_f' not in input_kwargs:
        #         input_kwargs.update(**clause_b_4_2_3_d_f(**input_kwargs))
        #         _latex_equation_header.append('Clause B.4.2 (3), the flame thickness is:')
        #         _latex_equation_content.append(input_kwargs['_latex'])
        #     input_kwargs.update(**clause_b_4_2_10_epsilon(**input_kwargs))
        #     _latex_equation_header.append('Clause B.4.2 (10), the emissivity of flames is:')
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
            __ = clause_b_4_2_11_alpha_c(**input_kwargs)
            __['alpha_c_column'] = __.pop('alpha_c')
            input_kwargs.update(**__)
            _latex_equation_header.append(
                'Clause B.4.2 (11), the connective heat transfer coefficient for the external column is:')
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
            __ = clause_b_4_2_11_alpha_c(**input_kwargs)
            __['alpha_c_beam'] = __.pop('alpha_c')
            input_kwargs.update(**__)
            _latex_equation_header.append(
                'Clause B.4.2 (11), the connective heat transfer coefficient for the external beam is:')
            _latex_equation_content.append(input_kwargs['_latex'])
            input_kwargs.pop(
                'd_eq')  # delete temporary `d_eq` from `input_kwargs`, `d_eq` will be calculated again later.

        input_kwargs.update(
            _latex_equation_header=_latex_equation_header,
            _latex_equation_content=_latex_equation_content
        )

        return input_kwargs


def _test_1():
    test_object_1 = ExternalFlameForcedDraught(
        D=85.8,
        W=25.1,
        H=3.3,
        h_eq=3.3,
        w_t=20.87,  # travelling fire maximum length
        q_fd=400,
        u=6,
        Q=80,  # override
        tau_F=1200,
        rho_g=0.45,
        g=9.81,
        T_0=293.15,
        A_v=61.1 * 3.3,
        is_wall_above_opening=True,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        is_forced_draught=True,
        lambda_3=1,
        d_1=0.8,
        d_2=0.42
    )

    print(f'{test_object_1.output_kwargs["T_f"]:.5f} == 1450.36828')
    assert abs(test_object_1.output_kwargs['T_f'] - 1450.36828) < 1e-4

    print(f'{test_object_1.output_kwargs["T_w"]:.5f} == 973.54189')
    assert abs(test_object_1.output_kwargs['T_w'] - 973.54189) < 1e-4


if __name__ == '__main__':
    _test_1()
