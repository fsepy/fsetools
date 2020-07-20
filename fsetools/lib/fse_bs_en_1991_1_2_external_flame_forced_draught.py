import json
import subprocess
import webbrowser

from pylatex import NoEscape, Document, Package, Section, Enumerate

from fsetools.etc.latex import make_table, make_alginat_equations, py2tex_modified
from fsetools.libstd.bs_en_1991_1_2_2002_annex_b import *


class ExternalFlame:
    def __init__(
            self,
            D: float,
            W: float,
            H: float,
            h_eq: float,
            w_t: float,
            A_v: float,
            q_fd: float,
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
        section_1.append(NoEscape(
            r'Calculation documented herein follows Annex B in '
            r'"BS EN 1991-1-2:2002: Eurocode 1 - Actions on structures - General actions - Actions on structures '
            r'exposed to fire". This method allows the determination of (a) the maximum temperatures of a compartment'
            r'fire; (b) the size and temperatures of the flame from openings; and (c) the thermal radiation and '
            r'convection parameters.'))
        section_1.append(NoEscape(r'\par'))
        section_1.append(NoEscape(
            'This method considers steady-state conditions for various parameters and is only valid when the following '
            'conditions are met:'))
        section_1_enumerate_1 = Enumerate()
        section_1_enumerate_1.add_item(NoEscape('Fire load $q_{fd}$ is greater than 200 ${MJ}\\cdot m^{-2}$; and'))
        section_1_enumerate_1.add_item(NoEscape(
            'The size of the fire compartment should not exceed 70 $m$ in length, 18 $m$ in width and 5 $m$ in height.'
        ))
        section_1.append(section_1_enumerate_1)
        section_1.append(NoEscape(r'\par'))
        section_1.append(NoEscape(
            'Symbols and abbreviations shown in this document are consistent with the referenced document unless '
            'specifically stated and therefore is not repeated herein.'))
        section_1.append(NoEscape(r'\par'))
        section_1.append(NoEscape(
            'Numerical values shown in this document are rounded as appropriate for readability, however, calculations '
            'are carried out based on unrounded numerical values with '
            '\\href{https://docs.python.org/3/tutorial/floatingpoint.html}{high precision}.'
        ))
        doc.append(section_1)

        # ----------------
        # Section 2 Inputs
        # ----------------
        section_2 = Section(title='Inputs')
        symbols = ['D', 'W', 'H', 'A_f', 'h_eq', 'w_t', 'A_v', 'd_ow', 'DW_ratio', 'q_fk', 'q_fd', 'L_x', 'tau_F',
                   'Omega', 'O', 'Q', 'd_eq', 'T_f', 'L_L', 'L_H', 'L_f', 'T_w', 'T_z']
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
            input_kwargs.update(clause_b_4_2_1_Q(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (1), the heat release rate is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        # Calculate flame vertical projection
        if 'd_f' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_3_d_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (3), the flame thickness is:')
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

        if 'w_f' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_5_w_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (5), the flame width is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        if 'L_f' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_6_L_f(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (6), the flame length along axis is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        if 'T_w' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_7_T_w(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (7), the flame temperature at the window is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        if 'T_z' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_9_T_z(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (9), the flame temperature along the axis is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        if 'epsilon' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_10_epsilon(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (10), the emissivity of flames is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        if 'alpha_c' not in input_kwargs:
            input_kwargs.update(**clause_b_4_2_11_alpha_c(**input_kwargs))
            _latex_equation_header.append('Clause B.4.2 (11), the convective heat transfer coefficient is:')
            _latex_equation_content.append(input_kwargs['_latex'])

        input_kwargs.update(
            _latex_equation_header=_latex_equation_header,
            _latex_equation_content=_latex_equation_content
        )

        return input_kwargs


if __name__ == '__main__':
    external_flame_report_1 = ExternalFlame(
        D=85.8,
        W=25.1,
        H=3.3,
        h_eq=3.35,
        w_t=20.87371141,  # travelling fire maximum length
        L_L=3,
        d_ow=1e10,
        q_fd=870,
        d_eq=0.8,
        u=6,
        Q=80,  # override
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

    try:
        external_flame_report_1.make_pdf(
            fp_pdf=r'ec_ext_flame_01_forced_draught.pdf',
            fp_pdf_viewer=r'C:\Users\ian\AppData\Local\SumatraPDF\SumatraPDF.exe'
        )
    except:
        import requests

        external_flame_report_1.make_tex(fp_tex=r'ec_ext_flame_01_forced_draught.tex', )
        fileio_response = requests.post(
            "https://file.io",
            files={
                'file': (
                    'ec_ext_flame_01_forced_draught.tex', open('ec_ext_flame_01_forced_draught.tex', 'rb'))
            }
        )
        texurl = json.loads(fileio_response.text)['link']
        webbrowser.open(f"https://www.overleaf.com/docs?snip_uri={texurl}")
