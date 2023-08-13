def test():
    import copy

    from matplotlib import pyplot as plt
    from scipy.interpolate import interp1d
    import numpy as np

    # Set geometrical parameters & simulation time frame

    nodes = 100  # set the number of nodes
    dx = 0.1 / nodes  # in m
    temp_arr = (
            np.ones(nodes) * 20
    )  # creates initial temperature nodal array with ambient condition
    endtime = 600  # number of timesteps
    dt = 0.025  # time step increment
    nth = 1000  # Temperature profile will be produced every nth time step
    endtimestep = int(endtime / dt)  # calculate total number of timesteps
    node_array = np.ones(nodes)  # Create depth array for temperature profile

    # Set heat transfer properties based upon initial temperature conditions

    lamda_temp_arr = [0, 1200]  # Temperature array for conductivity [DegC]
    lamda_input_arr = [40, 40]  # Corresponding conductivity input [W/m.K]
    # lamda_temp_arr = [19,500,1200]                              #  Temperature array for conductivity [DegC]
    # lamda_input_arr = [0.12,0.11, 1]                             #  Corresponding conductivity input [W/m.K]
    lamda_interp = interp1d(lamda_temp_arr, lamda_input_arr)  # Interpolation function

    cp_temp_arr = [0, 1200]  # Temperature array for specific heat [DegC]
    cp_input_arr = [450, 450]  # Corresponding specific heat input [J/kg.K]
    # cp_temp_arr = [19, 99, 100, 120, 121, 1200]                 #  Temperature array for specific heat [DegC]
    # cp_input_arr =[950, 950, 2000, 2000, 950, 950]              #  Corresponding specific heat input [J/kg.K]
    cp_interp = interp1d(cp_temp_arr, cp_input_arr)  # Interpolation function

    rho_temp_arr = [0, 1200]  # Temperature array for density [DegC]
    rho_input_arr = [9850, 9850]
    # rho_temp_arr = [19,1200]                                    #  Temperature array for density [DegC]
    # rho_input_arr =[450,400]                                    #  Corresponding density input [kg/m3]
    rho_interp = interp1d(rho_temp_arr, rho_input_arr)  # Interpolation function

    # Boundary conditions

    hchot = 25  # hot side convection coefficient [W/m2.K]
    hccold = 9  # cold side convection coefficient [W/m2.K]
    effemis = 0.8  # net emissivity - applies to all faces [-]
    tamb = 20  # ambient temp on unexposed face [DegC]

    list_temp_arr = list()  # Create storage matrix

    #  Main heat transfer solver

    print("SOLVING")

    for tstep in range(1, endtimestep + 1):

        # Update thermal property array at each time time
        print(temp_arr)

        # lamdaNL = lamda_interp(temp_arr)
        # cpNL = cp_interp(temp_arr)
        # rhoNL = rho_interp(temp_arr)
        from fsetools.ht1d.ht1d_finite_difference import ONEDHT_QINC
        from fsetools.ht1d.ht1d_finite_difference import ONEDHT_ELEM1
        from fsetools.ht1d.ht1d_finite_difference import ONEDHT_ELEMJ
        from fsetools.ht1d.ht1d_finite_difference import ONEDHT_QOUT
        from fsetools.ht1d.ht1d_finite_difference import ONEDHT_ELEMF
        from fsetools.ht1d.ht1d_finite_difference import k_steel_T
        from fsetools.ht1d.ht1d_finite_difference import c_steel_T
        from fsetools.ht1d.ht1d_finite_difference import ISO834_ft

        lamdaNL = np.array([k_steel_T(temp) for temp in temp_arr])
        cpNL = np.array([c_steel_T(temp) for temp in temp_arr])
        rhoNL = np.full_like(temp_arr, 7850)

        time = dt * tstep  # current simulation time
        gas_temp = ISO834_ft(time)  # gas temp in DegC
        gas_temp = 1000

        if tstep / 10 == int(tstep / 10):
            print("Time = ", time, " s ", "Gas temperature = ", gas_temp, " DegC")

        # First element calculations
        Qinc = ONEDHT_QINC(gas_temp, temp_arr[0], effemis, hchot)
        temp_arr[0] = ONEDHT_ELEM1(
            Qinc,
            temp_arr[0],
            temp_arr[1],
            lamdaNL[0],
            lamdaNL[1],
            dx,
            dt,
            cpNL[0],
            rhoNL[0],
        )

        # Intermediate element calculations
        for nodenum in range(1, nodes - 1):
            temp_arr[nodenum] = ONEDHT_ELEMJ(
                temp_arr[nodenum - 1],
                temp_arr[nodenum],
                temp_arr[nodenum + 1],
                lamdaNL[nodenum - 1],
                lamdaNL[nodenum],
                lamdaNL[nodenum + 1],
                dx,
                dt,
                cpNL[nodenum],
                rhoNL[nodenum],
            )

        # Final element calculations
        Qout = ONEDHT_QOUT(temp_arr[nodes - 1], tamb, effemis, hccold)
        temp_arr[nodes - 1] = ONEDHT_ELEMF(
            Qout,
            temp_arr[nodes - 2],
            temp_arr[nodes - 1],
            lamdaNL[nodes - 2],
            lamdaNL[nodes - 1],
            dx,
            dt,
            cpNL[nodes - 1],
            rhoNL[nodes - 1],
        )

        # Store results

        list_temp_arr.append(copy.copy(temp_arr))

    # Generate depth array [mm]

    for x in range(0, nodes):
        node_array[x] = x * dx * 1000

    # Plot temperature profiles at every nth time step

    plt.style.use("seaborn-paper")
    fig, ax = plt.subplots(figsize=(4, 3))
    for i, v in enumerate(list_temp_arr):
        if i / nth == int(i / nth):
            ax.plot(node_array, v)
            ax.grid(True)
            ax.set_xlabel("Depth [mm]")
            ax.set_ylabel("Temperature [$^\circ C$]")

    ax.plot(node_array, list_temp_arr[-1])

    plt.tight_layout()
    plt.show()
