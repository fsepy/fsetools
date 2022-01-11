from fsetools.lib.fse_eurocode_external_steel import *


# todo, function to be finalised as api has changed.
def test_1():
    input_params = dict(
        D=20.9,  # original depth 85.5, shortened to match travelling fire width
        W=25.1,  # the dimension with opening
        H=3.3,
        w_t=20.9,  # travelling fire maximum length
        h_eq=3.3,
        q_fd=400,
        Q=80,
        d_eq=(0.4 + 0.7) / 2.,
        d_1=0.4,
        d_2=0.7,
        # d_1_column=0.4,
        # d_2_column=0.7,
        # d_1_beam=0.4,
        # d_2_beam=0.982,

        L_x=0.9,
        d_fw=0.79 - 0.2,
        d_aw=0,

        is_wall_above_opening=True,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,

        fp_pdf_no_suffix='Appendix A - Travelling fire',
        report_section_prefix='A.',

        make_pdf=False,
    )

    external_steel_temperature(
        **input_params
    )
