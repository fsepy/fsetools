import json
import subprocess
import webbrowser
from abc import ABC, abstractmethod
from sys import platform
import tempfile

try:
    import requests
    from pylatex import NoEscape, Document, Package
except ModuleNotFoundError:
    pass


class ReportBase(ABC):
    def __init__(self):
        super().__init__()

    def make_tex(self, fp_tex: str):
        doc = self.make_latex()
        if fp_tex.endswith('.tex'):
            fp_tex = fp_tex[:-4]
        doc.generate_tex(fp_tex)

    def make_pdf(self, fp_pdf: str, fp_pdf_viewer: str = None, clean: bool = True, clean_tex: bool = True):
        """
        Render LaTeX with the following compilers: `latexmk` or `pdflatex`
        :param fp_pdf:
        :param fp_pdf_viewer:
        :param clean:
        :param clean_tex:
        :return:
        """

        # get file path, without .pdf suffix
        if fp_pdf.endswith('.pdf'):
            fp_pdf = fp_pdf[:-4]

        # make LaTeX source code
        doc = self.make_latex()

        doc.generate_pdf(filepath=fp_pdf, clean=clean, clean_tex=clean_tex)

        if platform == 'darwin':
            subprocess.Popen(['open', fp_pdf + '.pdf'], creationflags=0x08000000)
        else:
            if fp_pdf_viewer:
                subprocess.Popen([fp_pdf_viewer, fp_pdf + '.pdf'], creationflags=0x08000000)
            else:
                subprocess.Popen([fp_pdf + '.pdf'], shell=True, creationflags=0x08000000)

    def make_pdf_web(self, fp_tex: str = None):

        if fp_tex is not None:
            if fp_tex.endswith('.tex'):
                fp_tex = fp_tex[:-4]
        else:
            temp_fp_tex = tempfile.NamedTemporaryFile()
            fp_tex = temp_fp_tex.name

        self.make_tex(fp_tex=fp_tex + '.tex', )
        fileio_response = requests.post(
            "https://file.io",
            files={
                'file': (
                    fp_tex + '.tex',
                    open(fp_tex + '.tex', 'rb'))
            }
        )
        texurl = json.loads(fileio_response.text)['link']
        webbrowser.open(f"https://www.overleaf.com/docs?snip_uri={texurl}")

        try:
            temp_fp_tex.close()
        except Exception as e:
            pass

    @abstractmethod
    def make_latex(self, *args, **kwargs) -> Document:
        pass

    @abstractmethod
    def make_latex_sections(self) -> list:
        pass

    @staticmethod
    def make_document_template(sec_title_prefix: str = None, *_, **__):
        doc = Document(
            indent=False,
            geometry_options={'left': '0.99in', 'right': '0.99in', 'top': '1.5in', 'bottom': '1.5in'}
        )
        doc.packages.append(Package('xcolor'))
        doc.packages.append(Package('sectsty'))
        doc.packages.append(Package('hyperref'))
        doc.packages.append(Package('mathtools'))
        # doc.packages.append(Package('standalone', options='preview'))
        doc.preamble.append(NoEscape(r'\definecolor{ofr}{RGB}{0, 164, 153}'))
        doc.preamble.append(NoEscape(r'\renewcommand\familydefault{\sfdefault}'))
        doc.preamble.append(NoEscape(r'\sectionfont{\color{ofr}}'))
        doc.preamble.append(NoEscape(r'\subsectionfont{\color{ofr}}'))
        doc.preamble.append(NoEscape(r'\subsubsectionfont{\color{ofr}}'))
        doc.preamble.append(NoEscape(r'\renewcommand{\arraystretch}{1.2}'))
        # \titleformat{<command>}[<shape>]{<format>}{<label>}{<sep>}{<before-code>}[<after-code>]
        # doc.preamble.append(NoEscape(r'\titleformat{\section}{}{}{\hspace{1cm}}{}%'))
        if sec_title_prefix:
            doc.preamble.append(NoEscape(f'\\renewcommand{{\\thesection}}{{{sec_title_prefix}\\arabic{{section}}}}'))

        return doc


class Report(ReportBase):
    def __init__(self, sections: list, sec_title_prefix: str):
        self.sections: list = sections
        self.sec_title_prefix: str = sec_title_prefix
        super().__init__()

    def make_latex(self) -> Document:
        doc = self.make_document_template(self.sec_title_prefix)
        for i in self.sections:
            doc.append(i)
        return doc

    def make_latex_sections(self) -> list:
        return self.sections
