import numpy as np
from typing import Union


def clause_3_2_1_k_y_theta(theta_a: Union[float, np.ndarray]):

    if isinstance(theta_a, float):
        if theta_a < 673.15:
            k_y_theta = 1
        elif theta_a <= 773.15:
            k_y_theta = 1.00 + (0.78 - 1.00) / 100 * (theta_a - 673.15)
        elif theta_a <= 873.15:
            k_y_theta = 0.78 + (0.47 - 0.78) / 100 * (theta_a - 773.15)
        elif theta_a <= 973.15:
            k_y_theta = 0.47 + (0.23 - 0.47) / 100 * (theta_a - 873.15)
        elif theta_a <= 1073.15:
            k_y_theta = 0.23 + (0.11 - 0.23) / 100 * (theta_a - 973.15)
        elif theta_a <= 1173.15:
            k_y_theta = 0.11 + (0.06 - 0.11) / 100 * (theta_a - 1073.15)
        elif theta_a <= 1273.15:
            k_y_theta = 0.06 + (0.04 - 0.06) / 100 * (theta_a - 1173.15)
        elif theta_a <= 1373.15:
            k_y_theta = 0.04 + (0.02 - 0.04) / 100 * (theta_a - 1273.15)
        elif theta_a <= 1473.15:
            k_y_theta = 0.02 + (0.00 - 0.02) / 100 * (theta_a - 1373.15)
        else:
            k_y_theta = 0.02 + (0.00 - 0.02) / 100 * (theta_a - 1373.15)

    elif isinstance(theta_a, np.ndarray):
        k_y_theta = np.where(theta_a <= 673.15, 1, 0)
        k_y_theta = np.where((673.15 < theta_a) & (theta_a <= 773.15), 1.00 + (0.78 - 1.00) / 100 * (theta_a - 673.15), k_y_theta)
        k_y_theta = np.where((773.15 < theta_a) & (theta_a <= 873.15), 0.78 + (0.47 - 0.78) / 100 * (theta_a - 773.15), k_y_theta)
        k_y_theta = np.where((873.15 < theta_a) & (theta_a <= 973.15), 0.47 + (0.23 - 0.47) / 100 * (theta_a - 873.15), k_y_theta)
        k_y_theta = np.where((973.15 < theta_a) & (theta_a <= 1073.15), 0.23 + (0.11 - 0.23) / 100 * (theta_a - 973.15), k_y_theta)
        k_y_theta = np.where((1073.15 < theta_a) & (theta_a <= 1173.15), 0.11 + (0.06 - 0.11) / 100 * (theta_a - 1073.15), k_y_theta)
        k_y_theta = np.where((1173.15 < theta_a) & (theta_a <= 1273.15), 0.06 + (0.04 - 0.06) / 100 * (theta_a - 1173.15), k_y_theta)
        k_y_theta = np.where((1273.15 < theta_a) & (theta_a <= 1373.15), 0.04 + (0.02 - 0.04) / 100 * (theta_a - 1273.15), k_y_theta)
        k_y_theta = np.where((1373.15 < theta_a) & (theta_a <= 1473.15), 0.02 + (0.00 - 0.02) / 100 * (theta_a - 1373.15), k_y_theta)
        k_y_theta = np.where(1473.15 < theta_a, 0, k_y_theta)

    else:
        raise TypeError(f'theta_a can be either float or numpy.ndarray type, got {type(theta_a)}')

    return k_y_theta
