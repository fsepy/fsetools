__all__ = 'radiative_heat_flux_from_fire', 'flame_radiation', 'smoke_radiation'

import numpy as np

from .fse_activation_hd import heat_detector_temperature_pd7974
from ..libstd.bre_br_187_2014 import eq_A4_phi_parallel_corner


# Performance-based external fire spread assessment based on point source methodology in PD 7974-1
# Fire characteristics at time of sprinkler activation


# Radiation due to smoke
def flame_radiation(
        fire_hrr_act_kW: float,
        fire_hrr_density_kWm2: float,
        H: float,
        W_o: float,
        S: float,
        fire_conv_frac: float,
        *_, **__
):  # Convective fraction
    """

    :param fire_hrr_act_kW: Heat release rate at sprinkler activation [kW]
    :param fire_hrr_density_kWm2: Heat release rate per unit area [kW/m²]
    :param H: Height of ceiling [m]
    :param W_o: Width of opening/compartment [m]
    :param S_half: Radial distance from the ceiling impingement point [m]
    :param fire_conv_frac: HRR convective portion [1]
    :return:
    """
    D_f = (4 * (fire_hrr_act_kW / fire_hrr_density_kWm2) / np.pi) ** 0.5
    d_D_ratio = S / D_f
    if d_D_ratio > 2.5:
        model_type = 0
        q = (1 - fire_conv_frac) * fire_hrr_act_kW / (4 * np.pi * np.power(S, 2))
        phi = 1.0  # View factor for a point source is assumed to be 1.0
    else:
        model_type = 1
        H_f = 0.235 * np.power(fire_hrr_act_kW, 2 / 5) - 1.02 * D_f  # Height of flame
        if H_f <= H:  # No flame impingement to the ceiling
            W_e = D_f
        else:  # There is flame impingement to the ceiling
            r_f = 0.95 * (H_f - H)  # Horizontal flame extension [m]
            W_e = max(2 * r_f, D_f)
        W_e = min(W_e, W_o)  # Flame panel width limited to opening/compartment width
        H_e = min(H_f, H)

        # Incident radiation at source due to flame equals half the radiative fraction of HRR at time of sprinkler activation divided by flame panel area
        q = ((1 - fire_conv_frac) * fire_hrr_act_kW / 2) / (W_e * H_e)  # [kw/m²]
        phi = 4 * eq_A4_phi_parallel_corner(W_e / 2, H_e / 2, S)

    q_f = phi * q  # Radiation at receiver due to flame [kw/m²]

    return dict(q_f=q_f, model_type=model_type)


# Radiation due to flame
def smoke_radiation(  # Radiation due to smoke
        smoke_temperature: float,
        epsilon_s: float,
        H: float,
        W_o: float,
        S: float,
        *_, **__
):
    """Calculates the radiation from hot smoke layer

    :param smoke_temperature: [oC] gas/smoke temperature
    :param epsilon_s: [m] emissivity of smoke
    :param H: [m] height of ceiling
    :param W_o: [m] width of opening/compartment
    :param S_half: [m] boundary distance
    :return:
    """
    # todo: fix to SI unit
    q = 5.67e-11 * epsilon_s * (smoke_temperature ** 4 - 293.15 ** 4)  # Incident radiation at source due to smoke
    phi_s = 4 * eq_A4_phi_parallel_corner(W_o / 2, H / 2, S)
    q_s = phi_s * q  # Radiation at receiver due to smoke [kw/m²]
    return dict(q_s=q_s)


def radiative_heat_flux_from_fire(
        fire_duration: float,
        fire_time_step: float,
        fire_hrr_density_kWm2: float,
        fire_alpha,
        detector_to_fire_vertical_distance,
        detector_to_fire_horizontal_distance,
        detector_response_time_index,
        detector_conduction_factor,
        detector_act_temp,
        H, W_o, S,
        fire_conv_frac=0.7,
        epsilon_s=1.0,
        epsilon_f=1.0,
        *_, **__
):
    inputs = locals()
    inputs.pop('_')
    inputs.pop('__')

    inputs['fire_time'] = np.arange(0, fire_duration + fire_time_step / 2, fire_time_step)
    inputs['fire_hrr_kW'] = fire_alpha * inputs['fire_time'] ** 2

    outputs = heat_detector_temperature_pd7974(**inputs)
    if min(outputs['detector_temperature']) < detector_act_temp < max(outputs['detector_temperature']):
        act_index = np.argmin(np.abs(outputs['detector_temperature'] - detector_act_temp))
        outputs['detector_act_time'] = inputs['fire_time'][act_index]
        outputs['fire_hrr_act_kW'] = inputs['fire_hrr_kW'][act_index]
    else:
        raise ValueError(
            f'Heat detector not activated, max and min detector temperature reached {max(outputs["detector_temperature"])}')
    inputs['smoke_temperature'] = outputs['jet_temperature'][act_index]

    # Radiation due to smoke
    outputs.update(smoke_radiation(**inputs, **outputs, ))

    # Radiation due to flame
    outputs.update(flame_radiation(**inputs, **outputs))

    # Total radiation due to combined smoke and flame effect [kW/m²]
    outputs['q'] = outputs['q_s'] + outputs['q_f']

    return outputs
