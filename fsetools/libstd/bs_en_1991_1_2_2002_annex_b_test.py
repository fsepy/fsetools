from fsetools.libstd.bs_en_1991_1_2_2002_annex_b import *


def test_1(raise_error=True):
    """
    Test against analysis carried in report '190702-R00-SC19024-WP1-Flame Projection Calculations-DN-CIC'.
    Wall above opening and no balcony above opening.
    """

    # compulsory user defined parameters
    w_t = 1.82
    h_eq = 1.1
    d_ow = 1e10
    D = 6.681317  # calculated based on floor area 14.88 and D/W = 3
    W = 2.227106  # calculated based on floor area 14.88 and D/W = 3
    W_1 = 1.82
    W_2 = 5.46
    q_fd = 870
    tau_F = 1200
    rho_g = 0.45
    g = 9.81
    T_0 = 293.15

    is_wall_above_opening = True
    is_windows_on_more_than_one_wall = False
    is_central_core = False

    # derived values below
    A_v = w_t * h_eq
    A_f = D * W
    O = 0.03

    kwargs = locals()

    # Calculate D/W
    try:
        kwargs.update(clause_b_2_2_DW_ratio(**kwargs))
    except AssertionError:
        try:
            kwargs.update(clause_b_2_3_DW_ratio(**kwargs))
        except AssertionError:
            kwargs.update(clause_b_2_4_DW_ratio(**kwargs))

    # Calculate heat release rate
    kwargs.update(clause_b_4_1_1_Q(**kwargs))

    # Calculate external flame vertical projection
    kwargs.update(clause_b_4_1_3_L_L(**kwargs))

    # Calculate external flame horizontal projection
    kwargs.update(clause_b_4_1_6_L_H(**kwargs))

    # Modify L_H and L_L
    # todo

    # Calculate flame length
    kwargs.update(clause_b_4_1_7_L_f(**kwargs))

    print(f'{kwargs["L_f"]:.1f} == 1.9')
    assert abs(round(kwargs["L_f"], 1) - 1.9) < 1e-7
