from typing import Union

import numpy as np


def clause_3_2_1_3_k_y_theta(theta_a: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Effective yield strength in accordance with Clause 3.2.1 (3).

    :param theta_a: [K] Steel temperature
    :return:        [-] Reduction factor for effective yield strength
    """
    return np.interp(
        theta_a,
        (293.15, 673.15, 773.15, 873.15, 973.15, 1073.15, 1173.15, 1273.15, 1373.15, 1473.15),
        (1, 0.9999999, 0.78, 0.47, 0.23, 0.11, 0.06, 0.04, 0.02, 0)
    )


def clause_3_2_1_3_k_y_theta_reversed(k_y_theta: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    return np.interp(
        k_y_theta,
        (0, 0.02, 0.04, 0.06, 0.11, 0.23, 0.47, 0.78, 0.9999999, 1),
        (1473.15, 1373.15, 1273.15, 1173.15, 1073.15, 973.15, 873.15, 773.15, 673.15, 293.15),
    )


def clause_3_2_1_3_k_p_theta(theta_a: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Effective yield strength in accordance with Clause 3.2.1 (3).

    :param theta_a: [K] Steel temperature
    :return:        [-] Reduction factor for effective yield strength
    """
    return np.interp(
        theta_a,
        (293.15, 373.15, 473.15, 573.15, 673.15, 773.15, 873.15, 973.15, 1073.15, 1173.15, 1273.15, 1373.15, 1473.15),
        (1, 0.9999999, 0.807, 0.613, 0.42, 0.36, 0.18, 0.075, 0.05, 0.0375, 0.025, 0.0125, 0),
    )


def clause_3_2_1_3_k_p_theta_reversed(k_y_theta: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    return np.interp(
        k_y_theta,
        (0, 0.0125, 0.025, 0.0375, 0.05, 0.075, 0.18, 0.36, 0.42, 0.613, 0.807, 0.9999999, 1),
        (1473.15, 1373.15, 1273.15, 1173.15, 1073.15, 973.15, 873.15, 773.15, 673.15, 573.15, 473.15, 373.15, 293.15),
    )


def clause_3_2_1_3_k_E_theta(theta_a: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Effective yield strength in accordance with Clause 3.2.1 (3).

    :param theta_a: [K] Steel temperature
    :return:        [-] Reduction factor for effective yield strength
    """
    return np.interp(
        theta_a,
        (293.15, 373.15, 473.15, 573.15, 673.15, 773.15, 873.15, 973.15, 1073.15, 1173.15, 1273.15, 1373.15, 1473.15),
        (1, 0.9999999, 0.9, 0.8, 0.7, 0.6, 0.31, 0.13, 0.09, 0.0675, 0.045, 0.0225, 0),
    )


def clause_3_2_1_3_k_E_theta_reversed(k_y_theta: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    return np.interp(
        k_y_theta,
        (0, 0.0225, 0.045, 0.0675, 0.09, 0.13, 0.31, 0.6, 0.7, 0.8, 0.9, 0.9999999, 1),
        (1473.15, 1373.15, 1273.15, 1173.15, 1073.15, 973.15, 873.15, 773.15, 673.15, 573.15, 473.15, 373.15, 293.15),
    )


def clause_3_2_1_3_k_y_theta_mod(theta_a: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Effective yield strength in accordance with Clause 3.2.1 (3).

    :param theta_a: [K] Steel temperature
    :return:        [-] Reduction factor for effective yield strength
    """

    if isinstance(theta_a, float):
        if theta_a < 273.15:
            k_y_theta = 1.
        elif theta_a < 673.15:
            k_y_theta = 1.00 + (0.99 - 1.00) / 400 * (theta_a - 273.15)
        elif theta_a <= 773.15:
            k_y_theta = 0.99 + (0.78 - 0.99) / 100 * (theta_a - 673.15)
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
        k_y_theta = np.where(theta_a <= 273.15, 1, 0)
        k_y_theta = np.where((273.15 < theta_a) & (theta_a <= 673.15), 1.00 + (0.99 - 1.00) / 400 * (theta_a - 273.15),
                             k_y_theta)
        k_y_theta = np.where((673.15 < theta_a) & (theta_a <= 773.15), 0.99 + (0.78 - 0.99) / 100 * (theta_a - 673.15),
                             k_y_theta)
        k_y_theta = np.where((773.15 < theta_a) & (theta_a <= 873.15), 0.78 + (0.47 - 0.78) / 100 * (theta_a - 773.15),
                             k_y_theta)
        k_y_theta = np.where((873.15 < theta_a) & (theta_a <= 973.15), 0.47 + (0.23 - 0.47) / 100 * (theta_a - 873.15),
                             k_y_theta)
        k_y_theta = np.where((973.15 < theta_a) & (theta_a <= 1073.15), 0.23 + (0.11 - 0.23) / 100 * (theta_a - 973.15),
                             k_y_theta)
        k_y_theta = np.where((1073.15 < theta_a) & (theta_a <= 1173.15),
                             0.11 + (0.06 - 0.11) / 100 * (theta_a - 1073.15), k_y_theta)
        k_y_theta = np.where((1173.15 < theta_a) & (theta_a <= 1273.15),
                             0.06 + (0.04 - 0.06) / 100 * (theta_a - 1173.15), k_y_theta)
        k_y_theta = np.where((1273.15 < theta_a) & (theta_a <= 1373.15),
                             0.04 + (0.02 - 0.04) / 100 * (theta_a - 1273.15), k_y_theta)
        k_y_theta = np.where((1373.15 < theta_a) & (theta_a <= 1473.15),
                             0.02 + (0.00 - 0.02) / 100 * (theta_a - 1373.15), k_y_theta)
        k_y_theta = np.where(1473.15 < theta_a, 0, k_y_theta)

    else:
        raise TypeError(f'theta_a can be either float or numpy.ndarray type, got {type(theta_a)}')

    return k_y_theta


def clause_3_2_1_3_k_y_theta_mod_reversed(k_y_theta: float):
    T_range = np.arange(273.15, 1200 + 273.15, 0.1)
    k_range = clause_3_2_1_3_k_y_theta_mod(T_range)
    T = T_range[np.argmin(np.abs(k_range - k_y_theta))]
    return T
