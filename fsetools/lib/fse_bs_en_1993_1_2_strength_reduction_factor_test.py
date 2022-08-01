import numpy as np

from fsetools.lib.fse_bs_en_1993_1_2_strength_reduction_factor import k_y_theta_prob
from fsetools.libstd.bs_en_1993_1_2_2005_k_y_theta import clause_3_2_1_1_k_y_theta as k_y_theta


def func_test():
    T = np.linspace(273.15 + 0, 273.15 + 1500, 5000)
    return T, k_y_theta(T)


def func_vector_test():
    T = np.linspace(273.15 + 0, 273.15 + 1500, 5000)
    return T, k_y_theta(T)


def func_prob_vector_test():
    T = np.linspace(273.15 + 0, 273.15 + 1500, 10000)
    q = np.random.random_sample(len(T))
    return T, k_y_theta_prob(T, q)


def probabilistic_test():
    assert abs(k_y_theta_prob(0., 0.5) - 1.161499) <= 0.00001
    assert abs(k_y_theta_prob(673.15, 0.5) - 1.001560) <= 0.0001


def plot_prob_k_y_ach():
    import matplotlib.pyplot as plt
    plt.style.use('seaborn-paper')

    fig, ax = plt.subplots(figsize=(4, 3))
    T = np.linspace(273.15 + 0, 273.15 + 1500, 5000)
    ax.scatter(*func_prob_vector_test(), s=2, color=((0, 0, 0, 0.1)), label='Random Sampled Points')
    ax.plot(T, k_y_theta_prob(T, 0.05), ls='--', c='k', label=r'$\epsilon$ Percentile 0.05, 0.50, 0.95')
    ax.plot(T, k_y_theta_prob(T, 0.5), ls='--', c='k')
    ax.plot(T, k_y_theta_prob(T, 0.95), ls='--', c='k')
    ax.plot(T, k_y_theta(T), ls='-', c='r', label=r'Eurocode $k_{y,\theta}$')

    ax.set_xlabel('Temperature [$^oC$]')
    ax.set_ylabel('$k_{y,ach}$ [$1$]')
    ax.legend().set_visible(True)
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    plot_prob_k_y_ach()
