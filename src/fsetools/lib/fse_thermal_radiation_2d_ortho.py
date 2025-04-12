from typing import Union

import numpy as np

from .fse_thermal_radiation import phi_parallel_any_br187, phi_perpendicular_any_br187
from ..etc.transforms2d import rotation_meshgrid, angle_between_two_vectors_2d


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
    def x2(self, minor_offset: bool = True):
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
