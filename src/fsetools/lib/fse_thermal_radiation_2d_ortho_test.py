from .fse_thermal_radiation_2d_ortho import *


def test_Plane():
    plane1 = Plane(0, 8, 0, 5, 0, 2)  # a diagonal wall
    plane2 = Plane(0, 8, 0, 0, 0, 2)  # a horizontal wall
    plane3 = Plane(0, 0, 0, 5, 0, 2)  # a vertical wall

    # check length method
    assert plane1.height == 2
    assert plane1.width == (8 ** 2 + 5 ** 2) ** 0.5
    assert plane2.width == 8
    assert plane3.width == 5


def test_Emitter_Receiver():
    import matplotlib.pyplot as plt
    plt.style.use("seaborn-v0_8")

    receiver1 = Receiver(0, 1, 0, 1, 2, 0.5)
    receiver2 = Receiver(0, 1, 0, 1, 2, 0.2)
    receiver3 = Receiver(0, 1, 0, 1, 2, 0.1)
    receiver4 = Receiver(0, 1, 0, 1, 2, 0.05)
    receiver = Receiver(0, 1, 0, 1, 2, 0.02)

    emitter1 = Emitter(0, 1, 0, 0, 0, 2, is_parallel=True, receiver=receiver1)
    emitter2 = Emitter(0, 1, 0, 0, 0, 2, is_parallel=True, receiver=receiver2)
    emitter3 = Emitter(0, 1, 0, 0, 0, 2, is_parallel=True, receiver=receiver3)
    emitter4 = Emitter(0, 1, 0, 0, 0, 2, is_parallel=True, receiver=receiver4)

    emitter5 = Emitter(0, 1, 0, 0, 0, 2, is_parallel=True, receiver=receiver)
    emitter6 = Emitter(0, 1, 0, 0, 0, 2, is_parallel=False, receiver=receiver)
    emitter7 = Emitter(0, 1, 0, 1, 0, 2, is_parallel=True, receiver=receiver)
    emitter8 = Emitter(0, 1, 0, 1, 0, 2, is_parallel=False, receiver=receiver)

    emitter9 = Emitter(0, 1, 0, 1, 0, 2, is_parallel=True, receiver=receiver)
    emitter10 = Emitter(1, 0, 0, 1, 0, 2, is_parallel=True, receiver=receiver)
    emitter11 = Emitter(1, 0, 1, 0, 0, 2, is_parallel=True, receiver=receiver)
    emitter12 = Emitter(0, 1, 1, 0, 0, 2, is_parallel=True, receiver=receiver)

    emitter13 = Emitter(0, 1, 0, 1, 0, 0, is_parallel=True, receiver=receiver)
    emitter14 = Emitter(0, 1, 0, 1, 0.5, 0.5, is_parallel=True, receiver=receiver)
    emitter15 = Emitter(0, 1, 0, 1, 1, 1, is_parallel=True, receiver=receiver)
    emitter16 = Emitter(0, 1, 0, 1, 1.5, 1.5, is_parallel=True, receiver=receiver)

    fig = plt.figure()

    def add_ax(n, data, title, r=4, c=4):
        ax = fig.add_subplot(r, c, n)
        ax.set_title(title, fontsize='small')
        ax.imshow(data[:, :, 0])
        ax.invert_yaxis()

    add_ax(1, emitter1.phi, 'delta = 0.5')
    add_ax(2, emitter2.phi, 'delta = 0.2')
    add_ax(3, emitter3.phi, 'delta = 0.1')
    add_ax(4, emitter4.phi, 'delta = 0.05')

    add_ax(5, emitter5.phi, 'horizontal parallel')
    add_ax(6, emitter6.phi, 'horizontal perpendicular')
    add_ax(7, emitter7.phi, 'diagonal parallel')
    add_ax(8, emitter8.phi, 'diagonal perpendicular')

    add_ax(9, emitter9.phi, 'perpendicular 1')
    add_ax(10, emitter10.phi, 'perpendicular 2')
    add_ax(11, emitter11.phi, 'perpendicular 3')
    add_ax(12, emitter12.phi, 'perpendicular 4')

    add_ax(13, emitter13.phi, 'flat 2 m')
    add_ax(14, emitter14.phi, 'flat 1.5 m')
    add_ax(15, emitter15.phi, 'flat 1 m')
    add_ax(16, emitter16.phi, 'flat 0.5 m')

    fig.tight_layout()
    plt.show()


def test_CuboidRoomModel():
    model = CuboidRoomModel(width=5, depth=3, height=2, delta=0.05)

    import matplotlib.pyplot as plt
    plt.style.use("seaborn-v0_8")

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.imshow(model.resultant_heat_flux((1, 0, 0, 0, 0))[:, :, 0])
    ax.invert_yaxis()

    plt.show()


def test_visual_CuboidRoomModel():
    import matplotlib.pyplot as plt
    plt.style.use("seaborn-v0_8")
    from matplotlib import cm

    model = CuboidRoomModel(width=15, depth=3, height=2, delta=0.05)
    resultant_heat_flux = model.resultant_heat_flux((100, 100, 100, 100, 100))[:, :, 0]
    xx, yy, zz = model.ceiling.mesh_grid_3d
    xx, yy = xx[:, :, 0], yy[:, :, 0]

    fig, ax = plt.subplots()

    figure_levels = np.linspace(np.amin(resultant_heat_flux), np.amax(resultant_heat_flux), 15)

    figure_colors_contour = ['k'] * len(figure_levels)
    figure_colors_contourf = [cm.get_cmap('YlOrRd')(i / (len(figure_levels) - 1)) for i, _ in enumerate(figure_levels)]
    figure_colors_contourf = [(r_, g_, b_, 1) for r_, g_, b_, a_ in figure_colors_contourf]

    # create axes
    cs = ax.contour(xx, yy, resultant_heat_flux, levels=figure_levels, colors=figure_colors_contour)
    cs_f = ax.contourf(xx, yy, resultant_heat_flux, levels=figure_levels, colors=figure_colors_contourf)

    ax.clabel(cs, inline=1, fontsize='small', fmt='%1.1f kW')

    ax.grid(which='major', axis='both', color='k', alpha=0.1)

    # axis ticks
    ax.set_xticks(np.arange(np.amin(xx), np.amax(xx) + .5, 1))
    ax.set_xticklabels([f'{i:.0f}' for i in np.arange(np.amin(xx), np.amax(xx) + .5, 1)], fontsize=9)
    ax.set_yticks(np.arange(np.amin(yy), np.amax(yy) + .5, 1))
    ax.set_yticklabels([f'{i:.0f}' for i in np.arange(np.amin(yy), np.amax(yy) + .5, 1)], fontsize=9)
    ax.tick_params(axis=u'both', which=u'both', direction='in')

    # axis limits
    ax.set_xlim((np.amin(xx), np.amax(xx)))
    ax.set_ylim((np.amin(yy), np.amax(yy)))

    ax.set_aspect(1)

    try:
        cbar = fig.colorbar(cs_f)
        cbar.ax.set_yticklabels([f'{i:.1f}'.rstrip('0').rstrip('.') + '\nkW/m²' for i in figure_levels])
    except:
        pass

    fig.tight_layout()

    plt.show()


if __name__ == '__main__':
    test_Plane()
    test_CuboidRoomModel()
    test_Emitter_Receiver()
    test_visual_CuboidRoomModel()
