from typing import Union

import numpy as np
from scipy.stats import norm

from fsetools.libstd.bs_en_1993_1_2_2005_k_y_theta import clause_3_2_1_1_k_y_theta as k_y_theta


def k_y_theta_prob(theta_a: Union[float, np.ndarray], epsilon_q: Union[float, np.ndarray]):
    k_y_2_T_bar = k_y_theta(theta_a=theta_a)
    k_y_2_T_star = (k_y_2_T_bar + 1e-6) / 1.7
    epsilon = norm.ppf(epsilon_q)

    b1 = np.log(k_y_2_T_star / (1 - k_y_2_T_star))
    b2 = 0.412
    b3 = -0.81e-3 * theta_a
    b4 = 0.58e-6 * (theta_a ** 1.9)
    b5 = 0.43 * epsilon
    b6 = np.exp(b1 + b2 + b3 + b4 + b5)

    k_y_theta_prob_ = (1.7 * b6) / (b6 + 1)
    return k_y_theta_prob_
