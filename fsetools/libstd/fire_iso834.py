import numpy as np


def clause_6_1_1_fire_curve(
        time: np.ndarray,
        temperature_initial: float = 293.15
) -> np.ndarray:
    """Section 6.1.1, ISO 834-1:1999(E)

    :param time: [s] time array.
    :param temperature_initial: [K] ambient temperature, 293.15 K by default.
    :return temperature: [K] average furnace temperature.
    """

    # INPUTS CHECK
    time = np.array(time, dtype=float)
    time[time < 0] = np.nan

    # SI UNITS -> EQUATION UNITS
    temperature_initial -= 273.15  # [K] -> [C]
    time /= 60.0  # [s] - [min]

    # CALCULATE TEMPERATURE BASED ON GIVEN TIME
    temperature = 345.0 * np.log10(time * 8.0 + 1.0) + temperature_initial
    temperature[temperature == np.nan] = temperature_initial

    # EQUATION UNITS -> SI UNITS
    time *= 60.0  # [min] -> [s]
    temperature += 273.15  # [C] -> [K]

    return temperature


def _test_clause_6_1_1_fire_curve():
    # function results
    temperature = clause_6_1_1_fire_curve(
        np.arange(0, 3601, 3600)
    )

    assert isinstance(temperature, np.ndarray)  # check type
    assert np.alltrue(np.isclose(temperature, [293.15, 1218.490051]))  # check results


if __name__ == "__main__":
    _test_clause_6_1_1_fire_curve()
