from typing import Union

import numpy as np

from ..libstd.pd_7974_1_2019 import eq_10_virtual_origin


def fire_plume_region(Q_dot_conv_kW: float, z: Union[float, np.ndarray]) -> Union[int, np.ndarray]:
    """
    Calculate z/Q**(2/5) and return flame region.

    :param Q_dot_conv_kW: Power in kW.
    :param z: Height in m.
    :return: Flame region (1: 'flame', 2: 'intermittent', or 3: 'plume').
    """
    region_check = z / (Q_dot_conv_kW ** (2 / 5))

    if isinstance(z, np.ndarray):
        regions = np.empty_like(region_check, dtype=int)
        regions[region_check < 0.08] = 0
        regions[(0.08 <= region_check) & (region_check <= 0.2)] = 1
        regions[region_check > 0.2] = 2
        return regions
    else:
        if region_check < 0.08:
            return 0  # 'flame'
        elif region_check > 0.2:
            return 2  # 'plume'
        else:
            return 1  # 'intermittent'


def fire_plume_temperature_rise_centreline(Q_dot_conv_kW: float, z: float, region: int, T_0: float = 293.15, ) -> float:
    """
    Calculate centre-line temperature of a fire plume.

    :param Q_dot_conv_kW: kW, total heat release rate.
    :param z: m, height where the fire plume diameter is measured.
    :param T_0: K, initial temperature.
    :param region: 1, Optional, will be calculated if not provided. 0: flame, 1: intermittent and 2: plume
    :return: Tuple of temperature rise and region check value.
    """
    C = 0.9
    if isinstance(region, np.ndarray):
        k = np.where(region == 0, 6.8, np.where(region == 2, 1.1, np.where(region == 1, 1.9, np.nan)))
        nu = np.where(region == 0, 1 / 2, np.where(region == 2, -1 / 3, np.where(region == 1, 0, np.nan)))
    else:
        if region == 0:  # 'flame':
            k, nu = 6.8, 1 / 2
        elif region == 2:  # 'plume':
            k, nu = 1.1, -1 / 3
        elif region == 1:  # 'intermittent':
            k, nu = 1.9, 0
        else:
            raise ValueError(f'Unrecognised region {region}')
    z_Q_c_factor = z / (Q_dot_conv_kW ** (2 / 5))
    delta_T = (((k / C) ** 2) * (z_Q_c_factor ** ((2 * nu) - 1)) * T_0) / (2 * 9.81)
    return delta_T


def __plume_diameter(Q_dot_kW: float, Q_dot_dd_kW_m2: float, z: float, T_c: float, coeff: float, T_0: float = 293.15):
    """
    Calculate diameter of the plume at a certain height.
    Equation 13.21 in Chapter 51, SFPE Handbook (2017)

    :param Q_dot_kW: kW, total heat release rate.
    :param Q_dot_dd_kW_m2: kW/m2, heat release rate per unit area.
    :param z: m, height where the fire plume diameter is measured.
    :return: Diameter of the plume.
    """
    r = (((Q_dot_kW / Q_dot_dd_kW_m2) / np.pi) ** 0.5)
    z_0 = eq_10_virtual_origin(D=2 * r, Q_dot_kW=Q_dot_kW)
    d = coeff * ((T_c / T_0) ** 0.5) * (z - z_0)
    return d


def plume_diameter_visible(
        Q_dot_kW: float, Q_dot_dd_kW_m2: float, z: float, T_c: float, T_0: float = 293.15
) -> float:
    """
    Calculate diameter of the plume at a certain height.
    Equation 51.54 in Chapter 51, SFPE Handbook (2017)

    :param Q_dot_kW: kW, total heat release rate.
    :param Q_dot_dd_kW_m2: kW/m2, heat release rate per unit area.
    :param z: m, height where the fire plume diameter is measured.
    :return: Diameter of the plume.
    """
    return __plume_diameter(Q_dot_kW, Q_dot_dd_kW_m2, z, T_c, 0.48, T_0)


def plume_diameter_at_50_temperature(
        Q_dot_kW: float, Q_dot_dd_kW_m2: float, z: float, T_c: float, T_0: float = 293.15
) -> float:
    """
    Calculate diameter of the plume at a certain height.
    Equation 13.21 in Chapter 13, SFPE Handbook (2017)

    :param Q_dot_kW: kW, total heat release rate.
    :param Q_dot_dd_kW_m2: kW/m2, heat release rate per unit area.
    :param z: m, height where the fire plume diameter is measured.
    :return: Diameter of the plume.
    """
    return 2 * __plume_diameter(Q_dot_kW, Q_dot_dd_kW_m2, z, T_c, 0.12, T_0)
