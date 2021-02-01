from typing import Union

import numpy as np
import scipy.stats as stats

from fsetools.libstd.bs_en_1993_1_2_2005_mat_prop import clause_3_2_1_1_k_y_theta as k_y_theta


def k_y_theta_prob(theta_a: Union[float, np.ndarray], epsilon_q: Union[float, np.ndarray]):
    k_y_2_T_bar = k_y_theta(theta_a=theta_a)

    k_y_2_T_star = (k_y_2_T_bar + 1e-6) / 1.7

    epsilon = stats.norm.ppf(epsilon_q)

    b1 = np.log(k_y_2_T_star / (1 - k_y_2_T_star))
    b2 = 0.412
    b3 = -0.81e-3 * theta_a
    b4 = 0.58e-6 * (theta_a ** 1.9)
    b5 = 0.43 * epsilon
    b6 = np.exp(b1 + b2 + b3 + b4 + b5)

    k_y_theta_prob_ = (1.7 * b6) / (b6 + 1)

    return k_y_theta_prob_


def func_test():
    T = np.linspace(273.15 + 0, 273.15 + 1500, 5000)
    return T, map(k_y_theta, T)


def func_vector_test():
    T = np.linspace(273.15 + 0, 273.15 + 1500, 5000)
    return T, k_y_theta(T)


def func_prob_vector_test():
    T = np.linspace(273.15 + 0, 273.15 + 1500, 5000)
    q = np.random.random_sample(len(T))
    return T, k_y_theta_prob(T, q)


def _test_probabilistic():
    assert abs(k_y_theta_prob(0., 0.5) - 1.161499) <= 0.00001
    assert abs(k_y_theta_prob(673.15, 0.5) - 1.001560) <= 0.0001


if __name__ == "__main__":
    _test_probabilistic()
    import matplotlib.pyplot as plt
    plt.style.use('seaborn-paper')

    theta_a = np.linspace(273.15 + 0, 273.15 + 1500, 5000)
    print(k_y_theta_prob(673.15, 0.5))

    fig, ax = plt.subplots(figsize=(3.5, 3.5))

    ax.scatter(theta_a - 273.15, k_y_theta_prob(theta_a, np.random.random_sample(len(theta_a))), c="grey", s=1, label="Random Sampled Points")
    ax.plot(theta_a - 273.15, k_y_theta_prob(theta_a, 0.5), "--k", label=r"$\epsilon$ Percentile 0.05, 0.5, 0.95", )
    ax.plot(theta_a - 273.15, k_y_theta_prob(theta_a, 0.05), "--k")
    ax.plot(theta_a - 273.15, k_y_theta_prob(theta_a, 0.95), "--k")
    ax.plot(theta_a - 273.15, k_y_theta(theta_a), "k", label=r"Eurocode $k_{y,\Theta}$")
    ax.set_xlabel(r"Temperature [$^\circ C$]")
    ax.set_ylabel(r"$k_{y,ach}$")

    ax.tick_params(axis='both', which='both', labelsize='xx-small')

    ax.legend(loc=0, fontsize='xx-small').set_visible(True)
    plt.tight_layout()
    plt.show()
