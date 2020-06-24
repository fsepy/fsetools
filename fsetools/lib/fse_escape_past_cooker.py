import math

"""
    WIP!!!
    This script is based off of internal fire engineering modeling of escape pasty a hob which is on fire.
    The necessary input parameters in order to calculate this are:
        uncongested horizontal travel speed
        occupant shoulder/ lane width
        time to open final exit door
        total travel distance in the room of fire origin (to final exit door)

        hob fire release rate
        radiative fraction

        number of time steps to consider(accuracy of model)
"""

def simplified_model(
    n=100,                              # number of time steps
    v=1,                                # Travel Speed [metres/second]
    lane_width=0.6,                     # lane width [metres]
    door_opening_time=5,                # time to open final exit door [seconds]
    shortest_separation=2.2,            # shortest separation from hob to a boundary or obstruction [metres] (the boundary is the reason we have to travel _past_ the hob per-se) 
    total_travel_distance=15,           # total travel distrance in room of fire origin [metres]
    heat_release_rate=625,              # heat release rate of fire [kW]
    radiative_fraction=0.4,             # radiative heat fraction [-]
    acceptable_tolerance_limit=1.67,    # acceptable toleratnce limit [(kW/sqm)^(4/3)]
    maximum_allowable_FED=1,            # maximum thermal fractional effective dose allowed
    x_f = 1.6,                          # Horizontal distyance between the firew and the evacuee
    y_f = 1.6,                           # vertical distance between the fire and the door
    return_csv=False,
    csv_path="./result.csv"
):
    # these should be arguments,
    
    total_travel_time = total_travel_distance / v
    delta_t = total_travel_time / n

    cumulative_FED = 0
    cumulative_travel = 0
    t = 0
    log = [["time step #", "time [seconds]", "cumulative travel", "separation", "heat received", "tIrad", "FED", "cumulative FED"]]
    for time_step in range(0,n):
        t += delta_t
        if time_step == n-1:
            #if we're on the last time step we also need to open the door
            delta_t += door_opening_time
        
        cumulative_travel = t * v

        y_separation = total_travel_distance - y_f - cumulative_travel

        separation = math.sqrt(x_f ** 2 + y_separation ** 2)

        heat_received = heat_release_rate * radiative_fraction / (4 * math.pi * separation**2)

        tIrad = acceptable_tolerance_limit / (heat_received ** 1.33)
        
        FED = delta_t / (60 * tIrad)

        cumulative_FED += FED

        # log the results because it's useful for debugging
        log_row = [time_step, t, cumulative_travel, separation, heat_received, tIrad, FED, cumulative_FED]
        log.append(log_row)

    if return_csv:
        import csv
        with open (csv_path, "w+") as csv_file:
            csvWriter = csv.writer(csv_file, delimiter=",")
            csvWriter.writerows(log)
    return cumulative_FED








