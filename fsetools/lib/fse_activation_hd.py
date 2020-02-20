import typing

import numpy as np

from fsetools.libstd.pd_7974_1_2019 import eq_10_virtual_origin
from fsetools.libstd.pd_7974_1_2019 import eq_14_plume_temperature
from fsetools.libstd.pd_7974_1_2019 import eq_15_plume_velocity
from fsetools.libstd.pd_7974_1_2019 import eq_26_axisymmetric_ceiling_jet_temperature
from fsetools.libstd.pd_7974_1_2019 import eq_27_axisymmetric_ceiling_jet_velocity
from fsetools.libstd.pd_7974_1_2019 import eq_55_activation_of_heat_detector_device


def heat_detector_temperature_pd7974(
        gas_time: typing.Union[np.ndarray, list],
        gas_hrr_kW: typing.Union[np.ndarray, list],
        detector_to_fire_vertical_distance: float,
        detector_to_fire_horizontal_distance: float,
        detector_response_time_index: float,
        detector_conduction_factor: float,
        fire_hrr_density_kWm2: float,
        fire_convection_fraction: float,
        ambient_gravity_acceleration: float = 9.81,
        ambient_gas_temperature: float = 293.15,
        ambient_gas_specific_heat: float = 1.2,
        ambient_gas_density: float = 1.0,
        force_plume_temperature_correlation: bool = False,
):
    """This function calculates heat detector device time - temperature revolution based on specified fire heat release
    rate.

    :param gas_time:
    :param gas_hrr_kW:
    :param detector_to_fire_vertical_distance:
    :param detector_to_fire_horizontal_distance:
    :param detector_response_time_index:
    :param detector_conduction_factor:
    :param fire_hrr_density_kWm2:
    :param fire_convection_fraction:
    :param ambient_gas_temperature:
    :param ambient_gas_density:
    :param ambient_gas_specific_heat:
    :param ambient_gravity_acceleration:
    :param force_plume_temperature_correlation:
    :return:
    """

    # Check and convert input types
    if isinstance(gas_time, list):
        gas_time = np.array(gas_time)
    if isinstance(gas_hrr_kW, list):
        gas_hrr_kW = np.array(gas_hrr_kW)

    # Validate parameters
    # ===================
    try:
        assert len(gas_time) == len(gas_hrr_kW)
    except AssertionError:
        raise ValueError('Gas time `gas_time` and temperature array `gas_temperature` length do not match.')

    # Result containers
    # =================

    fire_diameter = [((gas_hrr_kW[0] * fire_convection_fraction / fire_hrr_density_kWm2) / 3.1415926) ** 0.5 * 2]
    jet_temperature = [ambient_gas_temperature]
    jet_velocity = [0.]
    detector_temperature = [ambient_gas_temperature]
    virtual_origin = [0]

    # Main heat detector temperature calculation starts
    # =================================================

    for i in range(1, len(gas_time), 1):

        # Calculate change in time, dt
        # ----------------------------
        dt = gas_time[i] - gas_time[i - 1]

        # Calculate convective heat release rate
        # --------------------------------------
        Q_dot_c_kW = gas_hrr_kW[i] * fire_convection_fraction

        # Calculate fire diameter
        # -----------------------
        D = ((gas_hrr_kW[i] / fire_hrr_density_kWm2) / 3.1415926) ** 0.5 * 2

        # Calculate virtual fire origin
        # -----------------------------
        z_0 = eq_10_virtual_origin(D=D, Q_dot_kW=gas_hrr_kW[i])
        virtual_origin.append(z_0)

        # Calculate ceiling jet temperature
        # ---------------------------------
        if not force_plume_temperature_correlation:
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
        if not force_plume_temperature_correlation:
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
        dTe_dt = eq_55_activation_of_heat_detector_device(
            u=u_jet,
            RTI=detector_response_time_index,
            Delta_T_g=theta_jet - ambient_gas_temperature,
            Delta_T_e=detector_temperature[i - 1] - ambient_gas_temperature,
            C=detector_conduction_factor
        )
        dTe = dTe_dt * dt
        Te = dTe + detector_temperature[i - 1]
        # Te = dTe + ambient_gas_temperature

        # Record results
        # --------------
        fire_diameter.append(D)
        jet_temperature.append(theta_jet)
        jet_velocity.append(u_jet)
        detector_temperature.append(Te)

    # Pack up results
    # ===============

    res = dict(
        detector_temperature=np.array(detector_temperature),
        jet_temperature=np.array(jet_temperature),
        jet_velocity=np.array(jet_velocity),
        fire_diameter=np.array(fire_diameter),
        virtual_origin=np.array(virtual_origin),
    )

    return res


def _test_heat_detector_activation_ceiling_pd7974():
    from fsetools.libstd.pd_7974_1_2019 import eq_22_t_squared_fire_growth

    # Pre-calculated results

    # Code results
    t = np.array([i * 0.5 for i in range(1200)])
    res = heat_detector_temperature_pd7974(
        gas_time=t,
        gas_hrr_kW=[eq_22_t_squared_fire_growth(alpha=0.0117, t=i) / 1000. for i in t],
        detector_to_fire_vertical_distance=3.6,
        detector_to_fire_horizontal_distance=2.83,
        detector_response_time_index=115,
        detector_conduction_factor=0.4,
        fire_hrr_density_kWm2=510,
        fire_convection_fraction=0.7,
    )
    detector_activation_temperature = 68 + 273.15

    # find the activation time
    calculated_activation_time = t[np.argmin(np.abs(res['detector_temperature'] - detector_activation_temperature))]
    given_activation_time = 333  # checked against Chris Mayfield's calculation on 7th Feb 2020 15:20, Bicester
    assert abs(calculated_activation_time - given_activation_time) <= 1.


def _test_heat_detector_activation_ceiling_pd7974_2():
    from fsetools.libstd.pd_7974_1_2019 import eq_22_t_squared_fire_growth

    # Pre-calculated results

    # Code results
    gas_time = np.array([i * 0.5 for i in range(1200)])
    gas_hrr_kWm2 = eq_22_t_squared_fire_growth(0.0117, gas_time) / 1000.
    res = heat_detector_temperature_pd7974(
        gas_time=gas_time,
        gas_hrr_kW=gas_hrr_kWm2,
        detector_to_fire_vertical_distance=3.,
        detector_to_fire_horizontal_distance=2.5,
        detector_response_time_index=115,
        detector_conduction_factor=0.4,
        fire_hrr_density_kWm2=510,
        fire_convection_fraction=0.7,
    )
    detector_activation_temperature = 68 + 273.15

    # find the activation time
    calculated_activation_time = gas_time[
        np.argmin(np.abs(res['detector_temperature'] - detector_activation_temperature))]
    given_activation_time = 287  # checked against Danny Hopkin's calculation on 7th Feb 2020 16:20, Bicester
    assert abs(calculated_activation_time - given_activation_time) <= 1.


if __name__ == '__main__':
    _test_heat_detector_activation_ceiling_pd7974()
    _test_heat_detector_activation_ceiling_pd7974_2()
