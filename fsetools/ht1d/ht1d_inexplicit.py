from typing import Tuple
from typing import Union, Callable

import numpy as np


def gauss(
        A: np.ndarray,
        b: np.ndarray,
        x: np.ndarray,
        tol: float,
        T_env: float,
        T_amb: float,
        diffus: float,
        dt: float,
        conductivity: float,
        dx: float,
        max_iter: int = 100,
) -> Tuple[np.ndarray, int, float, float]:
    max_x_err = 1
    count_iter: int = 0
    q_net_exp: float = np.nan
    q_net_unexp: float = np.nan

    while max_x_err > tol:
        L = np.tril(A)
        U = A - L

        #  Update boundary condition on exposed face
        q_net_exp = net_HF_in(T_env, x[0, 0], 0.7, 25)
        Exposed_C_coeff = (2 * diffus * q_net_exp * dt) / (conductivity * dx)
        b[0, 0] = x[0, 0] + Exposed_C_coeff

        #  Update boundary condition on unexposed face
        q_net_unexp = net_HF_in(x[-1, 0], T_amb, 0.7, 9)
        Unexposed_C_coeff = (2 * diffus * q_net_unexp * dt) / (conductivity * dx)
        b[-1, 0] = x[-1, 0] - Unexposed_C_coeff

        #
        x_old = x
        count_iter = count_iter + 1
        x = np.dot(np.linalg.inv(L), b - np.dot(U, x))
        x_err = abs((x - x_old) / x_old)
        max_x_err = np.amax(x_err)

        if count_iter > max_iter:
            raise StopIteration(count_iter)

    return x, count_iter, q_net_exp, q_net_unexp


def create_matrix(nodes):
    coeff_mat = np.zeros((nodes, nodes))
    return coeff_mat


def fourier_num(
        diffus: float,
        dt: float,
        dx: float,
) -> float:
    Fo = (diffus * dt) / (dx * dx)

    return Fo


def diffusivity(
        k: float,
        rho: float,
        cp: float,
) -> float:
    diffus = k / (rho * cp)
    return diffus


def net_HF_in(
        Tenv: float,
        Ts: float,
        emiss: float,
        conv: float,
) -> float:
    q_net_rad = emiss * 5.67e-8 * (((Tenv + 273) ** 4) - ((Ts + 273) ** 4))
    q_net_conv = conv * (Tenv - Ts)
    q_net_in = float(q_net_rad + q_net_conv)
    return q_net_in


def main(
        n_nodes: int,
        dx: float,
        t_end: float,
        dt: float,
        T_init: float,
        T_boundary_0: Union[float, Callable],
        k: float,
        rho: float,
        c: float,
        tol: float,
):
    # Calculate Fourier number
    diffus = diffusivity(k, rho, c)
    Fo = fourier_num(diffus, dt, dx)

    # Initialise storage array for temperatuers
    # T_solved = list()
    T_solved = np.full(shape=(len(np.arange(0, t_end + dt / 2, dt)), n_nodes), fill_value=np.nan)

    # Initialise A matrix
    A = create_matrix(n_nodes)

    # Initialise C matrix
    C = np.zeros((n_nodes, 1))
    C[0] = T_init
    for node_num_x in range(1, n_nodes - 1):
        C[node_num_x] = T_init * 2
    C[n_nodes - 1] = T_init

    # Define coefficients
    A[0, 0] = (1 + (2 * Fo))
    A[0, 1] = -2 * Fo

    for node_num_x in range(1, n_nodes):
        A[node_num_x, node_num_x] = (1 + (2 * Fo)) * 2
        A[node_num_x, node_num_x - 1] = -1 * Fo * 2
        if node_num_x < n_nodes - 1:
            A[node_num_x, node_num_x + 1] = -1 * Fo * 2
    A[n_nodes - 1, n_nodes - 1] = (1 + (2 * Fo))

    i = 0
    for t in np.arange(0, t_end + dt / 2, dt):

        # Get boundary condition
        if isinstance(T_boundary_0, (int, float)):
            T_env = T_boundary_0
        elif isinstance(T_boundary_0, Callable):
            T_env = T_boundary_0(t)
        else:
            raise TypeError(f'Supported data type Callable or float for `T_boundary_0`, got {type(T_boundary_0)}')

        # Update trial matrix
        trial_matrix = C

        # Solve coefficients
        gauss_sol, gauss_count, q_net_in, q_net_out = gauss(A, C, trial_matrix, tol, T_env, T_init, diffus, dt, k, dx)

        # Update C matrix for next loop
        C[0] = gauss_sol[0]  # + Exposed_C_coeff
        for node_num_x in range(1, n_nodes - 1):
            C[node_num_x] = gauss_sol[node_num_x] * 2
        C[n_nodes - 1] = gauss_sol[n_nodes - 1]  # - Unexposed_C_coeff

        # Store results
        # T_solved.append(copy.copy(gauss_sol))
        T_solved[i, :] = gauss_sol[:, 0]
        i += 1

    return T_solved
