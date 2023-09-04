from fsetools.libstd.bs_en_1993_1_2_2005_clause_3 import *


def test_clause_3_2_1_3_k_y_theta():
    for i, j in zip(
            (293.15, 673.15, 773.15, 873.15, 973.15, 1073.15, 1173.15, 1273.15, 1373.15, 1473.15),
            (1, 0.9999999, 0.78, 0.47, 0.23, 0.11, 0.06, 0.04, 0.02, 0)
    ):
        assert abs(clause_3_2_1_3_k_y_theta(i) - j) < 1e-6


def test_clause_3_2_1_3_k_p_theta():
    for i, j in zip(
            (293.15, 373.15, 473.15, 573.15, 673.15, 773.15, 873.15, 973.15, 1073.15, 1173.15, 1273.15, 1373.15,
             1473.15),
            (1, 0.9999999, 0.807, 0.613, 0.42, 0.36, 0.18, 0.075, 0.05, 0.0375, 0.025, 0.0125, 0),
    ):
        assert abs(clause_3_2_1_3_k_p_theta(i) - j) < 1e-6


def test_clause_3_2_1_3_k_E_theta():
    for i, j in zip(
            (293.15, 373.15, 473.15, 573.15, 673.15, 773.15, 873.15, 973.15, 1073.15, 1173.15, 1273.15, 1373.15,
             1473.15),
            (1, 0.9999999, 0.9, 0.8, 0.7, 0.6, 0.31, 0.13, 0.09, 0.0675, 0.045, 0.0225, 0),
    ):
        assert abs(clause_3_2_1_3_k_E_theta(i) - j) < 1e-6


def test_clause_3_2_1_1_k_y_theta_reversed():
    for T in np.arange(400 + 273.15, 1200 + 273.15 + 1, 100):
        a = clause_3_2_1_3_k_y_theta(T)
        b = clause_3_2_1_3_k_y_theta_reversed(a)
        assert abs(T - b) < 1e-6, f'{a}=>{T}!=>{b}'


def test_clause_3_2_1_3_k_p_theta_reversed():
    for T in np.arange(400 + 273.15, 1200 + 273.15 + 1, 100):
        a = clause_3_2_1_3_k_p_theta(T)
        b = clause_3_2_1_3_k_p_theta_reversed(a)
        assert abs(T - b) < 1e-6, f'{a}=>{T}!=>{b}'


def test_clause_3_2_1_3_k_E_theta_reversed():
    for T in np.arange(400 + 273.15, 1200 + 273.15 + 1, 100):
        a = clause_3_2_1_3_k_E_theta(T)
        b = clause_3_2_1_3_k_E_theta_reversed(a)
        assert abs(T - b) < 1e-6, f'{a}=>{T}!=>{b}'


def test_clause_3_2_1_1_k_y_theta_mod_reversed():
    for T in np.arange(0 + 273.15, 1200 + 273.15 + 1, 1):
        a = clause_3_2_1_3_k_y_theta_mod(float(T))
        b = clause_3_2_1_3_k_y_theta_mod_reversed(a)
        print(f'T={T:<10g} k={a:<10g} T={T:<10g}')
        assert abs(T - b) < 1


if __name__ == '__main__':
    test_clause_3_2_1_3_k_y_theta()
    test_clause_3_2_1_3_k_p_theta()
    test_clause_3_2_1_3_k_E_theta()

    test_clause_3_2_1_1_k_y_theta_reversed()
    test_clause_3_2_1_3_k_p_theta_reversed()
    test_clause_3_2_1_3_k_E_theta_reversed()
