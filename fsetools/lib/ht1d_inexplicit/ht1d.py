import copy

import numpy as np
from matplotlib import pyplot as plt


def gauss(A, b, x, tolerance):
    L = np.tril(A)
    U = A - L
    max_x_err = 1
    count = 0

    while max_x_err > tolerance:
        x_old = x
        count = count + 1
        x = np.dot(np.linalg.inv(L), b - np.dot(U, x))
        x_err = abs((x - x_old) / x_old)
        max_x_err = np.amax(x_err)
    return x, count


def create_matrix(nodes):
    coeff_mat = np.zeros((nodes, nodes))
    return coeff_mat


if __name__ == '__main__':

    # Inputs
    Fo = 0.5
    nodes = 9
    T_amb = 20
    tolerance = 1e-5
    time_steps = 5
    input_temp = 56.1

    # Initialise storage array for temperatuers
    list_temp_arr = []

    depth_arr = np.zeros(nodes)
    for node_num_x in range(1, nodes):
        depth_arr[node_num_x] = node_num_x

    # Initialise A matrix
    A = create_matrix(nodes)

    # Initialise trial matrix
    trial_matrix = np.zeros((nodes, 1))

    # Initialise C matrix
    C = np.zeros((nodes, 1))
    C[0] = T_amb + input_temp
    for node_num_x in range(1, nodes - 1):
        C[node_num_x] = T_amb * 2
    C[nodes - 1] = (T_amb * 2) + T_amb

    # Define coefficients
    A[0, 0] = (1 + (2 * Fo))
    A[0, 1] = -2 * Fo

    for node_num_x in range(1, nodes):
        A[node_num_x, node_num_x] = (1 + (2 * Fo)) * 2
        A[node_num_x, node_num_x - 1] = -1 * Fo * 2
        if node_num_x < nodes - 1:
            A[node_num_x, node_num_x + 1] = -1 * Fo * 2

    for t in range(0, time_steps):

        gauss_sol, gauss_count = gauss(A, C, trial_matrix, tolerance)

        print('Gauss_Siedel_solution =', gauss_sol, ',  Iterations =', gauss_count)
        C[0] = gauss_sol[0] + input_temp
        for node_num_x in range(1, nodes - 1):
            C[node_num_x] = gauss_sol[node_num_x] * 2
        C[nodes - 1] = (gauss_sol[nodes - 1] * 2) + T_amb

        # Store results
        list_temp_arr.append(copy.copy(gauss_sol))

        # Plot
        plt.plot(depth_arr, gauss_sol, label=str(t) + ' [step]')

    plt.xlabel('Node_number [-]')
    plt.ylabel('Temperature [$^o$ C]')
    plt.show()
