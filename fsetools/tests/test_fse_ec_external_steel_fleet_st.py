from fsetools.lib.fse_bs_en_1991_1_2_external_flame_forced_draught import ExternalFlameForcedDraught
from fsetools.lib.fse_bs_en_1991_1_2_external_flame_no_forced_draught import ExternalFlameNoForcedDraught
from fsetools.lib.fse_bs_en_1993_1_2_external_beam_engulfed import ExternalSteelTemperatureEngulfedBeam
from fsetools.lib.fse_bs_en_1993_1_2_external_column_engulfed import ExternalSteelTemperatureFullyEngulfedColumn
from fsetools.lib.fse_latex_report_template import Report


def flame_no_forced_draught(
        W_1,
        W_2,
        is_windows_on_more_than_one_wall,
        is_central_core,
        A_f,
        q_fd,
        tau_F,
        O,
        h_eq,
        A_t,
        w_t,
        is_wall_above_opening,
):
    report = ExternalFlameNoForcedDraught(
        # clause_b_2_2_DW_ratio
        W_1=W_1,
        W_2=W_2,
        is_windows_on_more_than_one_wall=is_windows_on_more_than_one_wall,
        is_central_core=is_central_core,

        # clause_b_2_3_DW_ratio
        # W_1=0,                                  # previously defined above
        # W_2=0,                                  # previously defined above
        # A_v1=1,
        # A_v=1,
        # is_windows_on_more_than_one_wall=0,     # previously defined above
        # is_central_core=0,                      # previously defined above

        # clause_b_2_4_DW_ratio
        # W_1=0,                                  # previously defined above
        # W_2=0,                                  # previously defined above
        # L_c=1,
        # W_c=1,
        # A_v1=0,                                 # previously defined above
        # A_v=0,                                  # previously defined above
        # is_central_core=0,                      # previously defined above

        # clause_b_4_1_1_Q
        A_f=A_f,
        q_fd=q_fd,
        tau_F=tau_F,
        O=O,
        # A_v=1,                                  # previously defined above
        h_eq=h_eq,
        # DW_ratio=1,

        # clause_1_6_Omega
        # A_f=1,                                  # previously defined above
        A_t=A_t,
        # A_v=1,                                  # previously defined above
        # q_fd=1,                                 # derived

        # clause_b_4_1_3_L_L
        # Q=1,                                    # derived
        # A_v=1,                                  # previously defined above
        # h_eq=1,                                 # previously defined above
        # rho_g=1,                                # use default
        # g=1,                                    # use default

        # clause_b_4_1_6_L_H
        # h_eq=1,                                 # previously defined above
        w_t=w_t,
        # L_L=1,                                  # derived
        # d_ow=np.nan,
        is_wall_above_opening=is_wall_above_opening,

        # clause_b_4_1_7_L_f
        # w_t=1,                                  # previously defined above
        # L_L=1,                                  # derived
        # L_H=1,                                  # derived
        # h_eq=1,                                 # previously defined above
        # is_wall_above_opening=1,                # previously defined above

        # clause_b_4_1_8_T_w
        # L_f=1,                                  # derived
        # w_t=1,                                  # previously defined above
        # Q=1,                                    # derived
        # T_0=293.15,                             # use default

        # clause_b_4_1_10_T_z
        T_z=None,
        # T_w=1,                                  # derived
        # T_0=1,                                  # derived
        # L_x=1,  # todo
        # # w_t=1,                                  # previously defined above
        #
        # # misc
        # is_test=False,
    )

    return report


def flame_forced_draught(
        W_1,
        W_2,
        is_windows_on_more_than_one_wall,
        is_central_core,
        A_f,
        q_fd,
        tau_F,
        A_t,
        T_0,
        h_eq,
        u,
        w_t,
        A_v1=None,
):
    report = ExternalFlameForcedDraught(
        # clause_b_2_2_DW_ratio
        W_1=W_1,
        W_2=W_2,
        is_windows_on_more_than_one_wall=is_windows_on_more_than_one_wall,
        is_central_core=is_central_core,

        # clause_b_2_3_DW_ratio
        # W_1=0,                                  # previously defined above
        # W_2=0,                                  # previously defined above
        A_v1=A_v1,
        # A_v=1,
        # is_windows_on_more_than_one_wall=0,     # previously defined above
        # is_central_core=0,                      # previously defined above

        # clause_b_2_4_DW_ratio
        # W_1=0,                                  # previously defined above
        # W_2=0,                                  # previously defined above
        # L_c=1,
        # W_c=1,
        # A_v1=0,                                 # previously defined above
        # A_v=0,                                  # previously defined above
        # is_central_core=0,                      # previously defined above

        # clause_b_4_2_1_Q
        A_f=A_f,
        q_fd=q_fd,
        tau_F=tau_F,

        # clause_1_6_Omega
        # A_f=0,                                  # previously defined above
        A_t=A_t,
        # A_v=0,                                  # previously defined above
        # q_fd=0,                                 # previously defined above

        # clause_b_4_2_2_T_f
        # Omega=1,                                # derived
        T_0=T_0,

        # clause_b_4_2_3_L_L
        h_eq=h_eq,
        # Q=1,                                    # derived
        # A_v=0,                                  # previously defined above
        u=u,

        # clause_b_4_2_4_L_H
        # h_eq=0,                                 # previously defined above
        # L_L=1,                                  # derived
        # u=0,                                    # previously defined above

        # clause_b_4_2_5_w_f
        w_t=w_t,
        # L_H=1,                                  # derived

        # clause_b_4_2_6_L_f
        # L_L=0,                                  # derived
        # L_H=0,                                  # derived

        # clause_b_4_2_7_T_w
        # A_v=0,                                  # previously defined above
        # Q=0,                                    # previously defined above
        # L_f=1,                                  # derived
        # T_0=0,                                  # previously defined above

        # clause_b_4_2_9_T_z
        T_z=None,  # skipped
        # L_x=1,
        # Q=0,                                    # previously defined above
        # A_v=0,                                  # previously defined above
        # T_w=1,                                  # derived
        # T_0=0,                                  # previously defined above

    )

    return report


def beam_temperature_no_forced_draught(
        is_forced_draught,

        L_L,
        L_H,
        Q,
        T_o,
        T_f,

        h_eq,
        w_t,
        A_v,
        d_aw,
        lambda_4,
        d_1,
        d_2,
        d_eq,
        C_1,
        C_2,
        C_3,
        C_4,

        sigma,
):
    report = ExternalSteelTemperatureEngulfedBeam(
        # clause_b_5_1_1_2_lambda_1
        L_L=L_L,
        L_H=L_H,
        h_eq=h_eq,
        d_aw=d_aw,
        lambda_4=lambda_4,
        d_1=d_1,
        is_forced_draught=is_forced_draught,

        # clause_b_5_1_1_2_lambda_2
        # L_L=1,                                                # previously defined
        # d_aw=1,                                               # previously defined
        d_2=d_2,
        # h_eq=1,                                               # previously defined
        # lambda_1=1,                                           # previously calculated
        # is_forced_draught=False,                              # previously defined

        # clause_b_5_1_1_2_lambda_3
        # L_H=1,                                                # previously defined
        # L_L=1,                                                # previously defined
        # lambda_4=1,                                           # previously defined
        # d_aw=1,                                               # previously defined
        # h_eq=1,                                               # previously defined
        # d_1=1,                                                # previously defined
        # d_2=1,                                                # previously defined
        # is_forced_draught=False,                              # previously defined

        # clause_b_1_4_1_phi_f_i_beam
        # h_eq=1,                                               # previously defined
        # w_t=1,                                                # previously defined
        # d_aw=1,                                               # previously defined
        # lambda_3=1,                                           # previously defined
        # lambda_4=1,                                           # previously defined

        # clause_b_5_2_1_epsilon_z_i
        # lambda_1=1,                                           # previously defined
        # lambda_2=1,                                           # previously calculated
        # lambda_3=1,                                           # previously calculated
        # lambda_4=1,                                           # previously defined

        # clause_b_5_1_2_2_I_z_i
        # C_1=1,                                                # previously defined
        # C_2=1,                                                # previously defined
        # C_3=1,                                                # previously defined
        # C_4=1,                                                # previously defined
        # epsilon_z_1=1,                                        # previously calculated
        # epsilon_z_2=1,                                        # previously calculated
        # epsilon_z_3=1,                                        # previously calculated
        # epsilon_z_4=1,                                        # previously calculated
        sigma=sigma,
        # T_z_1=1,  # previously calculated
        # T_z_2=1,  # previously calculated
        T_o=T_o,

        # clause_b_5_1_2_4_I_z_i
        # C_1=1,                                                # previously defined
        # C_3=1,                                                # previously defined
        # C_4=1,                                                # previously defined
        # epsilon_z_1=1,                                        # previously calculated
        # epsilon_z_3=1,                                        # previously calculated
        # epsilon_z_4=1,                                        # previously calculated
        # sigma=1,                                              # previously defined
        # T_z_1=1,                                              # previously defined
        # T_o=1,                                                # previously defined
        # d_2=1,
        # T_x=1,  # according to B.5.1.24)

        # clause_b_5_1_3_2_I_z_i
        # C_1, C_2, C_3, C_4,									# derived
        # epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4, 	# derived
        # sigma=1,                                              # previously defined
        # T_z_1, T_z_2,											# derived
        # T_o=1,                                                # previously defined

        # clause_b_1_3_5_I_f_i
        # phi_f_1, phi_f_2, phi_f_3, phi_f_4,					# derived
        # epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4,	# derived
        # sigma=1,                                              # previously defined
        T_f=T_f,
        # epsilon_f=1,

        # clause_b_4_1_12_alpha_c
        d_eq=d_eq,
        # Q=1,                                                  # previously defined
        A_v=A_v,  # previously defined

        # clause_b_4_2_11_alpha_c
        # d_eq=1,                                               # previously defined
        # A_v=1,                                                # previously defined
        # Q=1,                                                  # previously defined
        # u=u,

        # clause_b_1_3_3_T_m_i_beam
        # I_z_1, I_z_2, I_z_3, I_z_4,							# derived
        # I_f_1, I_f_2, I_f_3, I_f_4,							# derived
        # alpha=0.03,                                           # derived
        # T_z_1, T_z_2,											# derived
        # sigma=5.67e-11,                                       # previously defined

        # clause_b_1_4_1_phi_f
        phi_f=None,
        C_1=C_1,
        C_2=C_2,
        C_3=C_3,
        C_4=C_4,
        # phi_f_1=1,                                            # previously calculated
        # phi_f_2=1,                                            # previously calculated
        # phi_f_3=1,                                            # previously calculated
        # phi_f_4=1,                                            # previously calculated
        # d_1=1,                                                # previously defined
        # d_2=1,                                                # previously defined

        # clause_b_5_3_a_z
        a_z=None,
        # lambda_1=1,                                           # previously defined

        # clause_b_1_3_5_I_f
        I_f=None,
        # phi_f=1,
        # a_z=1,
        # sigma=1,                                              # previously defined
        # T_f=1,                                                # previously defined
        # epsilon_f=1,                                          # previously defined

        # clause_b_4_1_I_z
        I_z=None,
        # C_1, C_2, C_3, C_4,									# derived
        # I_z_1, I_z_2, I_z_3, I_z_4,							# derived
        # d_1=1,                                                # previously defined
        # d_2=1,                                                # previously defined

        # clause_b_4_1_10_T_z
        T_z=None,
        # T_z = 1000+293.15,
        # T_w=1,
        # L_x=1,
        w_t=w_t,
        Q=Q,
        # T_0=1,

        # clause_b_1_3_3_T_m
        T_m=None,
        # I_z=1,
        # I_f=1,
        # alpha=1,                                              # previously defined
        # T_z=1,  # previously defined
        # sigma=5.67e-11,                                       # previously defined
    )

    return report


def beam_temperature_forced_draught(
        is_forced_draught,

        L_L,
        L_H,
        Q,
        T_o,
        T_f,

        h_eq,
        w_t,
        A_v,
        d_aw,
        lambda_4,
        d_1,
        d_2,
        d_eq,
        C_1,
        C_2,
        C_3,
        C_4,
        u,

        T_0,
        sigma,
):
    report = ExternalSteelTemperatureEngulfedBeam(
        # clause_b_5_1_1_2_lambda_1
        L_L=L_L,
        L_H=L_H,
        h_eq=h_eq,
        d_aw=d_aw,
        lambda_4=lambda_4,
        d_1=d_1,
        is_forced_draught=is_forced_draught,

        # clause_b_5_1_1_2_lambda_2
        # L_L=1,                                                # previously defined
        # d_aw=1,                                               # previously defined
        d_2=d_2,
        # h_eq=1,                                               # previously defined
        # lambda_1=1,                                           # previously calculated
        # is_forced_draught=False,                              # previously defined

        # clause_b_5_1_1_2_lambda_3
        # L_H=1,                                                # previously defined
        # L_L=1,                                                # previously defined
        # lambda_4=1,                                           # previously defined
        # d_aw=1,                                               # previously defined
        # h_eq=1,                                               # previously defined
        # d_1=1,                                                # previously defined
        # d_2=1,                                                # previously defined
        # is_forced_draught=False,                              # previously defined

        # Calculate L_x_1
        # h_eq=1,
        # L_L=1,
        # L_H=1,
        # d_1=1,
        # d_aw=1,
        # lambda_4=1,
        # is_forced_draught=1,

        # Calculate T_x_1 ()

        # clause_b_1_4_1_phi_f_i_beam
        # h_eq=1,                                               # previously defined
        # w_t=1,                                                # previously defined
        # d_aw=1,                                               # previously defined
        # lambda_3=1,                                           # previously defined
        # lambda_4=1,                                           # previously defined

        # clause_b_5_2_1_epsilon_z_i
        # lambda_1=1,                                           # previously defined
        # lambda_2=1,                                           # previously calculated
        # lambda_3=1,                                           # previously calculated
        # lambda_4=1,                                           # previously defined

        # clause_b_1_4_1_phi_f
        phi_f=None,
        C_1=C_1,
        C_2=C_2,
        C_3=C_3,
        C_4=C_4,
        # phi_f_1=1,                                            # previously calculated
        # phi_f_2=1,                                            # previously calculated
        # phi_f_3=1,                                            # previously calculated
        # phi_f_4=1,                                            # previously calculated
        # d_1=1,                                                # previously defined
        # d_2=1,                                                # previously defined

        # clause_b_5_1_2_2_I_z_i
        # C_1=1,                                                # previously defined
        # C_2=1,                                                # previously defined
        # C_3=1,                                                # previously defined
        # C_4=1,                                                # previously defined
        # epsilon_z_1=1,                                        # previously calculated
        # epsilon_z_2=1,                                        # previously calculated
        # epsilon_z_3=1,                                        # previously calculated
        # epsilon_z_4=1,                                        # previously calculated
        sigma=sigma,
        # T_z_1=1,  # previously calculated
        # T_z_2=1,  # previously calculated
        T_o=T_o,

        # clause_b_5_1_2_4_I_z_i
        # C_1=1,                                                # previously defined
        # C_3=1,                                                # previously defined
        # C_4=1,                                                # previously defined
        # epsilon_z_1=1,                                        # previously calculated
        # epsilon_z_3=1,                                        # previously calculated
        # epsilon_z_4=1,                                        # previously calculated
        # sigma=1,                                              # previously defined
        # T_z_1=1,                                              # previously defined
        # T_o=1,                                                # previously defined
        # d_2=1,
        # T_x=1,  # according to B.5.1.24)

        # clause_b_5_1_3_2_I_z_i
        # C_1, C_2, C_3, C_4,									# derived
        # epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4, 	# derived
        # sigma=1,                                              # previously defined
        # T_z_1, T_z_2,											# derived
        # T_o=1,                                                # previously defined

        # clause_b_1_3_5_I_f_i
        # phi_f_1, phi_f_2, phi_f_3, phi_f_4,					# derived
        # epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4,	# derived
        # sigma=1,                                              # previously defined
        T_f=T_f,
        # epsilon_f=1,

        # clause_b_4_1_12_alpha_c
        d_eq=d_eq,
        # Q=1,                                                  # previously defined
        # A_v=1,                                                # previously defined

        # clause_b_4_2_11_alpha_c
        # d_eq=1,                                               # previously defined
        # A_v=1,                                                # previously defined
        # Q=1,                                                  # previously defined
        u=u,

        # clause_b_1_3_3_T_m_i_beam
        # I_z_1, I_z_2, I_z_3, I_z_4,							# derived
        # I_f_1, I_f_2, I_f_3, I_f_4,							# derived
        # alpha=0.03,                                           # derived
        # T_z_1, T_z_2,											# derived
        # sigma=5.67e-11,                                       # previously defined

        # clause_b_5_3_a_z
        a_z=None,
        # lambda_1=1,                                           # previously defined

        # clause_b_1_3_5_I_f
        I_f=None,
        # phi_f=1,
        # a_z=1,
        # sigma=1,                                              # previously defined
        # T_f=1,                                                # previously defined
        # epsilon_f=1,                                          # previously defined

        # clause_b_4_1_I_z
        I_z=None,
        # C_1, C_2, C_3, C_4,									# derived
        # I_z_1, I_z_2, I_z_3, I_z_4,							# derived
        # d_1=1,                                                # previously defined
        # d_2=1,                                                # previously defined

        # clause_b_4_1_10_T_z
        T_z=None,
        # T_z = 1000+293.15,
        # T_w=1,
        # L_x=1,
        w_t=w_t,
        Q=Q,
        # T_0=1,

        # clause_b_1_3_3_T_m
        T_m=None,
        # I_z=1,
        # I_f=1,
        # alpha=1,                                              # previously defined
        # T_z=1,  # previously defined
        # sigma=5.67e-11,                                       # previously defined

        T_0=T_0,
        A_v=A_v,
    )

    return report


def column_temperature_forced_draught(
        # condition
        is_forced_draught,

        # fire parameters
        L_L,
        L_H,
        T_o,
        T_f,
        Q,

        # BS EN 1993-1-2 parameters
        A_v,
        w_t,
        h_eq,
        d_1,
        d_2,
        lambda_1,
        lambda_3,
        d_eq,
        C_1,
        C_2,
        C_3,
        C_4,

        # constants
        sigma,
        T_0,
        u,

):
    report = ExternalSteelTemperatureFullyEngulfedColumn(
        # clause_b_4_1_lambda_2
        w_t=w_t,
        lambda_1=lambda_1,  # (w_t - d_2) / 2
        d_2=d_2,

        # clause_b_4_1_lambda_4
        lambda_3=lambda_3,
        L_L=L_L,
        L_H=L_H,
        h_eq=h_eq,
        d_1=d_1,
        is_forced_draught=is_forced_draught,

        # clause_b_4_5_l
        # h_eq=1,                                               # previously defined
        # L_H=1,                                                # previously defined
        # L_L=1,                                                # previously defined
        # lambda_3=1,                                           # previously defined
        # d_1=1,                                                # previously defined
        # is_forced_draught=1,                                  # previously defined

        # clause_b_4_2_epsilon_z_i
        # lambda_1=1,                                           # previously calculated
        # lambda_2=1,                                           # previously calculated
        # lambda_3=1,                                           # previously defined
        # lambda_4=1,                                           # previously calculated

        # clause_b_4_5_l
        # h_eq=1,                                               # previously defined
        # L_H=1,                                                # previously defined
        # L_L=1,                                                # previously defined
        # d_1=1,                                                # previously defined
        # is_forced_draught=1,                                  # previously defined

        # clause_b_4_2_9_T_z
        # L_x,                                                  # previously calculated
        # Q,                                                    # previously defined
        # A_v,                                                  # previously defined
        # T_w,                                                  # previously defined
        T_0=T_0,

        # clause_b_4_1_I_z_i
        C_1=C_1,
        C_2=C_2,
        C_3=C_3,
        C_4=C_4,
        # epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4,   # previously derived
        sigma=sigma,
        # T_z=1,                                                # previously calculated
        T_o=T_o,

        # clause_b_1_4_1_phi_f_i_column
        # h_eq=1,                                               # previously defined
        # d_2=1,                                                # previously defined
        # lambda_1=1,                                           # previously defined
        # lambda_2=1,                                           # previously calculated
        # lambda_3=1,                                           # previously defined
        # previously defined

        # clause_b_1_3_5_I_f_i
        # phi_f_1, phi_f_2, phi_f_3, phi_f_4,                   # previously calculated
        # epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4,   # previously calculated
        # sigma=5.67e-11,                                       # previously defined
        T_f=T_f,
        # epsilon_f=1,                                          # previously calculated

        # clause_b_4_1_12_alpha_c
        d_eq=d_eq,
        Q=Q,
        A_v=A_v,

        # clause_b_1_3_3_T_m_i_column
        # I_z_1, I_z_2, I_z_3, I_z_4,                           # previously calculated
        # I_f_1, I_f_2, I_f_3, I_f_4,                           # previously calculated
        # alpha=1,                                              # previously calculated
        # T_z=1,                                                # previously defined
        # sigma = 5.67e-11,                                     # previously defined

        # clause_b_4_1_I_z
        I_z=None,
        # C_1, C_2, C_3, C_4,                                   # previously defined
        # I_z_1, I_z_2, I_z_3, I_z_4,                           # previously calculated
        # d_1,                                                  # previously defined
        # d_2=1,                                                # previously defined

        # clause_b_1_4_1_phi_f
        phi_f=None,
        # C_1, C_2, C_3, C_4,                                   # previously defined
        # phi_f_1, phi_f_2, phi_f_3, phi_f_4,                   # previously calculated
        # d_1, d_2,                                             # previously defined

        # clause_b_4_6_a_z
        a_z=None,
        # epsilon_z_1=1,                                        # previously calculated
        # epsilon_z_2=1,                                        # previously calculated
        # epsilon_z_3=1,                                        # previously calculated

        # clause_b_1_3_5_I_f
        I_f=None,
        # phi_f=1,                                              # previously calculated
        # a_z=1,                                                # previously calculated
        # sigma=5.67e-11,                                       # previously defined
        # T_f=1,                                                # previously defined
        # epsilon_f = 1,                                        # previously calculated

        # clause_b_1_3_3_T_m
        T_m=None,
        # I_z=1,                                                # previously calculated
        # I_f=1,                                                # previously calculated
        # alpha=1,                                              # previously calculated
        # T_z=1,                                                # previously defined
        # sigma = 5.67e-11,                                     # previously defined

        u=u,
    )

    return report


def column_temperature_no_forced_draught(
        is_forced_draught,

        L_L,
        L_H,
        Q,
        T_o,
        T_f,

        A_v,
        w_t,
        h_eq,
        d_eq,
        lambda_1,
        lambda_3,
        d_1,
        d_2,
        C_1,
        C_2,
        C_3,
        C_4,

        sigma,
        T_0,
):
    report = ExternalSteelTemperatureFullyEngulfedColumn(
        # clause_b_4_1_lambda_2
        w_t=w_t,
        lambda_1=lambda_1,  # (w_t - d_2) / 2
        d_2=d_2,

        # clause_b_4_1_lambda_4
        lambda_3=lambda_3,
        L_L=L_L,
        L_H=L_H,
        h_eq=h_eq,
        d_1=d_1,
        is_forced_draught=is_forced_draught,

        # clause_b_4_5_l
        # h_eq=1,                                               # previously defined
        # L_H=1,                                                # previously defined
        # L_L=1,                                                # previously defined
        # lambda_3=1,                                           # previously defined
        # d_1=1,                                                # previously defined
        # is_forced_draught=1,                                  # previously defined

        # clause_b_4_2_epsilon_z_i
        # lambda_1=1,                                           # previously calculated
        # lambda_2=1,                                           # previously calculated
        # lambda_3=1,                                           # previously defined
        # lambda_4=1,                                           # previously calculated

        # clause_b_4_5_l
        # h_eq=1,                                               # previously defined
        # L_H=1,                                                # previously defined
        # L_L=1,                                                # previously defined
        # d_1=1,                                                # previously defined
        # is_forced_draught=1,                                  # previously defined

        # clause_b_4_2_9_T_z
        # L_x,                                                  # previously calculated
        # Q,                                                    # previously defined
        # A_v,                                                  # previously defined
        # T_w,                                                  # previously defined
        T_0=T_0,

        # clause_b_4_1_I_z_i
        C_1=C_1,
        C_2=C_2,
        C_3=C_3,
        C_4=C_4,
        # epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4,   # previously derived
        sigma=sigma,
        # T_z=1,                                                # previously calculated
        T_o=T_o,

        # clause_b_1_4_1_phi_f_i_column
        # h_eq=1,                                               # previously defined
        # d_2=1,                                                # previously defined
        # lambda_1=1,                                           # previously defined
        # lambda_2=1,                                           # previously calculated
        # lambda_3=1,                                           # previously defined
        # previously defined

        # clause_b_1_3_5_I_f_i
        # phi_f_1, phi_f_2, phi_f_3, phi_f_4,                   # previously calculated
        # epsilon_z_1, epsilon_z_2, epsilon_z_3, epsilon_z_4,   # previously calculated
        # sigma=5.67e-11,                                       # previously defined
        T_f=T_f,
        # epsilon_f=1,                                          # previously calculated

        # clause_b_4_1_12_alpha_c
        d_eq=d_eq,
        Q=Q,
        A_v=A_v,

        # clause_b_1_3_3_T_m_i_column
        # I_z_1, I_z_2, I_z_3, I_z_4,                           # previously calculated
        # I_f_1, I_f_2, I_f_3, I_f_4,                           # previously calculated
        # alpha=1,                                              # previously calculated
        # T_z=1,                                                # previously defined
        # sigma = 5.67e-11,                                     # previously defined

        # clause_b_4_1_I_z
        I_z=None,
        # C_1, C_2, C_3, C_4,                                   # previously defined
        # I_z_1, I_z_2, I_z_3, I_z_4,                           # previously calculated
        # d_1,                                                  # previously defined
        # d_2=1,                                                # previously defined

        # clause_b_1_4_1_phi_f
        phi_f=None,
        # C_1, C_2, C_3, C_4,                                   # previously defined
        # phi_f_1, phi_f_2, phi_f_3, phi_f_4,                   # previously calculated
        # d_1, d_2,                                             # previously defined

        # clause_b_4_6_a_z
        a_z=None,
        # epsilon_z_1=1,                                        # previously calculated
        # epsilon_z_2=1,                                        # previously calculated
        # epsilon_z_3=1,                                        # previously calculated

        # clause_b_1_3_5_I_f
        I_f=None,
        # phi_f=1,                                              # previously calculated
        # a_z=1,                                                # previously calculated
        # sigma=5.67e-11,                                       # previously defined
        # T_f=1,                                                # previously defined
        # epsilon_f = 1,                                        # previously calculated

        # clause_b_1_3_3_T_m
        T_m=None,
        # I_z=1,                                                # previously calculated
        # I_f=1,                                                # previously calculated
        # alpha=1,                                              # previously calculated
        # T_z=1,                                                # previously defined
        # sigma = 5.67e-11,                                     # previously defined
    )

    return report


def travelling_fire(print_pdf=False):
    # beams perpendicular 0.875, parallel 1
    # columns parallel 0.65, 0.875
    import numpy as np
    import os

    fake_modules = [os, np]

    try:
        from fsetools.tests.test_fse_ec_external_steel_fleet_st_dirwork import dirwork
    except ModuleNotFoundError:
        dirwork = ''

    def print_outputs(report, heading: str, params: list):
        print('\n' + heading)
        for k in params:
            print(f'{k + ":":<10}{report.output_kwargs[k]:g}')

    def print_reduction_factors(heading: str = None, *reports):
        if heading:
            print('\n' + heading)

        reduction_factors = np.zeros(shape=(4, len(reports)))
        for i, v in enumerate(['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4']):
            for j, report in enumerate(reports):
                reduction_factors[i, j] = report.output_kwargs[v] / max(report.output_kwargs['T_f'], report.output_kwargs['T_o'])

        print(reduction_factors)
        print(reduction_factors[:, np.argmax(np.max(reduction_factors, axis=0))])

    # Common parameters
    W_1 = 9.0
    W_2 = 12.3
    H = 3.05
    A_f = W_1 * W_2
    A_t = 2 * (W_1 * W_2 + W_2 * H + H * W_1)

    h_eq = 3.05
    w_t = 9.0
    A_v = h_eq * w_t

    q_fd = 396.9

    # Calculation

    report_flame_no_forced_draught = flame_no_forced_draught(
        W_1=W_1,
        W_2=W_2,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        A_f=A_f,
        q_fd=q_fd,
        tau_F=1200,
        O=(h_eq ** 0.5) * A_v / A_t,
        h_eq=h_eq,
        A_t=A_t,
        w_t=w_t,
        is_wall_above_opening=True,
    )

    report_flame_forced_draught = flame_forced_draught(
        W_1=W_1,
        W_2=W_2,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        A_f=A_f,
        q_fd=q_fd,
        tau_F=1200,
        A_t=A_t,
        T_0=293.15,
        h_eq=h_eq,
        u=6,
        w_t=w_t,
    )

    report_beam_temperature_no_forced_draught = beam_temperature_no_forced_draught(
        is_forced_draught=False,

        L_L=report_flame_no_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_no_forced_draught.output_kwargs['L_H'],
        Q=report_flame_no_forced_draught.output_kwargs['Q'],
        T_o=report_flame_no_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_no_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_aw=-0.325,
        lambda_4=0.618,
        d_1=0.875,
        d_2=1.,
        d_eq=(0.875 + 1.) / 2.,
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,

        sigma=5.67e-11,
    )

    report_beam_temperature_forced_draught = beam_temperature_forced_draught(
        is_forced_draught=True,

        L_L=report_flame_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_forced_draught.output_kwargs['L_H'],
        Q=report_flame_forced_draught.output_kwargs['Q'],
        T_o=report_flame_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_aw=-0.325,
        lambda_4=0.618,
        d_1=0.875,
        d_2=1.,
        d_eq=(0.875 + 1.) / 2.,
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        u=6,

        T_0=293.15,
        sigma=5.67e-11,
    )

    report_column_temperature_no_forced_draught = column_temperature_no_forced_draught(
        is_forced_draught=False,

        L_L=report_flame_no_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_no_forced_draught.output_kwargs['L_H'],
        Q=report_flame_no_forced_draught.output_kwargs['Q'],
        T_o=report_flame_no_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_no_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_eq=(0.875 + 0.65) / 2.,
        lambda_1=(8.659 - 0.65) / 2,  # (w_t - d_2) / 2
        lambda_3=0.618,
        d_1=0.875,
        d_2=0.65,

        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,

        sigma=5.67e-11,
        T_0=293.15,
    )

    report_column_temperature_forced_draught = column_temperature_forced_draught(
        is_forced_draught=True,

        L_L=report_flame_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_forced_draught.output_kwargs['L_H'],
        Q=report_flame_forced_draught.output_kwargs['Q'],
        T_o=report_flame_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_1=0.875,
        d_2=0.65,
        lambda_1=(8.659 - 0.65) / 2,  # (w_t - d_2) / 2
        lambda_3=0.618,
        d_eq=(0.875 + 0.65) / 2.,
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        u=6,

        sigma=5.67e-11,
        T_0=293.15,
    )

    print_outputs(report_flame_no_forced_draught, heading='non forced draught fire', params=['L_L', 'L_H', 'L_f', 'Q', 'T_f', 'T_w'])
    print_outputs(report_flame_forced_draught, heading='forced draught fire', params=['L_L', 'L_H', 'L_f', 'Q', 'T_f', 'T_w'])
    print_outputs(report_beam_temperature_no_forced_draught, heading='beam in non forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])
    print_outputs(report_beam_temperature_forced_draught, heading='beam in forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])
    print_outputs(report_column_temperature_no_forced_draught, heading='column in non forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])
    print_outputs(report_column_temperature_forced_draught, heading='column in forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])

    print_reduction_factors('beam reduction factors', report_beam_temperature_no_forced_draught, report_beam_temperature_forced_draught)
    print_reduction_factors('column reduction factors', report_column_temperature_no_forced_draught, report_column_temperature_forced_draught)

    # report_flame_no_forced_draught.make_pdf_web()
    # report_flame_forced_draught.make_pdf_web()
    # report_beam_temperature_no_forced_draught.make_pdf_web()
    # report_beam_temperature_forced_draught.make_pdf_web()
    # report_column_temperature_no_forced_draught.make_pdf_web()
    # report_column_temperature_forced_draught.make_pdf_web()

    report = Report(
        sections=report_flame_no_forced_draught.make_latex_sections() +
                 report_flame_forced_draught.make_latex_sections() +
                 report_beam_temperature_no_forced_draught.make_latex_sections() +
                 report_beam_temperature_forced_draught.make_latex_sections() +
                 report_column_temperature_no_forced_draught.make_latex_sections() +
                 report_column_temperature_forced_draught.make_latex_sections(),
        sec_title_prefix='C.'
    )

    if print_pdf:
        report.make_pdf(os.path.join(dirwork, '03.pdf'), fp_pdf_viewer='sumatrapdf')
        # report_flame_no_forced_draught.make_pdf(os.path.join(dirwork, '03a flame (no forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_flame_forced_draught.make_pdf(os.path.join(dirwork, '03b flame (forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_beam_temperature_no_forced_draught.make_pdf(os.path.join(dirwork, '03c beam (no forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_beam_temperature_forced_draught.make_pdf(os.path.join(dirwork, '03d beam (forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_column_temperature_no_forced_draught.make_pdf(os.path.join(dirwork, '03e column (no forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_column_temperature_forced_draught.make_pdf(os.path.join(dirwork, '03f column (forced draught).pdf'), fp_pdf_viewer='sumatrapdf')

    pass


def parametric_fire_1(print_pdf=False):
    # beams perpendicular 0.875, parallel 1
    # columns parallel 0.65, 0.875
    import numpy as np
    import os

    fake_modules = [os, np]

    try:
        from fsetools.tests.test_fse_ec_external_steel_fleet_st_dirwork import dirwork
    except ModuleNotFoundError:
        dirwork = ''

    def print_outputs(report, heading: str, params: list):
        print('\n' + heading)
        for k in params:
            print(f'{k + ":":<10}{report.output_kwargs[k]:g}')

    def print_reduction_factors(heading: str = None, *reports):
        if heading:
            print('\n' + heading)

        reduction_factors = np.zeros(shape=(4, len(reports)))
        for i, v in enumerate(['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4']):
            for j, report in enumerate(reports):
                reduction_factors[i, j] = report.output_kwargs[v] / max(report.output_kwargs['T_f'], report.output_kwargs['T_o'])

        print(reduction_factors)
        print(reduction_factors[:, np.argmax(np.max(reduction_factors, axis=0))])

    # Common parameters
    W_1 = 9.55
    W_2 = 6.36
    H = 3.05
    A_f = W_1 * W_2
    A_t = 2 * (W_1 * W_2 + W_2 * H + H * W_1)

    h_eq = 3.05
    w_t = 1.27
    A_v = h_eq * w_t

    q_fd = 287.81

    # Calculation

    report_flame_no_forced_draught = flame_no_forced_draught(
        W_1=W_1,
        W_2=W_2,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        A_f=A_f,
        q_fd=q_fd,
        tau_F=1200,
        O=(h_eq ** 0.5) * A_v / A_t,
        h_eq=h_eq,
        A_t=A_t,
        w_t=w_t,
        is_wall_above_opening=True,
    )

    report_flame_forced_draught = flame_forced_draught(
        W_1=W_1,
        W_2=W_2,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        A_v1=A_v,
        A_f=A_f,
        q_fd=q_fd,
        tau_F=1200,
        A_t=A_t,
        T_0=293.15,
        h_eq=h_eq,
        u=6,
        w_t=w_t,
    )

    report_beam_temperature_no_forced_draught = beam_temperature_no_forced_draught(
        is_forced_draught=False,

        L_L=report_flame_no_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_no_forced_draught.output_kwargs['L_H'],
        Q=report_flame_no_forced_draught.output_kwargs['Q'],
        T_o=report_flame_no_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_no_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_aw=-0.325,
        lambda_4=0.618,
        d_1=0.875,
        d_2=1.,
        d_eq=(0.875 + 1.) / 2.,
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,

        sigma=5.67e-11,
    )

    report_beam_temperature_forced_draught = beam_temperature_forced_draught(
        is_forced_draught=True,

        L_L=report_flame_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_forced_draught.output_kwargs['L_H'],
        Q=report_flame_forced_draught.output_kwargs['Q'],
        T_o=report_flame_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_aw=-0.325,
        lambda_4=0.618,
        d_1=0.875,
        d_2=1.,
        d_eq=(0.875 + 1.) / 2.,
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        u=6,

        T_0=293.15,
        sigma=5.67e-11,
    )

    report_column_temperature_no_forced_draught = column_temperature_no_forced_draught(
        is_forced_draught=False,

        L_L=report_flame_no_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_no_forced_draught.output_kwargs['L_H'],
        Q=report_flame_no_forced_draught.output_kwargs['Q'],
        T_o=report_flame_no_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_no_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_eq=(0.875 + 0.65) / 2.,
        lambda_1=(w_t - 0.65) / 2,  # (w_t - d_2) / 2
        lambda_3=0.618,
        d_1=0.875,
        d_2=0.65,

        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,

        sigma=5.67e-11,
        T_0=293.15,
    )

    report_column_temperature_forced_draught = column_temperature_forced_draught(
        is_forced_draught=True,

        L_L=report_flame_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_forced_draught.output_kwargs['L_H'],
        Q=report_flame_forced_draught.output_kwargs['Q'],
        T_o=report_flame_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_1=0.875,
        d_2=0.65,
        lambda_1=(w_t - 0.65) / 2,  # (w_t - d_2) / 2
        lambda_3=0.618,
        d_eq=(0.875 + 0.65) / 2.,
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        u=6,

        sigma=5.67e-11,
        T_0=293.15,
    )

    print_outputs(report_flame_no_forced_draught, heading='non forced draught fire', params=['L_L', 'L_H', 'L_f', 'Q', 'T_f', 'T_w'])
    print_outputs(report_flame_forced_draught, heading='forced draught fire', params=['L_L', 'L_H', 'L_f', 'Q', 'T_f', 'T_w'])
    print_outputs(report_beam_temperature_no_forced_draught, heading='beam in non forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])
    print_outputs(report_beam_temperature_forced_draught, heading='beam in forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])
    print_outputs(report_column_temperature_no_forced_draught, heading='column in non forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])
    print_outputs(report_column_temperature_forced_draught, heading='column in forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])

    print_reduction_factors('beam reduction factors', report_beam_temperature_no_forced_draught, report_beam_temperature_forced_draught)
    print_reduction_factors('column reduction factors', report_column_temperature_no_forced_draught, report_column_temperature_forced_draught)

    # report_flame_no_forced_draught.make_pdf_web()
    # report_flame_forced_draught.make_pdf_web()
    # report_beam_temperature_no_forced_draught.make_pdf_web()
    # report_beam_temperature_forced_draught.make_pdf_web()
    # report_column_temperature_no_forced_draught.make_pdf_web()
    # report_column_temperature_forced_draught.make_pdf_web()

    report = Report(
        sections=report_flame_no_forced_draught.make_latex_sections() +
                 report_flame_forced_draught.make_latex_sections() +
                 report_beam_temperature_no_forced_draught.make_latex_sections() +
                 report_beam_temperature_forced_draught.make_latex_sections() +
                 report_column_temperature_no_forced_draught.make_latex_sections() +
                 report_column_temperature_forced_draught.make_latex_sections(),
        sec_title_prefix='A.'
    )

    if print_pdf:
        report.make_pdf(os.path.join(dirwork, '01.pdf'), fp_pdf_viewer='sumatrapdf')
        # report_flame_no_forced_draught.make_pdf(os.path.join(dirwork, '01a flame (no forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_flame_forced_draught.make_pdf(os.path.join(dirwork, '01b flame (forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_beam_temperature_no_forced_draught.make_pdf(os.path.join(dirwork, '01c beam (no forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_beam_temperature_forced_draught.make_pdf(os.path.join(dirwork, '01d beam (forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_column_temperature_no_forced_draught.make_pdf(os.path.join(dirwork, '01e column (no forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_column_temperature_forced_draught.make_pdf(os.path.join(dirwork, '01f column (forced draught).pdf'), fp_pdf_viewer='sumatrapdf')


def parametric_fire_2(print_pdf=False):
    # beams perpendicular 0.875, parallel 1
    # columns parallel 0.65, 0.875
    import numpy as np
    import os

    fake_modules = [os, np]

    try:
        from fsetools.tests.test_fse_ec_external_steel_fleet_st_dirwork import dirwork
    except ModuleNotFoundError:
        dirwork = ''

    def print_outputs(report, heading: str, params: list):
        print('\n' + heading)
        for k in params:
            print(f'{k + ":":<10}{report.output_kwargs[k]:g}')

    def print_reduction_factors(heading: str = None, *reports):
        if heading:
            print('\n' + heading)

        reduction_factors = np.zeros(shape=(4, len(reports)))
        for i, v in enumerate(['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4']):
            for j, report in enumerate(reports):
                reduction_factors[i, j] = report.output_kwargs[v] / max(report.output_kwargs['T_f'], report.output_kwargs['T_o'])

        print(reduction_factors)
        print(reduction_factors[:, np.argmax(np.max(reduction_factors, axis=0))])

    # Common parameters
    W_1 = 14.58
    W_2 = 7.04
    H = 3.05
    A_f = W_1 * W_2
    A_t = 2 * (W_1 * W_2 + W_2 * H + H * W_1)

    h_eq = 3.05
    w_t = 6.17
    A_v = h_eq * w_t

    q_fd = 536.16

    # Calculation

    report_flame_no_forced_draught = flame_no_forced_draught(
        W_1=W_1,
        W_2=W_2,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        A_f=A_f,
        q_fd=q_fd,
        tau_F=1200,
        O=(h_eq ** 0.5) * A_v / A_t,
        h_eq=h_eq,
        A_t=A_t,
        w_t=w_t,
        is_wall_above_opening=True,
    )

    report_flame_forced_draught = flame_forced_draught(
        W_1=W_1,
        W_2=W_2,
        is_windows_on_more_than_one_wall=False,
        is_central_core=False,
        A_v1=A_v,
        A_f=A_f,
        q_fd=q_fd,
        tau_F=1200,
        A_t=A_t,
        T_0=293.15,
        h_eq=h_eq,
        u=6,
        w_t=w_t,
    )

    report_beam_temperature_no_forced_draught = beam_temperature_no_forced_draught(
        is_forced_draught=False,

        L_L=report_flame_no_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_no_forced_draught.output_kwargs['L_H'],
        Q=report_flame_no_forced_draught.output_kwargs['Q'],
        T_o=report_flame_no_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_no_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_aw=-0.325,
        lambda_4=0.618,
        d_1=0.875,
        d_2=1.,
        d_eq=(0.875 + 1.) / 2.,
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,

        sigma=5.67e-11,
    )

    report_beam_temperature_forced_draught = beam_temperature_forced_draught(
        is_forced_draught=True,

        L_L=report_flame_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_forced_draught.output_kwargs['L_H'],
        Q=report_flame_forced_draught.output_kwargs['Q'],
        T_o=report_flame_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_aw=-0.325,
        lambda_4=0.618,
        d_1=0.875,
        d_2=1.,
        d_eq=(0.875 + 1.) / 2.,
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        u=6,

        T_0=293.15,
        sigma=5.67e-11,
    )

    report_column_temperature_no_forced_draught = column_temperature_no_forced_draught(
        is_forced_draught=False,

        L_L=report_flame_no_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_no_forced_draught.output_kwargs['L_H'],
        Q=report_flame_no_forced_draught.output_kwargs['Q'],
        T_o=report_flame_no_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_no_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_eq=(0.875 + 0.65) / 2.,
        lambda_1=(w_t - 0.65) / 2,  # (w_t - d_2) / 2
        lambda_3=0.618,
        d_1=0.875,
        d_2=0.65,

        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,

        sigma=5.67e-11,
        T_0=293.15,
    )

    report_column_temperature_forced_draught = column_temperature_forced_draught(
        is_forced_draught=True,

        L_L=report_flame_forced_draught.output_kwargs['L_L'],
        L_H=report_flame_forced_draught.output_kwargs['L_H'],
        Q=report_flame_forced_draught.output_kwargs['Q'],
        T_o=report_flame_forced_draught.output_kwargs['T_w'],
        T_f=report_flame_forced_draught.output_kwargs['T_f'],

        h_eq=h_eq,
        w_t=w_t,
        A_v=A_v,
        d_1=0.875,
        d_2=0.65,
        lambda_1=(w_t - 0.65) / 2,  # (w_t - d_2) / 2
        lambda_3=0.618,
        d_eq=(0.875 + 0.65) / 2.,
        C_1=1,
        C_2=1,
        C_3=1,
        C_4=1,
        u=6,

        sigma=5.67e-11,
        T_0=293.15,
    )

    print_outputs(report_flame_no_forced_draught, heading='non forced draught fire', params=['L_L', 'L_H', 'L_f', 'Q', 'T_f', 'T_w'])
    print_outputs(report_flame_forced_draught, heading='forced draught fire', params=['L_L', 'L_H', 'L_f', 'Q', 'T_f', 'T_w'])
    print_outputs(report_beam_temperature_no_forced_draught, heading='beam in non forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])
    print_outputs(report_beam_temperature_forced_draught, heading='beam in forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])
    print_outputs(report_column_temperature_no_forced_draught, heading='column in non forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])
    print_outputs(report_column_temperature_forced_draught, heading='column in forced draught fire', params=['T_m_1', 'T_m_2', 'T_m_3', 'T_m_4'])

    print_reduction_factors('beam reduction factors', report_beam_temperature_no_forced_draught, report_beam_temperature_forced_draught)
    print_reduction_factors('column reduction factors', report_column_temperature_no_forced_draught, report_column_temperature_forced_draught)

    # report_flame_no_forced_draught.make_pdf_web()
    # report_flame_forced_draught.make_pdf_web()
    # report_beam_temperature_no_forced_draught.make_pdf_web()
    # report_beam_temperature_forced_draught.make_pdf_web()
    # report_column_temperature_no_forced_draught.make_pdf_web()
    # report_column_temperature_forced_draught.make_pdf_web()

    report = Report(
        sections=report_flame_no_forced_draught.make_latex_sections() +
                 report_flame_forced_draught.make_latex_sections() +
                 report_beam_temperature_no_forced_draught.make_latex_sections() +
                 report_beam_temperature_forced_draught.make_latex_sections() +
                 report_column_temperature_no_forced_draught.make_latex_sections() +
                 report_column_temperature_forced_draught.make_latex_sections(),
        sec_title_prefix='B.'
    )

    if print_pdf:
        report.make_pdf(os.path.join(dirwork, '02.pdf'), fp_pdf_viewer='sumatrapdf')
        # report_flame_no_forced_draught.make_pdf(os.path.join(dirwork, '02a flame (no forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_flame_forced_draught.make_pdf(os.path.join(dirwork, '02b flame (forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_beam_temperature_no_forced_draught.make_pdf(os.path.join(dirwork, '02c beam (no forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_beam_temperature_forced_draught.make_pdf(os.path.join(dirwork, '02d beam (forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_column_temperature_no_forced_draught.make_pdf(os.path.join(dirwork, '02e column (no forced draught).pdf'), fp_pdf_viewer='sumatrapdf')
        # report_column_temperature_forced_draught.make_pdf(os.path.join(dirwork, '02f column (forced draught).pdf'), fp_pdf_viewer='sumatrapdf')


if __name__ == '__main__':
    parametric_fire_1(False)
    parametric_fire_2(False)
    travelling_fire(False)

    # parametric_fire_1(True)
    # parametric_fire_2(True)
    # travelling_fire(True)
