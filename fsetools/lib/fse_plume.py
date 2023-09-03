import math
from typing import Union

import numpy as np


def flame_region(Q_conv_kW: float, z: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Calculate z/Q**(2/5) and return flame region.

    :param Q_conv_kW: Power in kW.
    :param z: Height in m.
    :return: Flame region ('flame', 'plume', or 'intermittent').
    """
    region_check = z / (Q_conv_kW ** (2 / 5))

    if isinstance(z, np.ndarray):
        regions = np.empty_like(region_check)
        regions[region_check < 0.08] = 0.
        regions[(0.08 <= region_check) & (region_check <= 0.2)] = 1.
        regions[region_check > 0.2] = 2.
        return regions
    else:
        if region_check < 0.08:
            return 0.  # 'flame'
        elif region_check > 0.2:
            return 2.  # 'plume'
        else:
            return 1.  # 'intermittent'


def centre_line_temperature(Q_c_kW: float, z: float, T_0: float) -> (float, float):
    """
    Calculate centreline temperature rise.

    :param Q_c_kW: Power in kW.
    :param z: Height in m.
    :param T_0: Initial temperature.
    :return: Tuple of temperature rise and region check value.
    """
    z_Q_c_factor = z / (Q_c_kW ** (2 / 5))
    region = flame_region(Q_c_kW, z)

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

    delta_T = ((k / C) ** 2 * z_Q_c_factor ** ((2 * nu) - 1) * T_0) / (2 * 9.81)
    return delta_T, z_Q_c_factor


def compute_fire_dimensions(Q_c_kW: float, HRRPUA_kW_m2: float, conv_frac: float) -> (float, float):
    """
    Compute fire area and fire radius.

    :param Q_c_kW: Power in kW.
    :param HRRPUA_kW_m2: Heat release rate per unit area in kW/sq.m.
    :param conv_frac: Convective fraction.
    :return: Tuple of fire area and fire radius.
    """
    fire_area = (Q_c_kW / conv_frac) / HRRPUA_kW_m2
    fire_radius = (fire_area / math.pi) ** 0.5
    return fire_area, fire_radius


def plume_diameter(Q_c_kW: float, HRRPUA_kW_m2: float, conv_frac: float, z_0: float, z: float) -> float:
    """
    Calculate diameter of the plume at a certain height.

    :param Q_c_kW: Power in kW.
    :param HRRPUA_kW_m2: Heat release rate per unit area in kW/sq.m.
    :param conv_frac: Convective fraction.
    :param z_0: Virtual origin.
    :return: Diameter of the plume.
    """
    _, fire_radius = compute_fire_dimensions(Q_c_kW, HRRPUA_kW_m2, conv_frac)
    return (fire_radius / (-z_0)) * (z + (z_0 * -1))


def virtual_origin(Q_c_kW: float, HRRPUA_kW_m2: float, conv_frac: float) -> float:
    """
    Calculate virtual origin of the fire.

    :param Q_c_kW: Power in kW.
    :param HRRPUA_kW_m2: Heat release rate per unit area in kW/sq.m.
    :param conv_frac: Convective fraction.
    :return: Virtual origin.
    """
    _, fire_radius = compute_fire_dimensions(Q_c_kW, HRRPUA_kW_m2, conv_frac)
    fire_diameter = 2 * fire_radius
    z_0 = (-1.02 + (Q_c_kW ** (2 / 5)) / fire_diameter * 0.083) * fire_diameter
    return z_0 if z_0 < 0. else 0.
