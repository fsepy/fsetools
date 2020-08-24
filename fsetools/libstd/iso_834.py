import numpy as np


def clause_6_1_1(time: np.ndarray):
    """The average temperature of the furnace specified in ISO 834-1, clause 6.1.1. ALL IN SI UNITS.

    :param time: Time array.
    :return temperature: Calculated average furnace temperature.
    """

    # INPUTS CHECK
    time = np.array(time, dtype=float)
    time[time < 0] = np.nan

    # SI UNITS -> EQUATION UNITS
    time /= 60.0  # [s] - [min]

    # CALCULATE TEMPERATURE BASED ON GIVEN TIME
    temperature = 345.0 * np.log10(time * 8.0 + 1.0) + 20
    temperature[temperature == np.nan] = 20

    # EQUATION UNITS -> SI UNITS
    temperature += 273.15  # [C] -> [K]

    return temperature


if __name__ == "__main__":
    fire_time = np.arange(0, 2 * 60 * 60 + 1, 1)
    fire_temperature = clause_6_1_1(fire_time)

    print(
        fire_temperature[fire_time == 5 * 60],
        fire_temperature[fire_time == 10 * 60],
        fire_temperature[fire_time == 15 * 60],
        fire_temperature[fire_time == 20 * 60],
        fire_temperature[fire_time == 25 * 60],
    )
