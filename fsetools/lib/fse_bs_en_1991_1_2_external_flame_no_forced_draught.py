from pylatex import NoEscape, Section, Subsection, Enumerate

from fsetools.etc.latex import make_alginat_equations, make_summary_table
from fsetools.lib.fse_latex_report_template import ReportBase
from fsetools.libstd.bs_en_1991_1_2_2002_annex_b import *


class ExternalFlameNoForcedDraught(ReportBase):
    """
    Carries out assessment as per Clause B.4.2, BS EN 1991-1-2 (2002), generates a LaTeX report.
    """

    def __init__(
            self,
            h_eq: float,
            w_t: float,
            A_t: float,
            **kwargs
    ):
        super().__init__()

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
            sections.append(Section(title='Thermal actions for external members (non forced draught)'))

        if include_introduction:
            sections.append(self.section_1_introduction())

        if include_inputs_summary:
            sections.append(ExternalFlameNoForcedDraught.section_2_inputs(self.input_kwargs))

        if include_calculation:
            sections.append(ExternalFlameNoForcedDraught.section_3_calculation(self.output_kwargs))

        if include_outputs_summary:
            sections.append(ExternalFlameNoForcedDraught.section_4_summary(self.output_kwargs))

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
            'W_1', 'W_2', 'A_f', 'h_eq', 'w_t', 'A_v', 'd_ow', 'DW_ratio', 'q_fk', 'q_fd', 'L_x', 'tau_F', 'u',
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
        """
        Calculation procedure as defined in Clause B4 in BS EN 1991-1-2 (2002) to assess characteristics of external
        flame from a window.
        :param input_kwargs:    Keyword arguments containing all the required parameters as per Clause B4.
                                The following functions are involved in this process:
                                    clause_b_2_2_DW_ratio, to calculate D/W
                                    clause_b_2_3_DW_ratio, to calculate D/W
                                    clause_b_2_4_DW_ratio, to calculate D/W
                                    clause_b_4_1_1_Q, to calculate fire HRR
                                    clause_1_6_Omega, an intermediate variable
                                    clause_b_4_1_2_T_f, flame temperature within the fire enclosure
                                    clause_b_4_1_3_L_L, external flame vertical dimension
                                    clause_b_4_1_6_L_H, external flame horizontal dimension
                                    clause_b_4_1_7_L_f, external flame total length
                                    clause_b_4_1_8_T_w, flame temperature at the window
                                    clause_b_4_1_10_T_z, external flame temperature at a given location
                                    clause_b_4_1_12_alpha_c, convective heat transfer coefficient
        :return:    A dict containing the following:
                        _latex_equation_header, a list of descriptions, used for generating LaTeX
                        _latex_equation_content, a list of step-by-step equations, used for generating LaTeX
                        **, all keyword arguments returned from the functions in described in the `input_kwargs`
        """

        _latex_equation_header = list()
        _latex_equation_content = list()

        # Calculate Q, optional if provided
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
                        except (AssertionError, TypeError) as e:
                            raise ValueError(f'Failed to calculate `DW_ratio`, {e}')
            input_kwargs.update(clause_b_4_1_1_Q(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (1), the heat release rate is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate compartment temperature, if not provided
        if 'T_f' not in input_kwargs:
            if 'Omega' not in input_kwargs:
                input_kwargs.update(clause_1_6_Omega(**input_kwargs))
                _latex_equation_header.append('Clause 1.2, the variable $\\Omega$ is:')
                _latex_equation_content.append(input_kwargs['_latex'])
            input_kwargs.update(clause_b_4_1_2_T_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (2), the temperature within the fire compartment is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate external flame vertical projection, if not provided
        if 'L_L' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_3_L_L(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (3), the external flame height is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate external flame horizontal projection, if not provided
        if 'L_H' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_6_L_H(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (6), the horizontal project of flames is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame length, if not provided
        if 'L_f' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_7_L_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (7), the flame length along the axis is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame temperature at window, if not provided
        if 'T_w' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_8_T_w(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (8), the flame temperature at window opening is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame temperature beyond window, if not provided
        if 'T_z' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_10_T_z(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (10), the flame temperature along the axis at $L_x$ is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        input_kwargs.update(
            _latex_equation_header=_latex_equation_header,
            _latex_equation_content=_latex_equation_content
        )

        return input_kwargs


def _test_1():
    """
    Test against results documented in "190702-R00-SC19024-WP1-Flame Projection Calculations-DN-CIC",
    dated 2nd July 2019, prepared by OFR (GM)
    """

    test_object_1 = ExternalFlameNoForcedDraught(
        q_fd=870,
        W_1=1.82,
        W_2=5.46,
        A_f=14.88,
        A_t=70.3,
        h_eq=1.1,
        w_t=1.82,
        tau_F=1200,
        T_0=293.15,
        is_wall_above_opening=True,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        alpha_c=None,
        T_f=None,
        T_w=None,
        T_z=None,
    )

    print(f'{test_object_1.output_kwargs["L_L"]:.5f} == 1.33691')
    assert abs(test_object_1.output_kwargs['L_L'] - 1.33691) < 1e-4

    print(f'{test_object_1.output_kwargs["L_H"]:.5f} == 0.36667')
    assert abs(test_object_1.output_kwargs['L_H'] - 0.36667) < 1e-4


if __name__ == '__main__':
    _test_1()
