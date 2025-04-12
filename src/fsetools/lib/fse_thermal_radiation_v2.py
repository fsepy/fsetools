import numpy as np

__all__ = 'phi_solver', 'phi_angled_any_en_1_converted',

from ..etc.solver import linear_solver


def phi_angled_corner_en_1(w: float, h: float, theta: float, s: float):
    a = h / s
    b = w / s

    cc = (1 - b * np.cos(theta)) / ((1 + b ** 2 - 2 * b * np.cos(theta)) ** 0.5)
    dd = np.arctan(a / (1 + b ** 2 - 2 * b * np.cos(theta)) ** 0.5)
    ee = (a * np.cos(theta)) / ((a ** 2 + np.sin(theta) ** 2) ** 0.5)
    ff = np.arctan((b - np.cos(theta)) / ((a ** 2 + np.sin(theta) ** 2) ** 0.5))
    gg = np.arctan((np.cos(theta)) / ((a ** 2 + np.sin(theta) ** 2) ** 0.5))

    Phi = 0.5 / np.pi * (np.arctan(a) - cc * dd + ee * (ff + gg))

    return Phi


def phi_angled_any_en_1(W, H, w, h, theta, S):
    """
    :param W: width of emitter
    :param H: height of emitter
    :param w: separation between the intersection point to the furthest emitter edge
    :param h: receiver vertical location to the conner
    :param theta: angle between the receiver plane and emitter plane
    :param S: separation between the corner to the receiver
    :return Phi: view factor
    """
    # print(f'W={W:<10.2f}, H={H:<10.2f}, w={w:<10.2f}, h={h:<10.2f}, theta={theta:<10.2f}, S={S:<10.2f}')

    if w < 0:
        # no part of the emitter visible to receiver
        return 0

    if h < 0:
        # take it symmetrical
        h = H - h
    if h == H:
        # at the corner, effectively h = 0, e.g., symmetrical
        h = 0

    if h == 0:
        # at corner
        # just one emitter
        return phi_angled_variable_W(W=W, H=H, w=w, h=h, S=S, theta=theta)

    elif 0 < h < H:
        # within the edge/rect
        # the emitter split into two emitters, both are positive
        Phi_1 = phi_angled_variable_W(W=W, H=H - h, w=w, h=0, S=S, theta=theta)
        Phi_2 = phi_angled_variable_W(W=W, H=h, w=w, h=0, S=S, theta=theta)
        return Phi_1 + Phi_2

    elif H < h:
        # outside the edge/rect
        # the emitter will be split into two, one large positive emitter and one smaller negative emitter
        Phi_1 = phi_angled_variable_W(W=W, H=h, w=w, h=0, S=S, theta=theta)
        Phi_2 = -phi_angled_variable_W(W=W, H=h - H, w=w, h=0, S=S, theta=theta)
        return Phi_1 + Phi_2

    else:
        raise ValueError()


def phi_angled_any_en_1_converted(W, H, w, h, theta, S):
    if isinstance(theta, np.ndarray):
        theta[(theta < 1e-5) | (theta > 0)] = 1e-5
        theta[(theta > -1e-5) | (theta < 0)] = 1e-5
    else:
        if 1e-5 > theta >= 0:
            theta = 1e-5
        elif -1e-5 < theta <= 0:
            theta = -1e-5

    return phi_angled_any_en_1(**map_var_to_en_1(W=W, H=H, w=w, h=h, theta=theta, S=S))


def phi_angled_variable_W(W, H, w, h, theta, S) -> float:
    # this function only deals with H=h or h=0
    assert H == h or h == 0

    if W > w:
        # part of the emitter will be invisible to the receiver, ignore this part
        W = w

    if W == w:
        # receiver at the emitter corner
        return phi_angled_corner_en_1(w=W, h=H, s=S, theta=theta)

    elif W < w:
        # receiver away from the emitter edge
        # the receiver split into two, a larger positive emitter and a smaller negative emitter
        Phi_1 = phi_angled_corner_en_1(w=w, h=H, s=S, theta=theta)
        Phi_2 = -phi_angled_corner_en_1(w=w - W, h=H, s=S, theta=theta)
        return Phi_1 + Phi_2
    else:
        raise ValueError()


def phi_solver(W: float, H: float, w: float, h: float, theta: float, Q: float, Q_a: float, S=None, UA=None):
    """A wrapper to `phi_parallel_any_br187` with error handling and customised IO"""

    # default values
    phi_solved, q_solved, S_solved, UA_solved = [None] * 4
    # phi_solved, solved configuration factor
    # q_solved, solved receiver heat flux
    # S_solved, solved separation distance, surface-to-surface
    # UA_solved, solved permissible unprotected area
    # msg, a message to indicate calculation status if successful.

    if S:  # to calculate maximum unprotected area
        try:
            phi_solved = phi_angled_any_en_1_converted(W=W, H=H, w=w, h=h, theta=theta, S=S)
        except Exception as e:
            raise ValueError(f'Failed to execute `phi_parallel_any_br187`. {type(e).__name__}.')

        if Q:
            # if Q is provided, proceed to calculate q and UA
            q_solved = Q * phi_solved
            if q_solved == 0:
                UA_solved = 1
            else:
                UA_solved = max([min([Q_a / q_solved, 1]), 0])

            q_solved *= UA_solved
    # to calculate minimum separation distance to boundary
    elif UA:
        phi_target = Q_a / (Q * UA)
        if phi_target > 1:
            S_solved = 0
            phi_solved = np.nan
            q_solved = Q * UA
        else:
            try:
                S_solved = linear_solver(
                    func=phi_angled_any_en_1_converted,
                    func_kwargs=dict(W=W, H=H, w=w, h=h, theta=theta, S=S),
                    x_name='S',
                    y_target=phi_target - 0.0001,
                    x_upper=10000,
                    x_lower=0.001,
                    y_tol=0.0001,
                    iter_max=1000,
                    func_multiplier=-1
                )
            except ValueError as e:
                raise ValueError(f'Unable to solve S. {type(e).__name__}.')
            phi_solved = phi_angled_any_en_1_converted(W=W, H=H, w=w, h=h, theta=theta, S=S_solved)
            q_solved = Q * phi_solved * UA
        if S_solved is None:
            raise ValueError('Unable to solve S. Maximum iteration reached.')

    return phi_solved, q_solved, S_solved, UA_solved


def map_var_to_en_1(W, H, w, h, theta, S):
    """Map tool variable to bs en 1991-1-2 correlation

    :param W:
    :param H:
    :param w:
    :param h:
    :param theta:
    :param S:
    :return:
    """
    # print(f'W={W}, H={H}, w={w}, h={h}, theta={theta}, S={S}')
    return dict(
        W=W,
        H=H,
        w=S / np.tan(theta) + W - w,
        h=h,
        theta=theta,
        S=S / np.sin(theta),
    )
