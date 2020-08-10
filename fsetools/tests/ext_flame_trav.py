from fsetools.lib.fse_eurocode_external_steel import external_fire_and_steel_beam_column_temperatures

if __name__ == '__main__':
    input_params = dict(
        D=20.88,  # original depth 85.5, shortened to match travelling fire width
        W=25.1,  # the dimension with opening
        H=3.3,
        w_t=20.88,  # travelling fire maximum length
        h_eq=3.3,
        q_fd=400,
        Q=80,
        d_1_column=0.4,
        d_2_column=0.7,
        d_1_beam=0.4,
        d_2_beam=0.982,

        d_fw=0.79 - 0.2,
        d_aw=0,

        is_wall_above_opening=True,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,

        fp_pdf_no_suffix='Appendix B - Travelling fire',
        report_section_prefix='B.',
    )

    external_fire_and_steel_beam_column_temperatures(
        **input_params
    )
