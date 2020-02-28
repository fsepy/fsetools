import typing
from os.path import join, realpath

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from fsetools.etc.transforms2d import rotation_meshgrid, angle_between_two_vectors_2d
from fsetools.lib.fse_thermal_radiation import phi_parallel_any_br187


def update_input_param(input_param_dict: dict):

    for emitter in input_param_dict['emitter_list']:
        emitter.update(
            dict(
                # width of the rectangle
                width=np.sum(
                    (emitter['x'][0] - emitter['x'][1]) ** 2 +
                    (emitter['y'][0] - emitter['y'][1]) ** 2
                ) ** 0.5,
                height=abs(emitter['z'][0] - emitter['z'][1]),
            )
        )

        if emitter['x'][0] == emitter['x'][1]:
            emitter['x'][1] += 1e-9
        if emitter['y'][0] == emitter['y'][1]:
            emitter['y'][1] += 1e-9

    return input_param_dict


def solve_phi(
        emitter: dict,
        xx: np.ndarray,
        yy: np.ndarray,
        zz: np.ndarray
) -> np.ndarray:
    # calculate the angle between a flat line (1, 0) and the emitter plane on z-plane
    v1 = emitter['x'][1] - emitter['x'][0], emitter['y'][1] - emitter['y'][0]
    v2 = (1, 0)
    theta_in_radians = angle_between_two_vectors_2d(
        v1=v1,
        v2=v2
    )

    # since this is a 2d solver, the results can only shown on a single z plane. therefore, calculation domain in zz
    # can only have one value.
    if len(zz) != 1:
        raise NotImplementedError('Multiple zz is not implemented.')

    # solver domain
    xx, yy = rotation_meshgrid(xx, yy, theta_in_radians)

    # calculate the emitter surface level, i.e. everything below this level is behind the emitter.
    emitter_x, emitter_y = rotation_meshgrid(emitter['x'], emitter['y'], theta_in_radians)
    try:
        assert abs(emitter_y[0, 0] - emitter_y[0, 1]) <= 1e-10
    except AssertionError:
        print(emitter_y[0, 0], emitter_y[0, 1], 'do not match.')
        raise AssertionError
    surface_level_y = emitter_y[0, 0]

    emitter_x_centre = np.average(emitter_x)

    # check meshgrid rotation
    # plt.contourf(xx, yy, np.ones_like(xx))
    # plt.show()

    vv = np.zeros_like(xx)
    emitter_height = emitter['height']
    emitter_width = emitter['width']
    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            y = yy[i, j]
            if y > surface_level_y:
                vv[i, j] = phi_parallel_any_br187(
                    W_m=emitter_width,
                    H_m=emitter_height,
                    w_m=0.5 * emitter_width + abs(emitter_x_centre - xx[i, j]),
                    h_m=zz[0],
                    S_m=y - surface_level_y
                )

    # check phi
    # plt.contourf(xx, yy, vv)
    # plt.show()
    # print(theta_in_radians)

    return vv


def _test_solve_phi():
    xx, yy = np.meshgrid(np.linspace(-20, 20, 100), np.linspace(-20, 20, 100))

    zz = solve_phi(
        emitter=update_input_param(
            dict(
                x=[-10, -10],
                y=[0, 10],
                z=[0, 3.5],
                heat_flux=84,
            )
        ),
        xx=xx,
        yy=yy,
        zz=[1]
    )

    plt.contourf(xx, yy, zz)
    plt.show()


def plot_heat_flux_on_ax(
        ax,
        xx: np.ndarray,
        yy: np.ndarray,
        zz: np.ndarray,
        levels: tuple = (0, 12.6, 20, 40, 60, 80, 200),
):
    levels_contour = levels
    colors_contour = ['r' if i == 12.6 else 'k' for i in levels_contour]
    levels_contourf = levels_contour
    colors_contourf = [cm.get_cmap('YlOrRd')(i / (len(levels_contour) - 1)) for i, _ in enumerate(levels_contour)]
    colors_contourf = [(r_, g_, b_, 0.65) for r_, g_, b_, a_ in colors_contourf]
    colors_contourf[0] = (195 / 255, 255 / 255, 143 / 255, 0.65)

    # create axes
    cs = ax.contour(xx, yy, zz, levels=levels_contour, colors=colors_contour)
    cs_f = ax.contourf(xx, yy, zz, levels=levels_contourf, colors=colors_contourf)

    ax.clabel(cs, inline=1, fontsize=12, fmt='%1.1f kW')

    ax.grid(b=True, which='major', axis='both')
    ax.set_aspect(aspect=1)

    # axis ticks
    ax.set_xticks(np.arange(xx.min(), xx.max() + 0.2, 0.2))
    ax.set_yticks(np.arange(yy.min(), xx.max() + 0.2, 0.2))

    # axis limits
    ax.set_xlim((xx.min(), xx.max()))
    ax.set_ylim((yy.min(), xx.max()))

    # axis visibility
    # ax.get_xaxis().set_visible(False)
    # ax.get_yaxis().set_visible(False)
    # ax.axis('off')

    return ax, (cs, cs_f)


def main_plot(input_param_dict: dict, dir_cwd: str = None, save_figure: bool = True):
    for n_count, case_name in enumerate(sorted(input_param_dict.keys())):
        # ratio of physical dimension to base figure size
        if 'figsize_base' in input_param_dict[case_name]:
            print('d')
            figsize_base = input_param_dict[case_name]['figsize_base']
        else:
            figsize_base = 30  # this is going to be the longest dimension of all figures (not axes)

        # create a figure
        fig = plt.figure(
            figsize=(figsize_base, figsize_base),
            frameon=False,
        )

        ax = fig.add_subplot()

        ax.set_aspect('equal')

        if 'figure_levels' in input_param_dict[case_name]:
            figure_levels = input_param_dict[case_name]['figure_levels']
        else:
            figure_levels = (0, 12.6, 20, 40, 60, 80, 200)

        ax, (_, cs_f) = plot_heat_flux_on_ax(
            ax=ax,
            xx=input_param_dict[case_name]['xx'],
            yy=input_param_dict[case_name]['yy'],
            zz=input_param_dict[case_name]['heat_flux'],
            levels=figure_levels
        )

        for i in range(len(input_param_dict[case_name]['emitter_list'])):
            ax.plot(input_param_dict[case_name]['emitter_list'][i]['x'],
                    input_param_dict[case_name]['emitter_list'][i]['y'], lw=5, c='r', ls='--')

        try:
            for i in range(len(input_param_dict[case_name]['receiver_list'])):
                ax.plot(input_param_dict[case_name]['receiver_list'][i]['x'],
                        input_param_dict[case_name]['receiver_list'][i]['y'], lw=5, c='k', ls='--')
        except KeyError:
            pass

        ax.set_xlim(*input_param_dict[case_name]['solver_domain']['x'])
        ax.set_ylim(*input_param_dict[case_name]['solver_domain']['y'])

        # colour bar
        cbar = fig.colorbar(cs_f)
        cbar.ax.set_yticklabels([f'{i:.1f} $kW\cdot m^{{2}}$' for i in figure_levels])

        input_param_dict[case_name]['ax'] = ax

        if save_figure:
            if dir_cwd:
                dir_cwd = realpath(dir_cwd)
            if dir_cwd:
                fp_fig = join(dir_cwd, f'{case_name}.png')
                fp_fig_extend = join(dir_cwd, f'{case_name}_extend.png')
            else:
                fp_fig = f'{case_name}.png'
                fp_fig_extend = f'{case_name}_extend.png'
            fig.savefig(fp_fig, transparent=True)
            extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            fig.savefig(fp_fig_extend, transparent=True, bbox_inches=extent)

    return input_param_dict


def main(params_dict: dict):
    """

    :param params_dict:
        A dict object with the following structure.
            dict(
                emitter_list=list(
                    x=(x1, x2),
                    y=(y1, y2),
                    z=(z1, z2),
                    heat_flux=float,
                ),
                receiver_list=list(  # optional
                    x=(x1, x2),
                    y=(y1, y2),
                ),
                solver_domain=dict(
                    x=(x1, x2),
                    y=(y1, y2),
                    z=(z1,)
                ),
                delta=0.5,  # optional
            )
        Where:
            emitter_list
                x1, y1      the first point of the line segment on z-plane.
                x2, y2      the second point of the line segment on z-plane.
                z1, z2      the bottom and top of the emitter, i.e. abs(z1-z2) is the emitter height.
                heat_flux   the heat flux (thermal) radiating from the emitter.
            receiver_list
                x1, y1      the first point of the line segment on z-plane.
                x2, y2      the second point of the line segment on z-plane.
            solver_domain
                the area/ space that the imposed heat flux going to be solved.
            solver_delta
                resolution of the `solver_domain`

    :return params_dict:
        the same as the input `params_dict` with calculated heat flux and configuration factors.
    """
    # ========================
    # prepare input parameters
    # ========================

    params_dict = update_input_param(params_dict)

    # ==============================
    # calculate configuration factor
    # ==============================

    x1, x2 = params_dict['solver_domain']['x']
    y1, y2 = params_dict['solver_domain']['y']
    delta = params_dict['solver_delta']
    xx, yy = np.arange(x1, x2 + 0.5 * delta, delta), np.arange(y1, y2 + 0.5 * delta, delta)
    xx, yy = np.meshgrid(xx, yy)
    for i, emitter in enumerate(params_dict['emitter_list']):
        phi = solve_phi(
            emitter=emitter,
            xx=xx,
            yy=yy,
            zz=params_dict['solver_domain']['z'],
        )

        emitter['phi'] = phi

    # =============================
    # calculate resultant heat flux
    # =============================

    heat_flux = np.zeros_like(params_dict['emitter_list'][0]['phi'], dtype=np.float64)
    for i, emitter in enumerate(params_dict['emitter_list']):
        heat_flux += (emitter['phi'] * emitter['heat_flux'])
    heat_flux[heat_flux == 0] = -1
    params_dict['heat_flux'] = heat_flux

    # make plots
    # main_plot(params_dict)

    return params_dict


def _test_main():

    # ======
    # test 0
    # ======
    # test interface

    input_param_dict = dict(
        emitter_list=[
            dict(
                x=[-5, 5],
                y=[1, 1],
                z=[0, 10],
                heat_flux=1,
            )
        ],
        receiver_list=[
            dict(
                x=[-5, 5],
                y=[10, 10],
            )
        ],
        solver_domain=dict(
            x=(-20, 20),
            y=(-20, 20),
            z=(5,)
        ),
        solver_delta=.2
    )

    out = main(input_param_dict)

    # check phi dimension
    x1, x2 = out['solver_domain']['x']
    y1, y2 = out['solver_domain']['y']
    delta = out['solver_delta']
    xx, yy = np.meshgrid(np.arange(x1, x2 + 0.5 * delta, delta), np.arange(y1, y2 + 0.5 * delta, delta))
    assert out['heat_flux'].shape == xx.shape == yy.shape

    # check output elements
    for emitter in out['emitter_list']:
        assert 'phi' in emitter
        assert 'height' in emitter
        assert 'width' in emitter

    # ======
    # test 1
    # ======
    # test numerical correctness
    # a horizontal emitter with dimension of 10 x 10 (w x h) located on y-plane (y=1). A receiver is located 5 m away
    # from the emitter and on the centre axis of the emitter.

    # INPUTS
    # W, width = 10
    # H, height = 10
    # w, horizontal offset = 0
    # h, vertical offset = 0
    # S, separation distance = 5
    # phi = 0.5541 (pre calculated)

    input_param_dict = dict(
        emitter_list=[
            dict(
                x=[-5, 5],
                y=[1, 1],
                z=[0, 10],
                heat_flux=1,
            )
        ],
        receiver_list=[
            dict(
                x=[-5, 5],
                y=[10, 10],
            )
        ],
        solver_domain=dict(
            x=(-20, 20),
            y=(-20, 20),
            z=(5,)
        ),
        solver_delta=.2
    )

    out = main(input_param_dict)
    
    x1, x2 = out['solver_domain']['x']
    y1, y2 = out['solver_domain']['y']
    delta = out['solver_delta']
    xx, yy = np.meshgrid(np.arange(x1, x2 + 0.5 * delta, delta), np.arange(y1, y2 + 0.5 * delta, delta))
    h = out['heat_flux'][(np.isclose(xx, 0)) & np.isclose(yy, 6)]

    # check phi solution
    print(h[0], 0.5541)
    assert np.isclose(h[0], 0.5541, atol=1e-4)

    # ======
    # test 2
    # ======
    # test numerical correctness
    # a horizontal emitter with dimension of 10 x 10 (w x h) located on y-plane (y=1). A receiver is located 5 m away
    # from the emitter and on the centre axis of the emitter.

    # INPUTS
    # W, width = 10
    # H, height = 10
    # w, horizontal offset = 5
    # h, vertical offset = 5
    # S, separation distance = 5
    # phi = 0.2078 (pre calculated)

    input_param_dict = dict(
        emitter_list=[
            dict(
                x=[-5, 5],
                y=[1, 1],
                z=[0, 10],
                heat_flux=1,
            )
        ],
        receiver_list=[
            dict(
                x=[-5, 5],
                y=[10, 10],
            )
        ],
        solver_domain=dict(
            x=(-20, 20),
            y=(-20, 20),
            z=(0,)
        ),
        solver_delta=.2
    )

    out = main(input_param_dict)

    x1, x2 = out['solver_domain']['x']
    y1, y2 = out['solver_domain']['y']
    delta = out['solver_delta']
    xx, yy = np.meshgrid(np.arange(x1, x2 + 0.5 * delta, delta), np.arange(y1, y2 + 0.5 * delta, delta))
    h = out['heat_flux'][(np.isclose(xx, -5)) & np.isclose(yy, 6)]

    # check phi solution
    print(h[0], 0.2078)
    assert np.isclose(h[0], 0.2078, atol=1e-4)


if __name__ == '__main__':
    _test_main()
    # _test_solve_phi()
