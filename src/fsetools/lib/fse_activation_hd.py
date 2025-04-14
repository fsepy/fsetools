from typing import Optional, Union

import numpy as np

from ..libstd.pd_7974_1_2019 import eq_10_virtual_origin
from ..libstd.pd_7974_1_2019 import eq_14_plume_temperature
from ..libstd.pd_7974_1_2019 import eq_15_plume_velocity
from ..libstd.pd_7974_1_2019 import eq_26_axisymmetric_ceiling_jet_temperature
from ..libstd.pd_7974_1_2019 import eq_27_axisymmetric_ceiling_jet_velocity
from ..libstd.pd_7974_1_2019 import eq_55_activation_of_heat_detector_device


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
) -> tuple:
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

    fire_diameter = np.zeros_like(fire_time, dtype=float)
    jet_temperature = np.zeros_like(fire_time, dtype=float)
    jet_velocity = np.zeros_like(fire_time, dtype=float)
    detector_temperature = np.zeros_like(fire_time, dtype=float)
    virtual_origin = np.zeros_like(fire_time, dtype=float)
    air_type_arr = np.zeros_like(fire_time, dtype=int)

    # assign initial conditions
    fire_diameter[0] = ((fire_hrr_kW[0] * fire_conv_frac / fire_hrr_density_kWm2) / 3.1415926) ** 0.5 * 2
    jet_temperature[0] = ambient_gas_temperature
    detector_temperature[0] = ambient_gas_temperature
    air_type_arr[0] = -1

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

        # Decide whehter to use plume or jet
        # ----------------------------------
        if (r / (z_H - z_0) > 0.134) and (r / (z_H - z_0) > 0.246):
            air_type = 2  # jet
        else:
            air_type = 1  # plume

        if i > 2 and air_type_arr[i - 1] != air_type:
            raise ValueError(f'Air temperature correlation transitioned between Jet and Plume at {fire_time[i]} s '
                             f'with r / (z_H - z_0) = {r / (z_H - z_0):g}. '
                             f'This is currently not supported by this function.')

        # Calculate ceiling jet temperature and velocity
        # ----------------------------------------------
        if air_type == 1:
            theta_jet_rise = eq_14_plume_temperature(
                T_0=ambient_gas_temperature,
                g=ambient_gravity_acceleration,
                c_p_0_kJ_kg_K=ambient_gas_specific_heat,
                rho_0=ambient_gas_density,
                Q_dot_c_kW=Q_dot_c_kW,
                z=detector_to_fire_vertical_distance,
                z_0=z_0
            )
            u_jet = eq_15_plume_velocity(
                T_0=ambient_gas_temperature,
                g=ambient_gravity_acceleration,
                c_p_0_kJ_kg_K=ambient_gas_specific_heat,
                rho_0=ambient_gas_density,
                Q_dot_c_kW=Q_dot_c_kW,
                z=detector_to_fire_vertical_distance,
                z_0=z_0,
            )
        elif air_type == 2:
            theta_jet_rise = eq_26_axisymmetric_ceiling_jet_temperature(
                Q_dot_c_kW=Q_dot_c_kW,
                z_H=detector_to_fire_vertical_distance,
                z_0=z_0,
                r=detector_to_fire_horizontal_distance,
            )
            u_jet = eq_27_axisymmetric_ceiling_jet_velocity(
                Q_dot_c_kW=Q_dot_c_kW,
                z_H=detector_to_fire_vertical_distance,
                z_0=z_0,
                r=detector_to_fire_horizontal_distance,
            )
        else:
            raise ValueError(f'Unknown `air_type` {air_type}')

        theta_jet = theta_jet_rise + ambient_gas_temperature

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
        fire_diameter[i] = D
        virtual_origin[i] = z_0
        air_type_arr[i] = air_type
        jet_velocity[i] = u_jet
        jet_temperature[i] = theta_jet
        detector_temperature[i] = Delta_Te

    # Pack up results
    # ===============
    return fire_diameter, virtual_origin, air_type_arr, jet_velocity, jet_temperature, detector_temperature,


def heat_detector_temperature_pd7974_dict(
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
        *_, **__
) -> dict:
    (
        fire_diameter,
        virtual_origin,
        air_type_arr,
        jet_velocity,
        jet_temperature,
        detector_temperature,
    ) = heat_detector_temperature_pd7974(
        fire_time=fire_time,
        fire_hrr_kW=fire_hrr_kW,
        detector_to_fire_vertical_distance=detector_to_fire_vertical_distance,
        detector_to_fire_horizontal_distance=detector_to_fire_horizontal_distance,
        detector_response_time_index=detector_response_time_index,
        detector_conduction_factor=detector_conduction_factor,
        fire_hrr_density_kWm2=fire_hrr_density_kWm2,
        fire_conv_frac=fire_conv_frac,
        ambient_gravity_acceleration=ambient_gravity_acceleration,
        ambient_gas_temperature=ambient_gas_temperature,
        ambient_gas_specific_heat=ambient_gas_specific_heat,
        ambient_gas_density=ambient_gas_density,
    )

    return dict(
        fire_diameter=fire_diameter,
        virtual_origin=virtual_origin,
        air_type=air_type_arr,
        jet_velocity=jet_velocity,
        jet_temperature=jet_temperature,
        detector_temperature=detector_temperature,
    )
