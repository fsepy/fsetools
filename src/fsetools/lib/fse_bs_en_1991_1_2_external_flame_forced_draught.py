try:
    from pylatex import NoEscape, Section
except ModuleNotFoundError:
    pass

from .fse_latex_report_template import ReportBase
from ..libstd.bs_en_1991_1_2_2002_annex_b import *


class ExternalFlameForcedDraught(ReportBase):
    """
    Carries out assessment in Clause B.4.2, BS EN 1991-1-2 (2002) and generate LaTeX report
    """
    from .fse_bs_en_1991_1_2_external_flame_no_forced_draught import \
        ExternalFlameNoForcedDraught as __ExternalFlameNoForcedDraught

    def __init__(
            self,
            h_eq: float,
            w_t: float,
            A_t: float,
            **kwargs
    ):
        super().__init__()

        # derived values below
        A_v = w_t * h_eq
        try:
            O = h_eq ** 0.5 * A_v / A_t
        except TypeError:
            # this happens when A_t is not provided
            O = None

        input_kwargs = locals()
        input_kwargs.pop('self')
        input_kwargs.pop('kwargs')
        input_kwargs.pop('__class__')
        input_kwargs.update(**kwargs)
        self.input_kwargs = input_kwargs
        self.output_kwargs = self.__calculation(**input_kwargs)

    def make_latex(self, *args, **kwargs):
        # make LaTeX from template, this include permeable, formatting etc
        doc = self.make_document_template(**self.input_kwargs)

        # make LaTeX contents/sections
        for i in self.make_latex_sections(*args, **kwargs):
            doc.append(i)

        return doc

    def make_latex_sections(
            self,
            section_title: str = None,
            include_introduction: bool = True,
            include_inputs_summary: bool = True,
            include_calculation: bool = True,
            include_outputs_summary: bool = True,
            *_,
            **__,
    ) -> list:
        """
        Put up together LaTeX calculation procedure

        :param section_title: Section title
        :param include_introduction: `True` to include introduction section, default `True`
        :param include_inputs_summary: `True` to include user defined parameters, default `True`
        :param include_calculation: `True` to include calculation procedures, default `True`
        :param include_outputs_summary: `True` to include outputs summary section, default `True`
        :return: a list of LaTeX items
        """
        sections = list()
        if section_title:
            sections.append(Section(title=f'{section_title}'))
        else:
            sections.append(Section(title='Thermal actions for external members (forced draught)'))

        if include_introduction:
            sections.append(self.section_1_introduction())

        if include_inputs_summary:
            sections.append(self.__ExternalFlameNoForcedDraught.section_2_inputs(self.input_kwargs))

        if include_calculation:
            sections.append(self.__ExternalFlameNoForcedDraught.section_3_calculation(self.output_kwargs))

        if include_outputs_summary:
            sections.append(self.__ExternalFlameNoForcedDraught.section_4_summary(self.output_kwargs))

        return sections

    def section_1_introduction(self):
        sec = self.__ExternalFlameNoForcedDraught.section_1_introduction()
        sec[-1] = NoEscape(
            'This assessment is specific to \\textit{forced draught} condition in accordance with '
            'Clause B.4.2 in BS EN 1991-1-2.'
        )
        return sec

    @staticmethod
    def __calculation(**input_kwargs):

        _latex_equation_header = list()
        _latex_equation_content = list()

        # Calculate Q, if not provided
        if 'Q' not in input_kwargs:
            if 'DW_ratio' not in input_kwargs:
                try:
                    is_windows_on_more_than_one_wall = input_kwargs['is_windows_on_more_than_one_wall']
                    is_central_core = input_kwargs['is_central_core']
                except KeyError:
                    raise KeyError(
                        '`is_central_core` and `is_windows_on_more_than_one_wall` are missing, required to calculate `DW_ratio`')

                if is_windows_on_more_than_one_wall is False and is_central_core is False:
                    input_kwargs.update(clause_b_2_2_DW_ratio(**input_kwargs))
                    _latex_equation_header.append(NoEscape('Clause B.2 (2), the ratio of $D/W$ is:'))
                    _latex_equation_content.append(input_kwargs['_latex'])
                elif is_windows_on_more_than_one_wall is True and is_central_core is False:
                    input_kwargs.update(clause_b_2_3_DW_ratio(**input_kwargs))
                    _latex_equation_header.append(NoEscape('Clause B.2 (3), the ratio of $D/W$ is:'))
                    _latex_equation_content.append(input_kwargs['_latex'])
                elif is_windows_on_more_than_one_wall is True and is_central_core is True:
                    input_kwargs.update(clause_b_2_4_DW_ratio(**input_kwargs))
                    _latex_equation_header.append(NoEscape('Clause B.2 (4), the ratio of $D/W$ is:'))
                    _latex_equation_content.append(input_kwargs['_latex'])
                else:
                    raise ValueError

            input_kwargs.update(clause_b_4_2_1_Q(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (1), the heat release rate is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate compartment temperature, if not provided
        if 'T_f' not in input_kwargs:
            if 'Omega' not in input_kwargs:
                input_kwargs.update(clause_1_6_Omega(**input_kwargs))
                _latex_equation_header.append('Clause 1.2, the variable $\\Omega$ is:')
                _latex_equation_content.append(input_kwargs['_latex'])
            input_kwargs.update(clause_b_4_2_2_T_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (3), the temperature within the fire compartment is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame vertical projection, if not provided
        if 'L_L' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_3_L_L(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (3), the flame height is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame horizontal projection, if not provided
        if 'L_H' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_4_L_H(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (4), the horizontal projection of flames is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame width, if not provided
        if 'w_f' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_5_w_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (5), the flame width is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame length, if not provided
        if 'L_f' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_6_L_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (6), the flame length along axis is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame temperature at window, if not provided
        if 'T_w' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_7_T_w(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (7), the flame temperature at the window is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame temperature beyond window, if not provided
        if 'T_z' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_9_T_z(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (9), the flame temperature along the axis is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        input_kwargs.update(
            _latex_equation_header=_latex_equation_header,
            _latex_equation_content=_latex_equation_content
        )

        return input_kwargs


def _test_1():
    test_object_1 = ExternalFlameForcedDraught(
        q_fd=400,
        Q=80,  # override
        W_1=25.1,
        W_2=85.8,
        A_f=85.8 * 25.1,
        A_t=2 * (85.8 * 25.1 + 25.1 * 3.3 + 3.3 * 85.8),
        h_eq=3.3,
        w_t=20.87,  # travelling fire maximum length
        A_v=3.3 * 20.87,
        L_x=0.1,
        u=6,
        tau_F=1200,
        rho_g=0.45,
        g=9.81,
        T_0=293.15,
        T_z_1=None,
        T_z_2=None,
        is_wall_above_opening=True,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        alpha_c=None,
    )

    print(f'{test_object_1.output_kwargs["T_f"]:.5f} == 1450.36828')
    assert abs(test_object_1.output_kwargs['T_f'] - 1450.36828) < 1e-4

    print(f'{test_object_1.output_kwargs["T_w"]:.5f} == 973.54189')
    assert abs(test_object_1.output_kwargs['T_w'] - 973.54189) < 1e-4


if __name__ == '__main__':
    _test_1()
