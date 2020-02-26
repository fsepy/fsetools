import numpy as np
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib import cm
from pprint import pprint
from tqdm import tqdm
import typing
from fsetools.lib.fse_thermal_radiation import phi_parallel_any_br187
import os
from os.path import join, realpath, basename, dirname


def update_input_param(input_set: dict):

    x1, x2 = input_set['domain']['x']
    y1, y2 = input_set['domain']['y']
    delta = input_set['delta']

    input_set['xx'], input_set['yy'] = np.meshgrid(
        np.arange(x1, x2 + delta, delta),
        np.arange(y1, y2 + delta, delta),
    )

    return input_set


def update_emitter(dict_emitter: dict):

    emitter = dict_emitter

    emitter.update(
        dict(
            # width of the rectangle
            width = np.sum
                (np.square(emitter['x'][0] - emitter['x'][1]) + np.square(emitter['y'][0] - emitter['y'][1])) ** 0.5,
            height = abs(emitter['z'][0 ] - emitter['z'][1]),
            theta = np.arctan2(emitter['y'][1] - emitter['y'][0], emitter['x'][1] - emitter['x'][0])
        )
    )

    return emitter


def solve_intersection_line_and_perpendicular_point(
        xy1: tuple,
        xy2: tuple,
        xy3: tuple
) -> tuple:
    """Solves for coordinates of p4. Where p4 is the intersection between two lines p1->p2 and p3->p4, and p4 is on the
    same line as p1->p2.

    :param xy1:
    :param xy2:
    :param xy3:
    :return:
    """

    x1, y1 = xy1
    x2, y2 = xy2
    x3, y3 = xy3

    # solve for the line equation p1->p2
    # a x + b = y
    m1 = np.array([[x1, 1], [x2, 1]])
    m2 = np.array([y1, y2])
    a1, b1 = np.linalg.solve(m1, m2)

    # solve for the line equation p3->p4
    # a2 x + b2 = y, a2 is known
    a2 = np.tan(np.arctan(a1 ) +np.pi /2)
    b2 = y3 - a2 * x3

    # solve p4
    m1 = np.array([[a1 ,-1], [a2 ,-1]])
    m2 = np.array([-b1 ,-b2])
    x4, x4 = np.linalg.solve(m1, m2)

    return x4, x4


def solve_phi(
        emitter: dict,
        xx: np.ndarray,
        yy: np.ndarray,
        zz: np.ndarray
) -> np.ndarray:

    # point 1 and point 2 defines the line segment (i.e. emitter).
    x1, y1 = emitter['x'][0], emitter['y'][0]
    x2, y2 = emitter['x'][1], emitter['y'][1]

    phi_arr = np.zeros_like(xx)
    n_iter_total = xx.size*len(zz)
    n_iter_count = 0
    with tqdm(total=n_iter_total) as pbar:
        for i in range(np.shape(xx)[0]):
            for j in range(np.shape(xx)[1]):

                # point 3, the point outside the line
                x3, y3 = xx[i, j], yy[i, j]

                # point 4, so that p4 -> p3 is perpendicular to p1 -> p2 and p4 is the intersection.
                x4, y4 = solve_intersection_line_and_perpendicular_point(
                    xy1=(x1, y1), xy2=(x2, y2), xy3=(x3, y3)
                )

                # point 5, the median of p1 -> p2
                x5, y5 = (x2 + x1) / 2, (y2 + y1) / 2

                # separation between receiver (p3) and emitter (p4)
                d = ((x4 - x3) ** 2 + (y4 - y3) ** 2) ** 0.5

                # offset between p3 (receiver) to p1->p2 (emitter) centre axis, i.e. the horizontal distance
                D = ((x5 - x4) ** 2 + (y5 - y4) ** 2) ** 0.5

                phi_z = 0
                zz = [emitter['height'] / 2]  # temporary, currently always set at mid-point vertically.
                for z in zz:
                    pbar.update(n_iter_count - pbar.n)
                    n_iter_count += 1
                    if d > 0:
                        phi = phi_parallel_any_br187(
                            W_m=emitter['width'], H_m=emitter['height'], w_m=0.5 * emitter['width'] + D,
                            h_m=z - emitter['z'][0], S_m=d
                        )
                        if phi > phi_z:
                            phi_z = phi

                phi_arr[i, j] = phi_z

    return phi_arr


def solve_phi_for_single_emitter(
        emitter: dict,
        xx: np.ndarray,
        yy: np.ndarray,
        zz: np.ndarray
) -> np.ndarray:

    emitter = update_emitter(emitter)

    phi = solve_phi(emitter=emitter, xx=xx, yy=yy, zz=zz)

    return phi


def plot_heat_flux_on_ax(
        ax,
        xx: np.ndarray,
        yy: np.ndarray,
        zz: np.ndarray,
        levels: tuple = (0, 5, 12.6, 20, 40, 60, 80),
):

    levels_contour = levels
    colors_contour = ['r' if i == 12.6 else 'k' for i in levels_contour]
    levels_contourf = levels_contour
    colors_contourf = [cm.get_cmap('YlOrRd')(i / (len(levels_contour) - 1)) for i, _ in enumerate(levels_contour)]
    colors_contourf = [(r_, g_, b_, 0.85) for r_, g_, b_, a_ in colors_contourf]


    # create axes
    cs = ax.contour(xx, yy, zz, levels=levels_contour, colors=colors_contour)
    cs_f = ax.contourf(xx, yy, zz, levels=levels_contourf, colors=colors_contourf)


    ax.clabel(cs, inline=1, fontsize=8, fmt='%1.1f kW')

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
    ax.set_xlim((xx.min(), xx.max()))
    ax.set_ylim((yy.min(), xx.max()))

    # axis visibility
    # ax.get_xaxis().set_visible(False)
    # ax.get_yaxis().set_visible(False)
    ax.axis('off')


    return ax



def solve_heat_flux_single_emitter(
        emitter_list: typing.List[dict],
        xx: np.ndarray,
        yy: np.ndarray,
):

    for i in range(len(emitter_list)):
        emitter_list[i] = update_emitter(emitter_list[i])

    heat_flux = np.zeros_like(xx)
    for emitter in emitter_list:
        phi = solve_phi(emitter, xx, yy, np.array([emitter['height']]))
        heat_flux += phi * emitter['heat_flux']

    return heat_flux


def main_plot(input_param_dict: dict, dir_cwd: str = None):

    figsize_width = 10

    # create a figure
    fig = plt.figure(
        figsize=(figsize_width, figsize_width),
        frameon=False,
    )

    for n_count, case_name in enumerate(sorted(input_param_dict.keys())):

        ax = fig.add_subplot(len(input_param_dict), 1, n_count+1)
        ax.set_aspect(aspect=1)
        plot_heat_flux_on_ax(
            ax=ax,
            xx=input_param_dict[case_name]['xx'],
            yy=input_param_dict[case_name]['yy'],
            zz=input_param_dict[case_name]['heat_flux']
        )

        for i in range(len(input_param_dict[case_name]['emitter_list'])):
            ax.plot(input_param_dict[case_name]['emitter_list'][i]['x'], input_param_dict[case_name]['emitter_list'][i]['y'], lw=5, c='k', ls='--')

        ax.set_xlim(*input_param_dict[case_name]['domain']['x'])
        ax.set_ylim(*input_param_dict[case_name]['domain']['y'])

        input_param_dict[case_name]['ax'] = ax

    # fig.tight_layout()
    if dir_cwd:
        dir_cwd = realpath(dir_cwd)

    for case_name in input_param_dict.keys():
        ax = input_param_dict[case_name]['ax']
        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        if dir_cwd:
            fp_fig = join(dir_cwd, f'{case_name}.png')
        else:
            fp_fig = f'{case_name}.png'
        fig.savefig(fp_fig, transparent=True, bbox_inches=extent)

    if dir_cwd:
        fp_fig = join(dir_cwd, 'main.png')
    else:
        fp_fig = 'main.png'

    return input_param_dict, fig


def main(input_param_dict: typing.Dict[str, dict], dir_cwd: str = None):

    # update parameters for each input set
    for case_name in input_param_dict.keys():
        input_param_dict[case_name] = update_input_param(input_param_dict[case_name])

    # update emitter parameters for each emitter in each input set
    for case_name in input_param_dict.keys():
        for i in range(len(input_param_dict[case_name]['emitter_list'])):
            input_param_dict[case_name]['emitter_list'][i] = update_emitter(input_param_dict[case_name]['emitter_list'][i])

    # calculation
    for case_name in input_param_dict.keys():
        input_param_dict[case_name]['heat_flux'] = solve_heat_flux_single_emitter(
            emitter_list=input_param_dict[case_name]['emitter_list'],
            xx=input_param_dict[case_name]['xx'],
            yy=input_param_dict[case_name]['yy'],
        )

    # make plots
    main_plot(input_param_dict, dir_cwd)

    pprint(input_param_dict)


if __name__ == '__main__':

    input_param_dict = dict(
        facade_a = dict(
            emitter_list=[
                dict(
                    x=[0, 15.48],
                    y=[0, 0.00001],
                    # z = [0, 29.5],
                    z=[0, 3.5],
                    heat_flux=84 * (163 / 571),
                ),
                dict(
                    x=[15.48, 28.25],
                    y=[0, 10],
                    # z = [0, 20.7],
                    z=[0, 3.5],
                    heat_flux=84,
                )
            ],
            domain=dict(
                x=(0, 28.25),
                y=(0, 8.66),
            ),
            delta=.5
        ),

        facade_b = dict(
            emitter_list=[
                dict(
                    x=[0, 15.48],
                    y=[0, 0.00001],
                    # z = [0, 29.5],
                    z=[0, 3.5],
                    heat_flux=84 * (163 / 571),
                ),
                dict(
                    x=[15.48, 28.25],
                    y=[0, 10],
                    # z = [0, 20.7],
                    z=[0, 3.5],
                    heat_flux=84,
                )
            ],
            domain=dict(
                x=(0, 28.25),
                y=(0, 8.66),
            ),
            delta=.5
        )
    )

    main(input_param_dict)
