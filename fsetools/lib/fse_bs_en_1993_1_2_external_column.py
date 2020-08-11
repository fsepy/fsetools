import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pylatex import NoEscape, Section, Subsection

from fsetools.etc.latex import make_alginat_equations, make_summary_table
from fsetools.lib.fse_latex_report_template import ReportBase
from fsetools.libstd.bs_en_1991_1_2_2002_annex_b import clause_b_4_1_10_T_z
from fsetools.libstd.bs_en_1993_1_2_2005_annex_b import *


class ExternalSteelTemperatureFullyEngulfedColumn(ReportBase):
    def __init__(
            self,
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
            sections.append(Section(title='Heat transfer to external steel column'))
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
            'This method allows the determination of the temperatures of an external steel member.\\par'))

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
            'This assessment is specific to an external steel column which is fully engulfed in flame in accordance '
            'with Clause B.4 in BS EN 1993-1-2.'
        ))

        return sec

    @staticmethod
    def section_2_inputs(input_kwargs: dict):
        sec = Subsection(title='Inputs')
        symbols = [
            'w_t', 'h_eq', 'd_1', 'd_2',
            'lambda_1', 'lambda_3', 'C_1', 'C_2', 'C_3', 'C_4',
            'L_H', 'L_L', 'T_f', 'T_o', 'T_z', 'alpha', 'w_f',
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

        _latex_equation_header, _latex_equation_content = list(), list()

        # Calculate l
        if 'l' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_lambda_2(**input_kwargs))
            _latex_equation_header.append('Clause B.4 (1), the flame thickness $\\lambda_2$ is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate lambda_2
        if 'lambda_2' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_lambda_2(**input_kwargs))
            _latex_equation_header.append('Clause B.4 (1), the flame thickness $\\lambda_2$ is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate lambda_4
        if 'lambda_4' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_lambda_4(**input_kwargs))
            _latex_equation_header.append('Clause B.4 (1), the flame thickness $\\lambda_4$ is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate T_z
        if 'T_z' not in input_kwargs:
            if 'L_x' not in input_kwargs:
                # __ = clause_b_4_5_l(**input_kwargs)
                __ = clause_b_4_5_l(
                    h_eq=input_kwargs['h_eq'],
                    L_H=input_kwargs['L_H'],
                    L_L=input_kwargs['L_L'],
                    d_fw=input_kwargs['d_fw'],
                    d_1=input_kwargs['d_1'],  # note this variable name is different
                    is_forced_draught=input_kwargs['is_forced_draught']
                )
                __['L_x'] = __.pop('l')
                input_kwargs.update(__)
                _latex_equation_header.append(
                    'Clause B.4 (5), the distance $l$ ($L_x$ in BS EN 1991-1-2) from the opening is:')
                _latex_equation_content.append(input_kwargs['_latex'])
            input_kwargs.update(clause_b_4_1_10_T_z(T_w=input_kwargs['T_o'], **input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (10), the flame temperature along the axis at $L_x$ is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate epsilon_z_1 ... epsilon_z_4
        if not all([i in input_kwargs for i in ['epsilon_z_1', 'epsilon_z_2', 'epsilon_z_3', 'epsilon_z_4']]):
            input_kwargs.update(clause_b_4_2_epsilon_z_i(**input_kwargs))
            _latex_equation_header.append(
                'Clause B.4 (2), the emissivity of the flames for each of the faces 1, 2, 3 and 4 of the column are:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate I_z_1 ... I_z_4
        if not all([i in input_kwargs for i in ['I_z_1', 'I_z_2', 'I_z_3', 'I_z_4']]):
            input_kwargs.update(clause_b_4_1_I_z_i(**input_kwargs))
            _latex_equation_header.append(
                'Clause B.4 (1), the radiative heat flux from the flames for each of the faces 1, 2, 3 and 4 of the column are:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate I_z
        if 'I_z' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_I_z(**input_kwargs))
            _latex_equation_header.append('Clause B.4 (1), the radiative heat flux from the flames is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate phi_f_1 ... phi_f_4
        if not all([i in input_kwargs for i in ['phi_z_1', 'phi_z_2', 'phi_z_3', 'phi_z_4']]):
            input_kwargs.update(clause_b_1_4_1_phi_f_i_column(**input_kwargs))
            _latex_equation_header.append(
                'Clause B.1.4 (1), the radiative heat flux from an opening for each of the faces 1, 2, 3 and 4 of the column is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate phi_f
        if 'phi_f' not in input_kwargs:
            input_kwargs.update(clause_b_1_4_1_phi_f(**input_kwargs))
            _latex_equation_header.append('Clause B.1.4 (1), the radiative heat flux from an opening is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate a_z
        if 'a_z' not in input_kwargs:
            input_kwargs.update(clause_b_4_6_a_z(**input_kwargs))
            _latex_equation_header.append('Clause B.4 (6), the absorptivity of the flames is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate I_f_1 ... I_f_4
        if not all([i in input_kwargs for i in ['I_f_1', 'I_f_2', 'I_f_3', 'I_f_4']]):
            input_kwargs.update(clause_b_1_3_5_I_f_i(**input_kwargs))
            _latex_equation_header.append(
                'Clause B.1.3 (5), the radiative heat flux from an opening for each of the faces 1, 2, 3, and 4 of the column are:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate I_f
        if 'I_f' not in input_kwargs:
            input_kwargs.update(clause_b_1_3_5_I_f(**input_kwargs))
            _latex_equation_header.append('Clause B.1.3 (5), the radiative heat flux from an opening is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate T_m_1 ... T_m_4
        if not all([i in input_kwargs for i in ['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4']]):
            input_kwargs.update(clause_b_1_3_3_T_m_i_column(**input_kwargs))
            _latex_equation_header.append(
                'Clause B.1.3 (3), the temperature of the steel member for each of its faces 1, 2, 3, and 4 are:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate T_m
        if 'T_m' not in input_kwargs:
            input_kwargs.update(clause_b_1_3_3_T_m(**input_kwargs))
            _latex_equation_header.append('Clause B.1.3 (3), the average temperature of the steel member is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        input_kwargs.update(_latex_equation_header=_latex_equation_header,
                            _latex_equation_content=_latex_equation_content)

        return input_kwargs

    @staticmethod
    def make_figure(
            h_eq,
            L_H,
            L_L,
            d_1,
            d_2,
            w_f,
            w_t,
            lambda_3,
            lambda_1,
            W_TH=0.2,
            *_, **__
    ):

        xlim1, xlim2 = -1.1, L_H + 0.1,
        ylim1, ylim2 = -(w_f - w_t) / 2 - 0.1, w_t + (w_f - w_t) / 2 + 0.1
        zlim1, zlim2 = -1.1, L_L + h_eq + 0.1,

        total_width = (xlim2 - xlim1) * 1.2
        total_height = (zlim2 - zlim1 + ylim2 - ylim1)
        scale = min(6 / total_width, 8.7 / total_height)

        # fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
        fig = plt.figure(constrained_layout=True, figsize=(total_width * scale, total_height * scale))
        gridspec = fig.add_gridspec(
            ncols=1,
            nrows=2,
            height_ratios=(zlim2 - zlim1 + 0.4, ylim2 - ylim1 + 0.4)
        )

        # plot x-z plane, i.e. vertical slice
        ax1 = fig.add_subplot(gridspec[0])
        patches = [
            Polygon([[0, 0], [0, zlim1], [0 - W_TH, zlim1], [0 - W_TH, 0]], color=(128 / 255, 128 / 255, 128 / 255, 1),
                    closed=True, fill=True, lw=0),
            Polygon([[0, zlim2], [0, h_eq], [-W_TH, h_eq], [-W_TH, zlim2]], color=(128 / 255, 128 / 255, 128 / 255, 1)),
            Polygon([[lambda_3 + d_1, zlim2], [lambda_3 + d_1, zlim1], [lambda_3, zlim1], [lambda_3, zlim2]],
                    color=(128 / 255, 128 / 255, 128 / 255, 1)),
            Polygon([[L_H, L_L + h_eq], [L_H, L_L], [0, 0], [0, h_eq]], color=(255 / 255, 0 / 255, 0 / 255, 0.5)),
        ]
        for p in patches:
            ax1.add_patch(p)
        ax1.annotate(
            '', xy=(0, 0), xycoords='data',
            xytext=(lambda_3, 0), textcoords='data',
            arrowprops={'arrowstyle': '<->'})
        ax1.annotate(
            '$\\lambda_3$', xy=(1, 1), xycoords='data',
            xytext=(5, 0), textcoords='offset points')

        ax1.set_xlim((xlim1, xlim2))
        ax1.set_ylim((zlim1, zlim2))

        # plot x-y plane, i.e. horizontal slice
        ax2 = fig.add_subplot(gridspec[1], sharex=ax1)
        patches = [
            Polygon([(0, 0), (0, ylim1), (-W_TH, ylim1), (-W_TH, 0)], color=(128 / 255, 128 / 255, 128 / 255, 1)),
            Polygon([(0, ylim2), (0, w_t), (-W_TH, w_t), (-W_TH, ylim2)], color=(128 / 255, 128 / 255, 128 / 255, 1)),
            Polygon([(L_H, 0.5 * (w_f - w_t) + w_t), (L_H, -0.5 * (w_f - w_t)), (0, 0), (0, w_t)],
                    color=(255 / 255, 0 / 255, 0 / 255, 0.5)),
            Polygon([(lambda_3 + d_1, w_t - lambda_1), (lambda_3 + d_1, w_t - lambda_1 - d_2),
                     (lambda_3, w_t - lambda_1 - d_2), (lambda_3, w_t - lambda_1)],
                    color=(128 / 255, 128 / 255, 128 / 255, 1)),
        ]
        for p in patches:
            ax2.add_patch(p)
        ax2.set_ylim((ylim1, ylim2))

        ax1.set_aspect(1)
        ax2.set_aspect(1)

        plt.show()
        fig.savefig('test.png')


def _test_fully_engulfed_column():
    test_object_1 = ExternalSteelTemperatureFullyEngulfedColumn(
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        lambda_1=10,
        lambda_3=1,
        sigma=5.67e-12,
        T_z=958.82,
        T_o=973.54,
        d_1=0.8,
        d_2=0.42,
        w_t=20.88,
        L_H=6.17,
        L_L=2.7,
        h_eq=3.3,
        is_forced_draught=True,
        T_f=1200 + 273.15,
        alpha=26.67,
        w_f=23.34,
    )

    print(f'{test_object_1.output_kwargs["T_m"]:.5f} == 958.88173')
    assert abs(test_object_1.output_kwargs['T_m'] - 958.88173) < 1e-4


if __name__ == '__main__':
    _test_fully_engulfed_column()
