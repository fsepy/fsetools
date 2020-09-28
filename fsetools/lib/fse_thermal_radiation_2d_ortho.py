from typing import Union

import numpy as np
from matplotlib import cm

from fsetools.etc.transforms2d import rotation_meshgrid, angle_between_two_vectors_2d
from fsetools.lib.fse_thermal_radiation import phi_parallel_any_br187, phi_perpendicular_any_br187


class Plane:

    def __init__(
            self,
            x1: float = None,
            x2: float = None,
            y1: float = None,
            y2: float = None,
            z1: float = None,
            z2: float = None,
            parent=None
    ):
        self.__x1: float = x1
        self.__x2: float = x2
        self.__y1: float = y1
        self.__y2: float = y2
        self.__z1: float = z1
        self.__z2: float = z2
        self.__width: float = None
        self.__depth: float = None
        self.__height: float = None
        self.__centroid: tuple = None
        self.parent = parent

    @property
    def x1(self):
        return self.__x1

    @x1.setter
    def x1(self, v: float):
        self.__x1 = v
        self.clear_calculation_catch()

    @property
    def x2(self, minor_offset: bool=True):
        if minor_offset and self.__x2 == self.__x1:
            return self.__x2 + 1e-9
        else:
            return self.__x2

    @x2.setter
    def x2(self, v: float):
        self.__x2 = v
        self.clear_calculation_catch()

    @property
    def y1(self):
        return self.__y1

    @y1.setter
    def y1(self, v: float):
        self.__y1 = v
        self.clear_calculation_catch()

    @property
    def y2(self, minor_offset: bool = True):
        if minor_offset and self.__y2 == self.__y1:
            return self.__y2 + 1e-9
        else:
            return self.__y2

    @y2.setter
    def y2(self, v: float):
        self.__y2 = v
        self.clear_calculation_catch()

    @property
    def z1(self):
        return self.__z1

    @z1.setter
    def z1(self, x: float):
        self.__z1 = x
        self.clear_calculation_catch()

    @property
    def z2(self):
        return self.__z2

    @z2.setter
    def z2(self, v: float):
        self.__z2 = v
        self.clear_calculation_catch()

    def clear_calculation_catch(self):
        self.__width = None
        self.__height = None
        self.__centroid = None

    @property
    def width(self):
        if self.__width is None:
            if self.z1 == self.z2:
                self.__width = abs(self.x2 - self.x1)
            else:
                self.__width = ((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** 0.5
        return self.__width

    @property
    def depth(self):
        if self.__depth is None:
            if self.z1 == self.z2:
                self.__depth = abs(self.y2 - self.y1)
            else:
                self.__depth = 0
        return self.__depth

    @property
    def height(self):
        if self.__height is None:
            self.__height = abs(self.z2 - self.z1)
        return self.__height

    @property
    def centroid(self):
        if self.__centroid is None:
            self.__centroid = self.z2 - self.z1, self.y2 - self.y1, self.z2 - self.z1
        return self.__centroid


def _test_Plane():
    plane1 = Plane(0, 8, 0, 5, 0, 2)  # a diagonal wall
    plane2 = Plane(0, 8, 0, 0, 0, 2)  # a horizontal wall
    plane3 = Plane(0, 0, 0, 5, 0, 2)  # a vertical wall

    # check length method
    assert plane1.height == 2
    assert plane1.width == (8 ** 2 + 5 ** 2) ** 0.5
    assert plane2.width == 8
    assert plane3.width == 5


class Receiver(Plane):
    def __init__(
            self,
            x1: float,
            x2: float,
            y1: float,
            y2: float,
            z: float,
            delta: float,
            parent=None
    ):
        # super properties
        super().__init__(parent=parent)
        self.x1, self.x2, self.y1, self.y2, self.z1, self.z2 = x1, x2, y1, y2, z, z

        # raw properties
        self.__delta = delta

        # resolved properties
        self.__mesh_grid: tuple = tuple([None] * 3)

    @property
    def delta(self):
        return self.__delta

    def correct_coordinates_for_numerical_stability(self):
        if self.x1 == self.x2:
            self.x2 += 1e-9
        if self.y1 == self.y2:
            self.y2 += 1e-9
        if self.z1 == self.z2:
            self.z2 += 1e-9

    @property
    def mesh_grid_3d(self) -> tuple:
        delta = self.delta

        def array(v1, v2, d):
            v = np.arange(v1, v2, d)
            if len(v) > 1:
                return v + 0.5 * d
            else:
                return [0.5 * (v1 + v2)]

        xx, yy, zz = np.meshgrid(
            array(self.x1, self.x2, delta),
            array(self.y1, self.y2, delta),
            array(self.z1, self.z2, delta)
        )

        self.__mesh_grid = (xx, yy, zz)
        return self.__mesh_grid


class Emitter(Plane):

    def __init__(
            self,
            x1: float,
            x2: float,
            y1: float,
            y2: float,
            z1: float,
            z2: float,
            is_parallel: bool,
            receiver: Receiver,
            parent=None
    ):
        # super properties
        super().__init__(parent=parent)
        self.x1, self.x2, self.y1, self.y2, self.z1, self.z2 = x1, x2, y1, y2, z1, z2

        # raw properties
        self.__is_parallel = is_parallel  # 'parallel' or 'perpendicular'
        self.__Receiver = receiver

        # resolved properties
        self.__phi: np.ndarray = None

    def __add__(self, other):
        return self.phi + other.phi

    @property
    def phi(self):
        if self.__phi is None:
            return self.calculate_phi(self.__Receiver)
        else:
            return self.__phi

    def calculate_phi(self, receiver: Receiver):

        if self.__is_parallel:
            phi_func = phi_parallel_any_br187
        else:
            phi_func = phi_perpendicular_any_br187

        # prepare useful variables
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2  # emitter locations

        # solver domain, i.e. the receiver mesh grid
        xx, yy, zz = receiver.mesh_grid_3d

        if self.z2 == self.z1:
            emitter_centroid_x = 0.5 * (self.x1 + self.x2)
            emitter_centroid_y = 0.5 * (self.y1 + self.y2)
            emitter_centroid_z = 0.5 * (self.z1 + self.z2)
        else:
            # transform solver domain so that the emitter is parallel to x-axis
            xx, yy = rotation_meshgrid(xx[:, :, 0], yy[:, :, 0], self.theta_to_x_axis)

            # calculate the emitter surface level, i.e. everything below this level is behind the emitter.
            xx2, yy2 = rotation_meshgrid(np.array((x1, x2)), np.array((y1, y2)), self.theta_to_x_axis)
            try:
                # check if the rated emitter is parallel to x-axis
                assert abs(yy2[0, 0] - yy2[0, -1]) <= 1e-9
            except AssertionError:
                raise AssertionError(yy2[0, 0], yy2[0, -1], 'do not match, rotated emitter is not parallel to x-axis')

            emitter_centroid_x = np.average(xx2)
            emitter_centroid_y = np.average(yy2)
            emitter_centroid_z = 0.5 * (self.z1 + self.z2)

        phiphi = np.zeros_like(zz)
        emitter_width = self.width
        emitter_depth = self.depth
        emitter_height = self.height

        if self.z2 == self.z1:
            for i in range(zz.shape[0]):
                for j in range(zz.shape[1]):
                    for k in range(zz.shape[2]):
                        if zz[i, j, k] > emitter_centroid_z:
                            phiphi[i, j, k] = phi_func(
                                W_m=emitter_width,
                                H_m=emitter_depth,
                                w_m=emitter_centroid_x + abs(emitter_centroid_x - xx[i, j]),
                                h_m=emitter_centroid_y + abs(emitter_centroid_y - yy[i, j]),
                                S_m=zz[i, j, k] - emitter_centroid_z
                            )
        else:
            for i in range(zz.shape[0]):
                for j in range(zz.shape[1]):
                    for k in range(zz.shape[2]):
                        if yy[i, j] > emitter_centroid_y:
                            phiphi[i, j, k] = phi_func(
                                W_m=emitter_width,
                                H_m=emitter_height,
                                w_m=0.5 * emitter_width + abs(emitter_centroid_x - xx[i, j]),
                                h_m=zz[i, j, k],
                                S_m=yy[i, j] - emitter_centroid_y
                            )

        self.__phi = phiphi

        return phiphi

    @property
    def theta_to_x_axis(self):
        v1 = np.subtract((self.x2, self.y2), (self.x1, self.y1))  # wall direction vector
        v2 = (1, 0)  # reference vector
        theta_in_radians = angle_between_two_vectors_2d(v1=v1, v2=v2)
        return theta_in_radians

    @staticmethod
    def heat_flux_2_temperature(heat_flux: float, ambient_temperature: float = 293.15):
        """Function returns surface temperature of an emitter for a given heat flux.

        :param heat_flux: [W/m2] heat flux of emitter.
        :param ambient_temperature: [K] ambient/receiver temperature, 293.15 deg.K by default.
        :return temperature: [K] calculated emitter temperature based on black body radiation model.
        """
        epsilon = 1.0  # radiation view factor
        sigma = 5.67e-8  # [W/m2/K4] stefan-boltzmann constant
        # E_dash_dash_dot = epsilon * sigma * (T_1 ** 4 - T_0 ** 4)  # [W/m2]

        return ((heat_flux / sigma / epsilon) + ambient_temperature ** 4) ** 0.25

    @staticmethod
    def temperature_2_heat_flux(temperature: float, ambient_temperature: float = 293.15):
        """calculates hot surface heat flux for a given temperature.

        :param temperature: [K] emitter temperature.
        :param ambient_temperature: [K] ambient/receiver temperature, 20 deg.C by default.
        :return heat_flux: [K] calculated emitter temperature based on black body radiation model.
        """

        epsilon = 1.0  # radiation view factor
        sigma = 5.67e-8  # [W/m2/K4] stefan-boltzmann constant

        heat_flux = epsilon * sigma * (temperature ** 4 - ambient_temperature ** 4)

        return heat_flux


def _test_Emitter_Receiver():
    import matplotlib.pyplot as plt

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


class CuboidRoomModel:

    def __init__(self, width, depth, height, delta):
        # raw properties
        self.ceiling = Receiver(x1=0, x2=width, y1=0, y2=depth, z=height, delta=delta)
        self.wall_1 = Emitter(x1=0, x2=width, y1=0, y2=0, z1=0, z2=height, is_parallel=False, receiver=self.ceiling)
        self.wall_2 = Emitter(x1=width, x2=width, y1=0, y2=depth, z1=0, z2=height, is_parallel=False,
                              receiver=self.ceiling)
        self.wall_3 = Emitter(x1=width, x2=0, y1=depth, y2=depth, z1=0, z2=height, is_parallel=False,
                              receiver=self.ceiling)
        self.wall_4 = Emitter(x1=0, x2=0, y1=depth, y2=0, z1=0, z2=height, is_parallel=False, receiver=self.ceiling)
        self.floor = Emitter(x1=0, x2=width, y1=0, y2=depth, z1=0, z2=0, is_parallel=True, receiver=self.ceiling)

        # resolved properties
        self.__wall_1_heat_flux: float = None
        self.__wall_2_heat_flux: float = None
        self.__wall_3_heat_flux: float = None
        self.__wall_4_heat_flux: float = None
        self.__floor_heat_flux: float = None
        self.__ceiling_temperature: float = None
        self.__phi: np.ndarray = None

    @property
    def resultant_phi(self):
        if self.__phi is None:
            phi_1 = self.wall_1.phi
            phi_2 = self.wall_2.phi
            phi_3 = self.wall_3.phi
            phi_4 = self.wall_4.phi
            phi_5 = self.floor.phi
            self.__phi = phi_1 + phi_2 + phi_3 + phi_4 + phi_5
        return self.__phi

    def resultant_heat_flux(self, heat_flux: Union[list, tuple]):
        q1, q2, q3, q4, q5 = heat_flux

        q1r = self.wall_1.phi * q1 if q1 else 0
        q2r = self.wall_2.phi * q2 if q2 else 0
        q3r = self.wall_3.phi * q3 if q3 else 0
        q4r = self.wall_4.phi * q4 if q4 else 0
        q5r = self.floor.phi * q5 if q5 else 0

        return q1r + q2r + q3r + q4r + q5r


def _test_CuboidRoomModel():
    model = CuboidRoomModel(width=5, depth=3, height=2, delta=0.05)

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.imshow(model.resultant_heat_flux((1, 0, 0, 0, 0))[:, :, 0])
    ax.invert_yaxis()

    plt.show()


def _test_visual_CuboidRoomModel():

    import matplotlib.pyplot as plt

    model = CuboidRoomModel(width=15, depth=3, height=2, delta=0.05)
    resultant_heat_flux = model.resultant_heat_flux((100, 100, 100, 100, 100))[:, :, 0]
    xx, yy, zz = model.ceiling.mesh_grid_3d
    xx, yy = xx[:, :, 0], yy[:, :, 0]

    fig, ax = plt.subplots()

    figure_levels = np.linspace(np.amin(resultant_heat_flux), np.amax(resultant_heat_flux), 15)

    figure_levels_contour = figure_levels
    figure_colors_contour = ['k'] * len(figure_levels)
    figure_colors_contourf = [cm.get_cmap('YlOrRd')(i / (len(figure_levels) - 1)) for i, _ in enumerate(figure_levels)]
    figure_colors_contourf = [(r_, g_, b_, 1) for r_, g_, b_, a_ in figure_colors_contourf]

    # create axes
    cs = ax.contour(xx, yy, resultant_heat_flux, levels=figure_levels, colors=figure_colors_contour)
    cs_f = ax.contourf(xx, yy, resultant_heat_flux, levels=figure_levels, colors=figure_colors_contourf)

    ax.clabel(cs, inline=1, fontsize='small', fmt='%1.1f kW')

    ax.grid(b=True, which='major', axis='both', color='k', alpha=0.1)

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

    cbar = fig.colorbar(cs_f)
    cbar.ax.set_yticklabels([f'{i:.1f}'.rstrip('0').rstrip('.') + '\nkW/m²' for i in figure_levels])

    fig.tight_layout()

    plt.show()


if __name__ == '__main__':
    _test_Plane()
    _test_Emitter_Receiver()
    _test_CuboidRoomModel()
    _test_visual_CuboidRoomModel()
