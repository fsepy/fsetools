import subprocess

from pylatex import NoEscape, Document, Package, Section

from fsetools.etc.latex import py2tex_modified, make_alginat_equations, make_table
from fsetools.libstd.bs_en_1991_1_2_2002_annex_b import *


class ExternalFlame:
    def __init__(
            self,
            D: float,
            W: float,
            H: float,
            h_eq: float,
            w_t: float,
            q_fd: float,
            A_v: float,
            **kwargs
    ):

        # derived values below
        if 'A_v' not in kwargs:
            A_v = w_t * h_eq
        if 'A_f' not in kwargs:
            A_f = D * W
        if 'A_t' not in kwargs:
            A_t = 2 * (D * W + W * H + H * D)
        if 'O' not in kwargs:
            O = h_eq ** 0.5 * A_v / (2 * (D * W + W * H + H * D))
        if 'Omega' not in kwargs:
            Omega = (D * W) * q_fd / (A_v * (2 * (D * W + W * H + H * D))) ** 0.5

        input_kwargs = locals()
        input_kwargs.pop('self')
        input_kwargs.pop('kwargs')
        input_kwargs.update(**kwargs)
        self.input_kwargs = input_kwargs
        self.output_kwargs = self.__calculation(**input_kwargs)

    def make_tex(self, fp_tex: str):
        doc = self.__make_pylatex()
        doc.generate_tex(fp_tex.rstrip('.tex'))

    def make_pdf(self, fp_pdf: str, fp_pdf_viewer: str = None):
        doc = self.__make_pylatex()
        doc.generate_pdf(filepath=fp_pdf.rstrip('.pdf'), clean=True)
        if fp_pdf_viewer:
            subprocess.Popen([fp_pdf_viewer, fp_pdf])

    def __make_pylatex(self):
        latex_equation_header = self.output_kwargs['_latex_equation_header']
        latex_equation_content = self.output_kwargs['_latex_equation_content']
        input_kwargs = self.input_kwargs

        doc = Document(
            indent=False,
            geometry_options={'left': '0.5in', 'right': '0.5in', 'top': '1in', 'bottom': '1in'}
        )
        doc.packages.append(Package('xcolor'))
        doc.packages.append(Package('sectsty'))
        doc.packages.append(Package('hyperref'))
        doc.preamble.append(NoEscape(r'\definecolor{colourofr}{RGB}{0, 164, 153}'))
        doc.preamble.append(NoEscape(r'\renewcommand\familydefault{\sfdefault}'))
        doc.preamble.append(NoEscape(r'\sectionfont{\color{colourofr}}'))
        doc.preamble.append(NoEscape(r'\renewcommand{\arraystretch}{1.1}'))

        # ----------------------
        # Section 1 Introduction
        # ----------------------
        section_1 = Section(title='Introduction')
        section_1.append(
            r'The external flame dimensions and temperature are calculated as per the method described in "BS EN 1991-1-2:2002: Eurocode 1 - Actions on structures - General actions - Actions on structures exposed to fire".')
        section_1.append(NoEscape(r'\par'))
        section_1.append(
            'Symbols and abbreviations shown in this document are consistent with the referenced document unless specifically stated and therefore is not repeated herein.')
        section_1.append(NoEscape(r'\par'))
        section_1.append(NoEscape(
            'Numerical values shown in this document are rounded as appropriate for readability. However, the calculations are carried out based on \\href{https://docs.python.org/3/tutorial/floatingpoint.html}{high precision} numerical values.'
        ))
        doc.append(section_1)

        # ----------------
        # Section 2 Inputs
        # ----------------
        section_2 = Section(title='Inputs')
        symbols = ['D', 'W', 'H', 'A_f', 'h_eq', 'w_t', 'A_v', 'd_ow', 'DW_ratio', 'q_fd', 'L_x', 'tau_F', 'Omega', 'O',
                   'Q', 'T_f', 'L_L', 'L_H', 'L_f', 'T_w', 'T_z']
        [symbols.remove(i) for i in list(set(symbols) - set(input_kwargs))]
        units = [UNITS[symbol] for symbol in symbols]
        values = [input_kwargs[symbol] for symbol in symbols]
        descriptions = [DESCRIPTIONS[symbol] for symbol in symbols]
        section_2.append(make_table(
            4,
            ['Symbol', 'Unit', 'Value', 'Description'],
            py2tex_modified(symbols),
            py2tex_modified(units),
            [f'{value:g}' for value in values],
            [description[0].upper() + description[1:] for description in descriptions],
        ))
        doc.append(section_2)

        # ---------------------
        # Section 3 Calculation
        # ---------------------
        section_3 = Section(title='Calculation')
        for i in range(len(latex_equation_header)):
            section_3.append(NoEscape(latex_equation_header[i]))
            section_3.append(make_alginat_equations(latex_equation_content[i]))
        doc.append(section_3)

        # -----------------
        # Section 4 Summary
        # -----------------
        section_4 = Section(title='Summary')
        section_4.append('The results of this assessment are summarised below.')
        symbols = ['Q', 'T_f', 'L_L', 'L_H', 'L_f', 'T_w', 'T_z', 'epsilon_f', 'alpha_c']
        [symbols.remove(i) for i in list(set(symbols) - set(self.output_kwargs))]
        units = [UNITS[symbol] for symbol in symbols]
        values = [self.output_kwargs[symbol] for symbol in symbols]
        descriptions = [DESCRIPTIONS[symbol] for symbol in symbols]
        section_4.append(make_table(
            4,
            ['Symbol', 'Unit', 'Value', 'Description'],
            py2tex_modified(symbols),
            py2tex_modified(units),
            [f'{value:g}' for value in values],
            [description[0].upper() + description[1:] for description in descriptions],
        ))
        doc.append(section_4)

        return doc

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
            input_kwargs.update(clause_b_4_1_1_Q(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (1), the heat release rate is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate compartment temperature
        if 'T_f' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_2_T_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (3), the temperature within the fire compartment is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame thickness
        if 'd_f' not in input_kwargs:
            input_kwargs.update(clause_b_4_1_3_d_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (3), the flame thickness is:')
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
        try:
            input_kwargs.update(clause_b_4_1_8_T_w(**input_kwargs))
            _latex_equation_header.append('Clause B.4.1 (8), the flame temperature at window opening is:')
            _latex_equation_content.append(input_kwargs['_latex'])
        except Exception as e:
            print(e)

        # Calculate flame temperature beyond window
        input_kwargs.update(clause_b_4_1_10_T_z(**input_kwargs))
        _latex_equation_header.append('Clause B.4.1 (10), the flame temperature along the axis at $L_x$ is:')
        _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate emissivity of flames
        input_kwargs.update(clause_b_4_1_11_epsilon(**input_kwargs))
        _latex_equation_header.append('Clause B.4.1 (11), the emissivity of flames is:')
        _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate convective heat transfer coefficient
        input_kwargs.update(**clause_b_4_1_12_alpha_c(**input_kwargs))
        _latex_equation_header.append('Clause B.4.1 (12), the connective heat transfer coefficient is:')
        _latex_equation_content.append(input_kwargs['_latex'])

        input_kwargs.update(_latex_equation_header=_latex_equation_header,
                            _latex_equation_content=_latex_equation_content)

        return input_kwargs


if __name__ == '__main__':
    external_flame_report_1 = ExternalFlame(
        D=85.8,
        W=25.1,
        H=3.3,
        h_eq=3.35,
        w_t=20.87371141,  # travelling fire maximum length
        # W_1=85.8,
        # W_2=25.1,
        # L_L=0.5,
        # A_v1=200,
        # d_ow=1e10,
        q_fd=870,
        d_eq=0.8,
        Q=80,  # override
        # d_f=2/3*3.35,
        L_x=1,
        tau_F=1200,
        rho_g=0.45,
        g=9.81,
        T_0=293.15,
        A_v=61.1 * 3.3,
        is_wall_above_opening=True,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
    )

    external_flame_report_1.make_pdf(
        fp_pdf=r'E:\projects\1CW\WP4\ec_external_flame-1_no_forced_draught.pdf',
        # fp_pdf_viewer=r'C:\Program Files\SumatraPDF\SumatraPDF.exe',
        fp_pdf_viewer=r'C:\Users\ian\AppData\Local\SumatraPDF\SumatraPDF.exe'
    )
