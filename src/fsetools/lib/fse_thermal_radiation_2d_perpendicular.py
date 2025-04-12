import typing

import numpy as np

# from .fse_thermal_radiation import phi_parallel_any_br187
from .fse_thermal_radiation import phi_perpendicular_any_br187
from ..etc.transforms2d import rotation_meshgrid, angle_between_two_vectors_2d


def main_plot(
        param_dict: dict,
        ax,
        fig=None,
        critical_heat_flux: float = 12.6,
        contour_line_font_size: float = 12,
        emitter_receiver_line_thickness: float = 5.,
        **kwargs
):
    x1, x2 = param_dict['solver_domain']['x']
    y1, y2 = param_dict['solver_domain']['y']
    delta = param_dict['solver_delta']
    xx, yy = np.meshgrid(np.arange(x1, x2 + 0.5 * delta, delta), np.arange(y1, y2 + 0.5 * delta, delta))
    zz = param_dict['heat_flux']

    if 'figure_levels' in param_dict:
        figure_levels = param_dict['figure_levels']
    else:
        figure_levels = (0, 12.6, 20, 40, 60, 80, 200)
    # figure_levels = list(figure_levels) + [critical_heat_flux]
    figure_levels = tuple(sorted(set(figure_levels)))

    # figure_levels_contour = figure_levels
    # figure_colors_contour = ['r' if i == critical_heat_flux else 'k' for i in figure_levels_contour]
    # figure_levels_contourf = figure_levels_contour
    # figure_colors_contourf = [cm.get_cmap('YlOrRd')(i / (len(figure_levels_contour) - 1)) for i, _ in
    #                           enumerate(figure_levels_contour)]
    # figure_colors_contourf = [(r_, g_, b_, a_) for r_, g_, b_, a_ in figure_colors_contourf]
    # figure_colors_contourf[0] = (195 / 255, 255 / 255, 143 / 255, 0.65)

    # create axes
    # cs = ax.contour(xx, yy, zz, levels=figure_levels_contour, colors=figure_colors_contour)
    cs_f = ax.contourf(xx, yy, zz, levels=figure_levels)

    # if contour_line_font_size > 0:
    #     ax.clabel(cs, inline=1, fontsize=contour_line_font_size, fmt='%1.1f kW')

    ax.grid(b=True, which='major', axis='both', color='k', alpha=0.1)

    # axis ticks
    ax.set_xticks(np.arange(np.amin(xx), np.amax(xx) + .5, 1))
    # ax.set_xticklabels('')
    ax.set_yticks(np.arange(np.amin(yy), np.amax(yy) + .5, 1))
    # ax.set_yticklabels('')
    ax.tick_params(axis=u'both', which=u'both', direction='in')

    # axis limits
    ax.set_xlim((np.amin(xx), np.amax(xx)))
    ax.set_ylim((np.amin(yy), np.amax(yy)))

    ax.set_aspect(1)

    if emitter_receiver_line_thickness > 0:
        for i in range(len(param_dict['emitter_list'])):
            ax.plot(param_dict['emitter_list'][i]['x'], param_dict['emitter_list'][i]['y'],
                    lw=emitter_receiver_line_thickness, c='r', ls='--')

        try:
            for i in range(len(param_dict['receiver_list'])):
                ax.plot(param_dict['receiver_list'][i]['x'], param_dict['receiver_list'][i]['y'],
                        lw=emitter_receiver_line_thickness, c='k', ls='--')
        except KeyError:
            pass

    ax.set_xlim(*param_dict['solver_domain']['x'])
    ax.set_ylim(*param_dict['solver_domain']['y'])

    # colour bar, only plot colorbar when figure object is provided to prevent double plotting
    if fig:
        cbar = fig.colorbar(cs_f)
        cbar.ax.set_yticklabels([f'{i:.1f}'.rstrip('0').rstrip('.') + '\nkW/m²' for i in figure_levels])

    return fig, ax


def main_plot_plotly(
        param_dict: dict,
        critical_heat_flux: float = 12.6,
        contour_line_font_size: float = 12,
        emitter_receiver_line_thickness: float = 5.,
        **kwargs
):
    x1, x2 = param_dict['solver_domain']['x']
    y1, y2 = param_dict['solver_domain']['y']
    delta = param_dict['solver_delta']
    xx, yy = np.meshgrid(np.arange(x1, x2 + 0.5 * delta, delta), np.arange(y1, y2 + 0.5 * delta, delta))
    zz = param_dict['heat_flux']

    import plotly.graph_objects as go

    fig = go.Figure(data=
    go.Contour(
        z=zz,
        x=np.arange(x1, x2 + 0.5 * delta, delta),  # horizontal axis
        y=np.arange(y1, y2 + 0.5 * delta, delta)  # vertical axis
    ))
    fig.show()

    return


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


def solver_phi_2d(
        emitter_xy1: typing.Union[list, tuple, np.ndarray],
        emitter_xy2: typing.Union[list, tuple, np.ndarray],
        emitter_z: typing.Union[list, tuple, np.ndarray],
        xx: typing.Union[list, tuple, np.ndarray],
        yy: typing.Union[list, tuple, np.ndarray],
        z: float,
) -> np.ndarray:
    """

    :param emitter:
    :param xx:
    :param yy:
    :param z:
    :return:
    """

    # calculate the angle between a flat line (1, 0) and the emitter plane on z-plane
    v1 = np.subtract(emitter_xy2, emitter_xy1)
    v2 = (1, 0)
    theta_in_radians = angle_between_two_vectors_2d(v1=v1, v2=v2)

    # solver domain
    xx, yy = rotation_meshgrid(xx, yy, theta_in_radians)

    # calculate the emitter surface level, i.e. everything below this level is behind the emitter.
    x1, y1 = emitter_xy1
    x2, y2 = emitter_xy2
    emitter_x, emitter_y = rotation_meshgrid(np.array((x1, x2)), np.array((y1, y2)), theta_in_radians)
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
    emitter_height = abs(emitter_z[0] - emitter_z[1])
    emitter_width = sum(np.square(np.subtract(emitter_xy1, emitter_xy2))) ** 0.5
    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            y = yy[i, j]
            if y > surface_level_y:
                vv[i, j] = phi_perpendicular_any_br187(
                    W_m=emitter_width,
                    H_m=emitter_height,
                    w_m=0.5 * emitter_width + abs(emitter_x_centre - xx[i, j]),
                    h_m=z,
                    S_m=y - surface_level_y
                )

    # check phi
    # plt.contourf(xx, yy, vv)
    # plt.show()
    # print(theta_in_radians)

    return vv


def _test_solve_phi():
    def helper_get_phi_at_specific_point(xx, yy, vv, x, y):
        v = vv[(np.isclose(xx, x)) & np.isclose(yy, y)]
        print('measured location and value', x, y, v, '.')
        return v

    xx, yy = np.meshgrid(np.arange(-20, 20, .1), np.arange(-20, 20, .1))

    width = 7
    height = 5
    separation = 5

    x_emitter_centre = 0
    y_emitter_centre = 0
    z_emitter_centre = 0

    phi = solver_phi_2d(
        emitter_xy1=[-width / 2 + x_emitter_centre, y_emitter_centre],
        emitter_xy2=[width / 2 + x_emitter_centre, y_emitter_centre],
        emitter_z=[-height / 2 + z_emitter_centre, height / 2 + z_emitter_centre],
        xx=xx,
        yy=yy,
        z=height / 2
    )

    # measure at 5 m from the emitter front
    solved = helper_get_phi_at_specific_point(xx, yy, phi, x_emitter_centre, separation + y_emitter_centre)
    answer = phi_perpendicular_any_br187(width, height, 0.5 * width + x_emitter_centre, 0.5 * height + y_emitter_centre,
                                         separation)
    print('assertion values', solved, answer)
    assert np.isclose(solved, answer, atol=1e-6)

    # measure at 5 m from the emitter front, offset 5 m x-axis (i.e. edge centre)
    solved = helper_get_phi_at_specific_point(xx, yy, phi, x_emitter_centre - 5, separation + y_emitter_centre)
    answer = phi_perpendicular_any_br187(width, height, 0.5 * width + x_emitter_centre - 5,
                                         0.5 * height + y_emitter_centre,
                                         separation)
    print('assertion values', solved, answer)
    assert np.isclose(solved, answer, atol=1e-6)

    # measure at 5 m from the emitter back
    solved = helper_get_phi_at_specific_point(xx, yy, phi, x_emitter_centre, separation + y_emitter_centre)
    answer = phi_perpendicular_any_br187(width, height, 0.5 * width + x_emitter_centre, 0.5 * height + y_emitter_centre,
                                         separation)
    print('assertion values', solved, answer)
    assert np.isclose(solved, answer, atol=1e-6)

    # measure at 5 m from the emitter front, offset 5 m x-axis and 2.5 m z-zxis (i.e. corner)
    phi = solver_phi_2d(
        emitter_xy1=[-width / 2 + x_emitter_centre, y_emitter_centre],
        emitter_xy2=[width / 2 + x_emitter_centre, y_emitter_centre],
        emitter_z=[-height / 2 + z_emitter_centre, height / 2 + z_emitter_centre],
        xx=xx,
        yy=yy,
        z=height / 2 - 2.5
    )
    solved = helper_get_phi_at_specific_point(xx, yy, phi, x_emitter_centre - 5, separation + y_emitter_centre)
    answer = phi_perpendicular_any_br187(width, height, 0.5 * width + x_emitter_centre - 5,
                                         0.5 * height + y_emitter_centre - 2.5, separation)
    print('assertion values', solved, answer)
    assert np.isclose(solved, answer, atol=1e-6)

    # measure at 5 m from the emitter front, offset 7.5 m x-axis and 5 m z-zxis (i.e. outside of the rectangle by 2.5 and 2.5 m)
    phi = solver_phi_2d(
        emitter_xy1=[-width / 2 + x_emitter_centre, y_emitter_centre],
        emitter_xy2=[width / 2 + x_emitter_centre, y_emitter_centre],
        emitter_z=[-height / 2 + z_emitter_centre, height / 2 + z_emitter_centre],
        xx=xx,
        yy=yy,
        z=height / 2 - 5
    )
    solved = helper_get_phi_at_specific_point(xx, yy, phi, x_emitter_centre - 7.5, separation + y_emitter_centre)
    answer = phi_perpendicular_any_br187(width, height, 0.5 * width + x_emitter_centre - 7.5,
                                         0.5 * height + y_emitter_centre - 5., separation)
    print('assertion values', solved, answer)
    assert np.isclose(solved, answer, atol=1e-6)

    # fig, ax = plt.subplots()
    # ax.contourf(xx, yy, phi)
    # ax.set_aspect(1)
    # plt.show()


def main(params_dict: dict, QtCore_ProgressSignal=None):
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
                    z=(z1, z2)
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
    z2, z1 = -np.inf, np.inf

    for emitter in params_dict['emitter_list']:
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
            emitter['x'] = (emitter['x'][0], emitter['x'][1] + 1e-9)
        if emitter['y'][0] == emitter['y'][1]:
            emitter['y'] = (emitter['y'][0], emitter['y'][1] + 1e-9)

        if min(emitter['z']) < z1:
            z1 = min(emitter['z'])
        if max(emitter['z']) > z2:
            z2 = max(emitter['z'])

    # ==============================
    # calculate configuration factor
    # ==============================

    x1, x2 = params_dict['solver_domain']['x']
    y1, y2 = params_dict['solver_domain']['y']
    delta = params_dict['solver_delta']
    xx, yy = np.arange(x1, x2 + 0.5 * delta, delta), np.arange(y1, y2 + 0.5 * delta, delta)
    xx, yy = np.meshgrid(xx, yy)
    if params_dict['solver_domain']['z']:
        if len(params_dict['solver_domain']['z']) == 2:
            if params_dict['solver_domain']['z'][0] == params_dict['solver_domain']['z'][1]:
                zz = [params_dict['solver_domain']['z'][0]]
            else:
                zz = np.arange(params_dict['solver_domain']['z'][0], params_dict['solver_domain']['z'][1] + 0.5 * delta,
                               delta)
        elif len(params_dict['solver_domain']['z']) == 1:
            zz = params_dict['solver_domain']['z']
        else:
            raise ValueError('solver_domain:z length can only be 1 or 2.')
    else:
        zz = np.arange(z1, z2 + 0.5 * delta, delta)

    n_calc = len(zz) * len(params_dict['emitter_list'])
    n_count = 0

    for z in zz:
        phi = np.zeros_like(xx)
        for i, emitter in enumerate(params_dict['emitter_list']):
            if QtCore_ProgressSignal:
                QtCore_ProgressSignal.emit(n_count / n_calc * 100)
            phi_ = solver_phi_2d(
                emitter_xy1=(emitter['x'][0], emitter['y'][0]),
                emitter_xy2=(emitter['x'][1], emitter['y'][1]),
                emitter_z=emitter['z'],
                xx=xx,
                yy=yy,
                z=z,
            )
            phi += phi_
            if 'phi_dict' in emitter:
                emitter['phi_dict'][f'{z:.3f}'] = phi_
            else:
                emitter['phi_dict'] = {f'{z:.3f}': phi_}
            n_count += 1

    if QtCore_ProgressSignal:
        QtCore_ProgressSignal.emit(100)

    # =============================
    # calculate resultant heat flux
    # =============================

    for z in zz:
        heat_flux = np.zeros_like(xx, dtype=np.float64)
        for emitter in params_dict['emitter_list']:
            heat_flux += emitter['heat_flux'] * emitter['phi_dict'][f'{z:.3f}']
        if 'heat_flux_dict' in params_dict:
            params_dict['heat_flux_dict'][f'{z:.3f}'] = heat_flux
        else:
            params_dict['heat_flux_dict'] = {f'{z:.3f}': heat_flux}

    heat_flux = np.max(np.array([i for i in params_dict['heat_flux_dict'].values()]), axis=0)
    heat_flux[heat_flux == 0] = -1
    params_dict['heat_flux'] = heat_flux

    # make plots
    # main_plot(params_dict)

    return params_dict


def _test_main():
    import plotly.graph_objects as go

    # ======
    # test 0
    # ======
    # test interface

    param_dict = dict(
        emitter_list=[
            dict(
                x=[0, 5],
                y=[0, 0],
                z=[0, 2],
                heat_flux=100,
            ),
            dict(
                x=[5, 5],
                y=[0, 2],
                z=[0, 2],
                heat_flux=100,
            ),
            dict(
                x=[5, 0],
                y=[2, 2],
                z=[0, 2],
                heat_flux=100,
            ),
            dict(
                x=[0, 0],
                y=[2, 0],
                z=[0, 2],
                heat_flux=50,
            ),
        ],
        receiver_list=[
            # dict(
            #     x=[-0.5, 0.5],
            #     y=[-0.5, -0.5],
            # )
        ],
        solver_domain=dict(
            x=(0, 5),
            y=(0, 2),
            z=(2, 2)
        ),
        solver_delta=.025,
        figure_levels=np.arange(40, 100 + 5, 5)
    )

    out = main(param_dict)

    # check phi dimension
    x1, x2 = out['solver_domain']['x']
    y1, y2 = out['solver_domain']['y']
    delta = out['solver_delta']
    xx, yy = np.meshgrid(np.arange(x1, x2 + 0.5 * delta, delta), np.arange(y1, y2 + 0.5 * delta, delta))
    print('assertion', out['heat_flux'].shape, xx.shape, yy.shape)
    assert out['heat_flux'].shape == xx.shape == yy.shape

    # check output elements
    print('assertion', list(out['emitter_list'][0].keys()))
    for emitter in out['emitter_list']:
        assert 'phi_dict' in emitter
        assert 'height' in emitter
        assert 'width' in emitter

    x1, x2 = param_dict['solver_domain']['x']
    y1, y2 = param_dict['solver_domain']['y']
    delta = param_dict['solver_delta']
    zz = param_dict['heat_flux']

    fig = go.Figure(data=
    go.Contour(
        z=zz,
        x=np.arange(x1, x2 + 0.5 * delta, delta),  # horizontal axis
        y=np.arange(y1, y2 + 0.5 * delta, delta)  # vertical axis
    ))
    fig.show()


if __name__ == '__main__':
    _test_main()
    # _test_solve_phi()
