from typing import Optional, Union

import numpy as np

from fsetools.libstd.pd_7974_1_2019 import eq_10_virtual_origin
from fsetools.libstd.pd_7974_1_2019 import eq_14_plume_temperature
from fsetools.libstd.pd_7974_1_2019 import eq_15_plume_velocity
from fsetools.libstd.pd_7974_1_2019 import eq_26_axisymmetric_ceiling_jet_temperature
from fsetools.libstd.pd_7974_1_2019 import eq_27_axisymmetric_ceiling_jet_velocity
from fsetools.libstd.pd_7974_1_2019 import eq_55_activation_of_heat_detector_device


def heat_detector_temperature_pd7974(
        fire_time: Union[np.ndarray, list],
        fire_hrr_kW: Union[np.ndarray, list],
        detector_to_fire_vertical_distance: float,
        detector_to_fire_horizontal_distance: float,
        detector_response_time_index: float,
        detector_conduction_factor: float,
        fire_hrr_density_kWm2: float,
        fire_conv_frac: float,
        ambient_gravity_acceleration: Optional[float] = 9.81,
        ambient_gas_temperature: Optional[float] = 293.15,
        ambient_gas_specific_heat: Optional[float] = 1.2,
        ambient_gas_density: Optional[float] = 1.0,
        force_plume_temperature_correlation: Optional[bool] = False,
        *_, **__
) -> dict:
    """This function calculates heat detector device time - temperature revolution based on specified fire heat release
    rate.

    :param fire_time:
    :param fire_hrr_kW:
    :param detector_to_fire_vertical_distance:
    :param detector_to_fire_horizontal_distance:
    :param detector_response_time_index:
    :param detector_conduction_factor:
    :param fire_hrr_density_kWm2:
    :param fire_conv_frac:
    :param ambient_gas_temperature:
    :param ambient_gas_density:
    :param ambient_gas_specific_heat:
    :param ambient_gravity_acceleration:
    :param force_plume_temperature_correlation:
    :return:
    """

    # refactor with common variable names
    z_H = detector_to_fire_vertical_distance
    r = detector_to_fire_horizontal_distance

    # Check and convert input types
    if isinstance(fire_time, list):
        fire_time = np.array(fire_time)
    if isinstance(fire_hrr_kW, list):
        fire_hrr_kW = np.array(fire_hrr_kW)

    # Validate parameters
    # ===================
    try:
        assert len(fire_time) == len(fire_hrr_kW)
    except AssertionError:
        raise ValueError('Gas time `gas_time` and temperature array `gas_temperature` length do not match.')

    # Result containers
    # =================

    fire_diameter = [((fire_hrr_kW[0] * fire_conv_frac / fire_hrr_density_kWm2) / 3.1415926) ** 0.5 * 2]
    jet_temperature = [ambient_gas_temperature]
    jet_velocity = [0.]
    detector_temperature = [ambient_gas_temperature]
    virtual_origin = [0]

    # Main heat detector temperature calculation starts
    # =================================================

    for i in range(1, len(fire_time), 1):

        # Calculate change in time, dt
        # ----------------------------
        dt = fire_time[i] - fire_time[i - 1]

        # Calculate convective heat release rate
        # --------------------------------------
        Q_dot_c_kW = fire_hrr_kW[i] * fire_conv_frac

        # Calculate fire diameter
        # -----------------------
        D = ((fire_hrr_kW[i] / fire_hrr_density_kWm2) / 3.1415926) ** 0.5 * 2

        # Calculate virtual fire origin
        # -----------------------------
        z_0 = eq_10_virtual_origin(D=D, Q_dot_kW=fire_hrr_kW[i])
        virtual_origin.append(z_0)

        # Calculate ceiling jet temperature
        # ---------------------------------
        if not force_plume_temperature_correlation and (r / (z_H - z_0) > 0.134):
            theta_jet_rise = eq_26_axisymmetric_ceiling_jet_temperature(
                Q_dot_c_kW=Q_dot_c_kW,
                z_H=detector_to_fire_vertical_distance,
                z_0=z_0,
                r=detector_to_fire_horizontal_distance,
            )
        else:
            theta_jet_rise = eq_14_plume_temperature(
                T_0=ambient_gas_temperature,
                g=ambient_gravity_acceleration,
                c_p_0_kJ_kg_K=ambient_gas_specific_heat,
                rho_0=ambient_gas_density,
                Q_dot_c_kW=Q_dot_c_kW,
                z=detector_to_fire_vertical_distance,
                z_0=z_0
            )
        theta_jet = theta_jet_rise + ambient_gas_temperature

        # Calculate ceiling jet velocity
        # ------------------------------
        if not force_plume_temperature_correlation and (r / (z_H - z_0) > 0.246):
            u_jet = eq_27_axisymmetric_ceiling_jet_velocity(
                Q_dot_c_kW=Q_dot_c_kW,
                z_H=detector_to_fire_vertical_distance,
                z_0=z_0,
                r=detector_to_fire_horizontal_distance,
            )
        else:
            u_jet = eq_15_plume_velocity(
                T_0=ambient_gas_temperature,
                g=ambient_gravity_acceleration,
                c_p_0_kJ_kg_K=ambient_gas_specific_heat,
                rho_0=ambient_gas_density,
                Q_dot_c_kW=Q_dot_c_kW,
                z=detector_to_fire_vertical_distance,
                z_0=z_0,
            )

        # Calculate detector temperature
        # ------------------------------
        d_Delta_Te_dt = eq_55_activation_of_heat_detector_device(
            u=u_jet,
            RTI=detector_response_time_index,
            Delta_T_g=theta_jet - ambient_gas_temperature,
            Delta_T_e=detector_temperature[i - 1] - ambient_gas_temperature,
            C=detector_conduction_factor
        )
        d_Delta_Te = d_Delta_Te_dt * dt
        Delta_Te = d_Delta_Te + detector_temperature[i - 1]

        # Record results
        # --------------
        fire_diameter.append(D)
        jet_temperature.append(theta_jet)
        jet_velocity.append(u_jet)
        detector_temperature.append(Delta_Te)

    # Pack up results
    # ===============
    return dict(
        detector_temperature=np.array(detector_temperature),
        jet_temperature=np.array(jet_temperature),
        jet_velocity=np.array(jet_velocity),
        fire_diameter=np.array(fire_diameter),
        virtual_origin=np.array(virtual_origin),
    )
