from .bs_en_1991_1_2_2002_annex_a import *


def test_appendix_a_parametric_fire():
    """This is a test function to `appendix_a_parametric_fire` within this module `fire_parametric_ec`, it compares the function against
    Figure 7 in Holicky, M. et al [1].
    yan fu, 1 oct 2018

    REFERENCES
    [1] Holicky, M., Meterna, A., Sedlacek, G. and Schleich, J.B., 2005. Implementation of eurocodes, handbook 5, design
    of buildings for the appendix_a_parametric_fire situation. Leonardo da Vinci Pilot Project: Luxembourg."""
    import copy

    try:
        from scipy.interpolate import interp1d
        from scipy import stats
    except ImportError:
        raise ImportError('Missing library `scipy`')

    # LOAD VERIFICATION DATA
    # data are extracted from the referenced document

    verification_data = (
        ((20, 30, 40, 50, 60, 70, 80),
         (689.1109391, 782.7282474, 167.4009827, 20, 20, 20, 20)),
        ((20, 30, 40, 50, 60, 70, 80),
         (689.1109391, 782.7317977, 402.4756096, 20, 20, 20, 20)),
        ((20, 30, 40, 50, 60, 70, 80),
         (689.1109391, 782.7317977, 508.8188932, 236.7716603, 20, 20, 20)),
        ((20, 30, 40, 50, 60, 70, 80),
         (843.9616854, 946.9144525, 781.2034026, 540.8761379, 304.2731159, 69.53931579, 20)),
        ((20, 30, 40, 50, 60, 70, 80),
         (741.3497451, 827.5114674, 885.6845648, 818.8612125, 692.3328174, 565.8079725, 441.145249)),
        ((20, 30, 40, 50, 60, 70, 80),
         (601.424372, 726.7651987, 777.4756096, 813.2641976, 843.4522203, 780.3602113, 719.1303236)),
        ((20, 30, 40, 50, 60, 70, 80),
         (269.3348197, 430.1234077, 533.0726245, 604.3089737, 651.2880412, 685.2109576, 709.8019654)),
    )

    # CALCULATE TIME TEMPERATURE CURVE BASED ON THE VERIFICATION DATA INPUTS

    # prepare inputs
    kws = dict(
        A_t=360,
        A_f=100,
        h_eq=1,
        q_fd=600e6,
        lambda_=1,
        rho=1,
        c=2250000,
        t_lim=20 * 60,
        t=np.arange(0, 2 * 60 * 60 + 1, 1),
        temperature_initial=293.15,
    )

    # define opening area
    A_v_list = [72, 50.4, 36.000000001, 32.4, 21.6, 14.4, 7.2]

    # calculate appendix_a_parametric_fire curves
    x1_list = []  # calculated time array
    y1_list = []  # calculated temperature array
    for i in A_v_list:
        y = appendix_a_parametric_fire(A_v=i, **copy.copy(kws))
        x = np.arange(0, 2 * 60 * 60 + 1, 1) + 10 * 60
        x1_list.append(x / 60)
        y1_list.append(y - 273.15)

    # COMPARE CALCULATED AND THE VERIFICATION DATA

    def r_square(x1, y1, x2, y2):

        slope, intercept, r_value, p_value, std_err = stats.linregress(
            y2, interp1d(x1, y1)(x2)
        )
        return r_value ** 2

    for i in range(len(A_v_list)):
        x1 = x1_list[i]
        y1 = y1_list[i]
        vd_ = verification_data[i]
        x2 = vd_[0]
        y2 = vd_[1]
        assert r_square(x1, y1, x2, y2) > 0.99
