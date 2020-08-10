from os.path import realpath

from pylatex import NewPage

from fsetools.lib.fse_bs_en_1991_1_2_external_flame import ExternalFlame
from fsetools.lib.fse_bs_en_1991_1_2_external_flame_forced_draught import ExternalFlameForcedDraught
from fsetools.lib.fse_bs_en_1993_1_2_external_beam import ExternalSteelTemperatureEngulfedBeam
from fsetools.lib.fse_bs_en_1993_1_2_external_column import ExternalSteelTemperatureFullyEngulfedColumn
from fsetools.lib.fse_latex_report_template import Report


def make_pdf_helper(pylatex_cls, fn_no_suffix: str, fp_pdf_viewer: str = r'C:\Program Files\SumatraPDF\SumatraPDF.exe',
                    overleaf_fallback: bool = True):
    try:
        pylatex_cls.make_pdf(
            fp_pdf=fn_no_suffix,
            fp_pdf_viewer=fp_pdf_viewer,
        )
        pylatex_cls.make_tex(fp_tex=fn_no_suffix)
    except Exception as e:
        if overleaf_fallback:
            pylatex_cls.make_pdf_web(fp_tex=fn_no_suffix)
        else:
            raise e


if __name__ == '__main__':
    D = 66
    W = 20
    H = 3.3
    A_f = D * W
    w_t = 8.3
    h_eq = 3.3
    A_v = w_t * h_eq
    q_fd = 200
    d_1_column = 0.4
    d_2_column = 0.7
    d_1_beam = 0.4
    d_2_beam = 0.982

    d_fw = 0.79 - 0.2
    d_aw = 0

    section_1 = ExternalFlame(
        D=D,
        W=W,
        H=H,
        A_f=A_f,
        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        q_fd=q_fd,
        W_1=W,
        W_2=D,
        tau_F=1200,
        rho_g=0.45,
        g=9.81,
        T_0=293.15,
        is_wall_above_opening=True,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        is_forced_draught=False,
        d_1_column=d_1_column,
        d_2_column=d_2_column,
        d_1_beam=d_1_beam,
        d_2_beam=d_2_beam,
        d_fw=d_fw,
        d_aw=d_aw,
    )

    section_2 = ExternalSteelTemperatureFullyEngulfedColumn(
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        lambda_1=0.5 * (w_t - d_2_column),
        lambda_3=d_fw,
        sigma=5.67e-11,
        T_z=section_1.output_kwargs['T_z'],
        T_o=section_1.output_kwargs['T_w'],
        d_1=d_1_column,
        d_2=d_2_column,
        w_t=w_t,
        L_H=section_1.output_kwargs['L_H'],
        L_L=section_1.output_kwargs['L_L'],
        h_eq=h_eq,
        is_forced_draught=False,
        T_f=section_1.output_kwargs['T_f'],
        alpha=section_1.output_kwargs['alpha_c_column'] / 1000,
        w_f=w_t,  # travelling fire maximum length
        T_m=None,
        I_z=None,
        I_f=None,
    )

    section_3 = ExternalSteelTemperatureEngulfedBeam(
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        lambda_4=d_fw,  # distance between member and wall
        sigma=5.67e-11,
        T_z=section_1.output_kwargs['T_z'],
        T_o=section_1.output_kwargs['T_w'],
        d_1=d_1_beam,
        d_2=d_2_beam,
        w_t=w_t,
        d_aw=d_aw,
        L_H=section_1.output_kwargs['L_H'],
        L_L=section_1.output_kwargs['L_L'],
        h_eq=h_eq,
        is_forced_draught=False,
        is_flame_above_steel_member=True,
        is_steel_member_adjacent_to_wall=False,
        T_f=section_1.output_kwargs['T_f'],
        T_z_1=section_1.output_kwargs['T_z_1'],
        T_z_2=section_1.output_kwargs['T_z_2'],
        alpha=section_1.output_kwargs['alpha_c_beam'] / 1000,
        w_f=w_t,
        T_m=None,
        I_z=None,
        I_f=None,
    )

    section_4 = ExternalFlameForcedDraught(
        D=D,
        W=W,
        H=H,
        h_eq=h_eq,
        w_t=w_t,  # travelling fire maximum length
        q_fd=q_fd,
        u=6,
        tau_F=1200,
        rho_g=0.45,
        g=9.81,
        T_0=293.15,
        A_v=A_v,
        is_wall_above_opening=True,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        is_forced_draught=True,
        d_1_column=d_1_column,
        d_2_column=d_2_column,
        d_1_beam=d_1_beam,
        d_2_beam=d_2_beam,
        d_fw=d_fw,
    )

    section_5 = ExternalSteelTemperatureFullyEngulfedColumn(
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        lambda_1=0.5 * (w_t - d_2_column),
        lambda_3=d_fw,
        sigma=5.67e-11,
        T_z=section_4.output_kwargs['T_z'],
        T_o=section_4.output_kwargs['T_w'],
        d_1=d_1_column,
        d_2=d_1_column,
        w_t=w_t,
        L_H=section_4.output_kwargs['L_H'],
        L_L=section_4.output_kwargs['L_L'],
        h_eq=h_eq,
        is_forced_draught=True,
        T_f=section_4.output_kwargs['T_f'],
        alpha=section_4.output_kwargs['alpha_c_column'] / 1000,
        w_f=section_4.output_kwargs['w_f'],
        T_m=None,
        I_z=None,
        I_f=None,
        a_z=None,
        phi_f=None,
    )

    section_6 = ExternalSteelTemperatureEngulfedBeam(
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        lambda_4=d_fw,  # distance between member and wall
        sigma=5.67e-11,
        T_z=section_4.output_kwargs['T_z'],
        T_o=section_4.output_kwargs['T_w'],
        d_1=d_1_beam,
        d_2=d_2_beam,
        w_t=w_t,
        d_aw=d_aw,
        L_H=section_4.output_kwargs['L_H'],
        L_L=section_4.output_kwargs['L_L'],
        h_eq=h_eq,
        is_forced_draught=True,
        is_flame_above_steel_member=True,
        is_steel_member_adjacent_to_wall=False,
        T_f=section_4.output_kwargs['T_f'],
        T_z_1=section_4.output_kwargs['T_z_1'],
        T_z_2=section_4.output_kwargs['T_z_2'],
        alpha=section_4.output_kwargs['alpha_c_beam'] / 1000,
        w_f=section_4.output_kwargs['w_f'],
        T_m=None,
        I_z=None,
        I_f=None,
        phi_f=None,
        a_z=None,
    )

    appendix = Report(
        # sections=[VerticalSpace(size='8cm')] +
        section_1.make_latex_sections() +
        [NewPage()] +
        section_2.make_latex_sections(section_title='Heat transfer to external steel column (no forced draught)') +
        [NewPage()] +
        section_3.make_latex_sections(section_title='Heat transfer to external steel beam (no forced draught)') +
        [NewPage()] +
        section_4.make_latex_sections() +
        [NewPage()] +
        section_5.make_latex_sections(section_title='Heat transfer to external steel column (forced draught)') +
        [NewPage()] +
        section_6.make_latex_sections(section_title='Heat transfer to external steel beam (forced draught)'),
        sec_title_prefix='C.'
    )

    make_pdf_helper(appendix, realpath('Appendix C - Parametric Fire 1'), overleaf_fallback=False)
