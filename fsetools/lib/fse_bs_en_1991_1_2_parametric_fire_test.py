import copy

import pandas

from fsetools.lib.fse_bs_en_1991_1_2_parametric_fire import *


def test_appendix_a_parametric_fire():
    """
    Verify against Figure 7, Section 1.2.2 in Holicky, M. et al [1].
    Yan Fu, 1 oct 2018

    REFERENCES
    [1] Holicky, M., Meterna, A., Sedlacek, G. and Schleich, J.B., 2005. Implementation of eurocodes, handbook 5, design
    of buildings for the fire situation. Leonardo da Vinci Pilot Project: Luxembourg.
    """

    # LOAD VERIFICATION DATA
    # data are from the referenced document
    from io import StringIO

    verification_data = StringIO(
        """time_1,temperature_1,time_2,temperature_2,time_3,temperature_3,time_4,temperature_4,time_5,temperature_5,time_6,temperature_6,time_7,temperature_7
        20,689.1109391,20,689.1109391,20,689.1109391,20,843.9616854,20,741.3497451,20,601.424372,20,269.3348197
        30,782.7282474,30,782.7317977,30,782.7317977,30,946.9144525,30,827.5114674,30,726.7651987,30,430.1234077
        40,167.4009827,40,402.4756096,40,508.8188932,40,781.2034026,40,885.6845648,40,777.4756096,40,533.0726245
        50,20,50,20,50,236.7716603,50,540.8761379,50,818.8612125,50,813.2641976,50,604.3089737
        60,20,60,20,60,20,60,304.2731159,60,692.3328174,60,843.4522203,60,651.2880412
        70,20,70,20,70,20,70,69.53931579,70,565.8079725,70,780.3602113,70,685.2109576
        80,20,80,20,80,20,80,20,80,441.145249,80,719.1303236,80,709.8019654"""
    )
    verification_data = pandas.read_csv(
        verification_data, skip_blank_lines=True, skipinitialspace=True
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

    # calculate fire curves
    x1_list = []  # calculated time array
    y1_list = []  # calculated temperature array
    for i in A_v_list:
        y = temperature(A_v=i, **copy.copy(kws))
        x = np.arange(0, 2 * 60 * 60 + 1, 1) + 10 * 60
        x1_list.append(x / 60)
        y1_list.append(y - 273.15)

    # COMPARE CALCULATED AND THE VERIFICATION DATA

    def r_square(x1, y1, x2, y2):
        pass


test_appendix_a_parametric_fire()
