def test_solve_phi():
    import numpy as np
    from .fse_thermal_radiation_2d_parallel import solver_phi_2d, phi_parallel_any_br187
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
    answer = phi_parallel_any_br187(width, height, 0.5 * width + x_emitter_centre, 0.5 * height + y_emitter_centre,
                                    separation)
    print('assertion values', solved, answer)
    assert np.isclose(solved, answer, atol=1e-6)

    # measure at 5 m from the emitter front, offset 5 m x-axis (i.e. edge centre)
    solved = helper_get_phi_at_specific_point(xx, yy, phi, x_emitter_centre - 5, separation + y_emitter_centre)
    answer = phi_parallel_any_br187(width, height, 0.5 * width + x_emitter_centre - 5, 0.5 * height + y_emitter_centre,
                                    separation)
    print('assertion values', solved, answer)
    assert np.isclose(solved, answer, atol=1e-6)

    # measure at 5 m from the emitter back
    solved = helper_get_phi_at_specific_point(xx, yy, phi, x_emitter_centre, separation + y_emitter_centre)
    answer = phi_parallel_any_br187(width, height, 0.5 * width + x_emitter_centre, 0.5 * height + y_emitter_centre,
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
    answer = phi_parallel_any_br187(width, height, 0.5 * width + x_emitter_centre - 5,
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
    answer = phi_parallel_any_br187(width, height, 0.5 * width + x_emitter_centre - 7.5,
                                    0.5 * height + y_emitter_centre - 5., separation)
    print('assertion values', solved, answer)
    assert np.isclose(solved, answer, atol=1e-6)

    # fig, ax = plt.subplots()
    # ax.contourf(xx, yy, phi)
    # ax.set_aspect(1)
    # plt.show()


def test_main():
    from .fse_thermal_radiation_2d_parallel import main, main_plot
    import numpy as np

    # ======
    # test 0
    # ======
    # test interface

    param_dict = dict(
        emitter_list=[
            dict(
                x=[-5, 0],
                y=[0, 0],
                z=[0, 2],
                heat_flux=100,
            ),
            dict(
                x=[0, 5],
                y=[0, 0],
                z=[0, 4],
                heat_flux=100,
            )
        ],
        receiver_list=[
            dict(
                x=[-0.5, 0.5],
                y=[-0.5, -0.5],
            )
        ],
        solver_domain=dict(
            x=(-10, 10),
            y=(-1, 10),
            z=None
        ),
        solver_delta=.2
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

    import matplotlib.pyplot as plt
    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots()
    _, ax = main_plot(out, ax, fig)
    plt.show()


if __name__ == '__main__':
    test_solve_phi()
    test_main()
