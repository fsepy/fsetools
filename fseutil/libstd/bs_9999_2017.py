

def clause_15_6_6_e_merging_flow_1(
        N: float,
        X: float,
        D: float,
        S_up: float,
        W_SE: float,
) -> tuple:
    """Calculates merging flow at final exit level in accordance with Figure 6 (1 of 3) in BD 9999:2017, page 68.
    Merging flow from stair with storey exit at final exit level.
    SI UNITS unless specified.

    :param N: is the number of people served by the final exit level storey exit.
    :param D: is the lesser distance from the final exit level storey exit or the lowest riser from the upward portion of the stair, in metres (m).
    :param S_up: is the stair width for the upward portion of the stair, in millimetres.
    :param W_SE: is the width of the final exit level storey exit, in millimetres.
    :param X: is the minimum door width per person (see 16.6 and Clause 18), in millimetres.
    :return W_FE: is the width of the final exit, in millimetres.
    """

    # convert unit
    S_up *= 1000.  # [m] -> [mm]
    W_SE *= 1000.  # [m] -> [mm]
    X *= 1000.  # [m] -> [mm]

    # calculate exit capacity
    condition_check = False
    if N > 60 and D < 2:
        condition_check = True
        W_FE = S_up + W_SE
    else:
        W_FE = N * X + 0.75 * S_up

    # check against absolute minimum width
    W_FE = max([W_FE, S_up])

    # convert unit
    W_FE /= 1000.  # [mm] -> [m]

    return W_FE, condition_check


def clause_15_6_6_e_merging_flow_2(
        B: float,
        X: float,
        D: float,
        S_up: float,
        S_dn: float,
) -> tuple:
    """Calculates merging flow at final exit level in accordance with Figure 6 (2 of 3) in BD 9999:2017, page 68.
    Merging flow from stair with storey exit at final exit level.
    SI UNITS unless specified.

    :param B: is the number of people served by the stair from below the final exit level.
    :param D: is the lesser distance from the final exit level storey exit or the lowest riser from the upward portion of the stair, in metres (m).
    :param S_up: is the stair width for the upward portion of the stair, in metres.
    :param S_dn: is the stair width for the downward portion of the stair, in metres.
    :param X: is the minimum door width per person (see 16.6 and Clause 18), in metres.
    :return W_FE: is the width of the final exit, in metres.
    """

    # convert unit
    S_up *= 1000.  # [m] -> [mm]
    S_dn *= 1000.  # [m] -> [mm]
    X *= 1000.  # [m] -> [mm]

    # calculate exit capacity
    condition_check = False
    if B > 60 and D < 2:
        condition_check = True
        W_FE = S_up + S_dn
    else:
        W_FE = B * X + 0.75 * S_up

    # check against absolute minimum width
    W_FE = max([W_FE, S_up])

    # convert unit
    W_FE /= 1000.  # [mm] -> [m]

    return W_FE, condition_check


def clause_15_6_6_e_merging_flow_3(
        B: float,
        X: float,
        D: float,
        S_up: float,
        S_dn: float,
        N: float,
        W_SE: float,
) -> tuple:
    """Calculates merging flow at final exit level in accordance with Figure 6 (3 of 3) in BD 9999:2017, page 68.
    Merging flow from stair with storey exit at final exit level.
    SI UNITS unless specified.

    :param B: is the number of people served by the stair from below the final exit level.
    :param N: is the number of people served by the final exit level storey exit.
    :param D: is the lesser distance from the final exit level storey exit or the lowest riser from the upward portion of the stair, in metres (m).
    :param S_up: is the stair width for the upward portion of the stair, in metres.
    :param S_dn: is the stair width for the downward portion of the stair, in metres.
    :param W_SE: is the width of the final exit level storey exit, in metres.
    :param X: is the minimum door width per person (see 16.6 and Clause 18), in metres.
    :return W_FE: is the width of the final exit, in metres.
    """

    # convert unit
    S_up *= 1000.  # [m] -> [mm]
    S_dn *= 1000.  # [m] -> [mm]
    X *= 1000.  # [m] -> [mm]
    W_SE *= 1000.  # [m] -> [mm]

    # calculate exit capacity
    condition_check = False
    if (B + N) > 60 and D < 2:
        condition_check = True
        W_FE = S_up + S_dn + W_SE
    else:
        W_FE = B * X + N * X + 0.75 * S_up

    # check against absolute minimum width
    W_FE = max([W_FE, S_up])

    # convert unit
    W_FE /= 1000.  # [mm] -> [m]

    return W_FE, condition_check


def _test_clause_15_6_6_e_merging_flow_3():

    calculation_result, *_ = clause_15_6_6_e_merging_flow_3(
        B=130,
        X=3.6/1000,
        D=1.9,
        S_up=1.6,
        S_dn=1.2,
        N=30,
        W_SE=1.1,
    )

    pre_calculated_result = 3.9  # 1.6 + 1.2 + 1.1

    assert calculation_result == pre_calculated_result

    calculation_result, *_ = clause_15_6_6_e_merging_flow_3(
        B=15,
        X=3.6/1000,
        D=2.5,
        S_up=1.6,
        S_dn=1.2,
        N=130,
        W_SE=1.1,
    )

    pre_calculated_result = 1.722  # 15 * 3.6 + 130 * 3.6 + 0.75 * 1.6

    assert calculation_result == pre_calculated_result


if __name__ == '__main__':
    _test_clause_15_6_6_e_merging_flow_3()
