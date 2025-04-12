def mean_flame_height_pd_7974(
        Q_dot_star: float,
        fuel_type: int,
        fire_diameter: float
):
    """Calculates mean flame height in accordance with Clause 8.3.2 in PD 7974-1:2019

    :param Q_dot_star:  dimensionless heat release rate.
    :param fuel_type:   0   Natural gas 10 cm to 50 cm diameter burner [1]
                        1   10 cm to 200 cm side wood cribs ΔH_c = 18.6 MJ/kg [2]
                        2   Gas, liquids and solids ΔH_c/φ²=3185 kJ/kg of air [3]
    :param fire_diameter: in m, fire source diameter.
    :return flame_height: in m, calculated mean fire height.

    [1] ZUKOSKI E. Fire Safety Science. Proceedings of the First International Symposium on Fire Safety Science, 1984.
    [2] THOMAS P.H. The size of flames from natural fires, Ninth Symposium. The Combustion Institute, 1963.
    [3] HESKESTAD G. Virtual origins of fire plumes. Fire Safety Journal, 5 (2) pp. 109–114, 1983.
    """
    if fuel_type == 0:
        if Q_dot_star < 0.15:
            flame_height = fire_diameter * 40 * Q_dot_star ** 2
        elif Q_dot_star < 1.0:
            flame_height = fire_diameter * 3.3 * Q_dot_star ** (2 / 3)
        elif Q_dot_star < 40:
            flame_height = fire_diameter * 3.3 * Q_dot_star ** (2 / 5)
        else:
            raise AssertionError(
                f'Condition `0 < Q_dot_star < 40` unsatisfied (Q_dot_star={Q_dot_star:.2f}). '
                f'See Table 1 in PD 7974-1:2019.'
            )
    elif fuel_type == 1:
        if 0.75 < Q_dot_star < 8.8:
            flame_height = fire_diameter * 3.4 * Q_dot_star ** 0.61
        else:
            raise AssertionError(
                f'Condition 0.75 < Q_dot_star < 8.8 unsatisfied (Q_dot_star={Q_dot_star:.2f}). '
                f'See Table 1 in PD 7974-1:2019.'
            )
    elif fuel_type == 2:
        if 0.12 < Q_dot_star < 12000:
            flame_height = fire_diameter * (3.7 * Q_dot_star ** (2 / 5) - 1.02)
        else:
            raise AssertionError(
                f'Condition 0.12 < Q_dot_star < 12000 unsatisfied (Q_dot_star={Q_dot_star:.2f}). '
                f'See Table 1 in PD 7974-1:2019.'
            )
    else:
        raise ValueError('Unknown fuel type.')

    return flame_height
