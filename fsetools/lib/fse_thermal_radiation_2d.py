import typing
from os.path import join, realpath

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from fsetools.etc.transforms2d import rotation_meshgrid, angle_between_two_vectors_2d
from fsetools.lib.fse_thermal_radiation import phi_parallel_any_br187


def update_input_param(input_set: dict):

    x1, x2 = input_set['domain']['x']
    y1, y2 = input_set['domain']['y']
    delta = input_set['delta']

    input_set['xx'], input_set['yy'] = np.meshgrid(
        np.arange(x1, x2 + delta, delta),
        np.arange(y1, y2 + delta, delta),
    )

    input_set['zz'] = input_set['domain']['z']

    return input_set


def update_emitter(dict_emitter: dict):
  
    emitter = dict_emitter

    emitter.update(
        dict(
            # width of the rectangle
            width=np.sum
                  (np.square(emitter['x'][0] - emitter['x'][1]) + np.square(emitter['y'][0] - emitter['y'][1])) ** 0.5,
            height=abs(emitter['z'][0] - emitter['z'][1]),
            theta=np.arctan2(emitter['y'][1] - emitter['y'][0], emitter['x'][1] - emitter['x'][0])
        )
    )

    if emitter['x'][0] == emitter['x'][1]:
        emitter['x'][1] += 1e-9
    if emitter['y'][0] == emitter['y'][1]:
        emitter['y'][1] += 1e-9

    return emitter


def solve_intersection_line_and_perpendicular_point(
        xy1: tuple,
        xy2: tuple,
        xy3: tuple
) -> tuple:
    """
    Solves for coordinates of p4 given p1, p2 and p3.
    p1 and p2 are two points forms a line l1.
    p3 and p4 are two points forms a line l2.
    l1 and l2 is perpendicular to each other.
    p4 is the intersection between l1 and l2.

    :param xy1:
    :param xy2:
    :param xy3:
    :return:
    """

    x1, y1 = xy1
    x2, y2 = xy2
    x3, y3 = xy3

    # solve the plane equation
    # a x + b = y
    # a = np.tan(emitter['theta'])
    # b = a * emitter['x'][1] + emitter['y'][1]
    m1 = np.array([[x1, 1], [x2, 1]])
    m2 = np.array([y1, y2])
    a1, b1 = np.linalg.solve(m1, m2)

    # solve the tangent line equation
    # a2 x + b2 = y, a2 is known
    a2 = np.tan(np.arctan(a1) + np.pi / 2)
    b2 = y3 - a2 * x3

    # solve the intersection
    m1 = np.array([[a1, -1], [a2, -1]])
    m2 = np.array([-b1, -b2])
    x4, y4 = np.linalg.solve(m1, m2)

    return x4, y4


def _test_solve_intersection_line_and_perpendicular_point():
    x4, y4 = solve_intersection_line_and_perpendicular_point(
        xy1=(0, 0),
        xy2=(10, 10),
        xy3=(10, 0)
    )
    print(x4, y4)
    x4, y4 = solve_intersection_line_and_perpendicular_point(
        (0, 0),
        (10, 5),
        (10, 0)
    )


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
        emitter=update_emitter(
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

    # colour bar
    # fig.colorbar(cs_f)

    # axis labels
    # ax.set_xlabel('Building Facade')
    # ax.set_ylabel('Separation to Surface')

    # axis ticks
    # ax.set_xticks(np.arange(xx.min(), xx.max() + d_ticks, d_ticks))
    # ax.set_yticks(np.arange(yy.min(), xx.max() + d_ticks, d_ticks))

    # axis limits
    # ax.set_xlim((xx.min(), xx.max()))
    # ax.set_ylim((yy.min(), xx.max()))

    # axis visibility
    # ax.get_xaxis().set_visible(False)
    # ax.get_yaxis().set_visible(False)
    ax.axis('off')

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

        ax.set_xlim(*input_param_dict[case_name]['domain']['x'])
        ax.set_ylim(*input_param_dict[case_name]['domain']['y'])

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


def main(input_param_dict: typing.Dict[str, dict], dir_cwd: str = None):
    # update parameters for each input set
    for case_name in input_param_dict.keys():
        input_param_dict[case_name] = update_input_param(input_param_dict[case_name])

    # update emitter parameters for each emitter in each input set
    for case_name in input_param_dict.keys():
        for i in range(len(input_param_dict[case_name]['emitter_list'])):
            input_param_dict[case_name]['emitter_list'][i] = update_emitter(
                input_param_dict[case_name]['emitter_list'][i])

    # calculation
    for case_name in input_param_dict.keys():
        heat_flux = np.zeros_like(input_param_dict[case_name]['xx'], dtype=np.float64)
        # calculate phi
        for i_emitter, emitter in enumerate(input_param_dict[case_name]['emitter_list']):
            phi = solve_phi(
                emitter=emitter,
                xx=input_param_dict[case_name]['xx'],
                yy=input_param_dict[case_name]['yy'],
                zz=input_param_dict[case_name]['zz'],
            )
            input_param_dict[case_name]['emitter_list'][i_emitter]['phi'] = phi
            heat_flux += phi * input_param_dict[case_name]['emitter_list'][i_emitter]['heat_flux']

        heat_flux[heat_flux == 0] = -1
        input_param_dict[case_name]['heat_flux'] = heat_flux

    # make plots
    main_plot(input_param_dict, dir_cwd)


def _test_main():
    input_param_dict = dict(
        case_1=dict(
            emitter_list=[
                dict(
                    x=[10, 0],
                    y=[10, 0],
                    z=[0, 10],
                    heat_flux=84,
                ),
                dict(
                    x=[0, -10],
                    y=[0, 0],
                    z=[0, 10],
                    heat_flux=84,
                ),
                dict(
                    x=[-10, -10],
                    y=[0, 10],
                    z=[0, 10],
                    heat_flux=84,
                ),
                dict(
                    x=[-10, 10],
                    y=[10, 10],
                    z=[0, 10],
                    heat_flux=84,
                ),
                dict(
                    x=[-10, 5],
                    y=[10, 10],
                    z=[0, 10],
                    heat_flux=200,
                )
            ],
            domain=dict(
                x=(-20, 20),
                y=(-20, 20),
                z=(2.5,)
            ),
            delta=.2
        )
    )

    main(input_param_dict)


if __name__ == '__main__':
    _test_main()
    # _test_solve_phi()
