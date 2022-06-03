from typing import Union

import numpy as np


# from matplotlib.path import Path


class Phi(object):
    def __init__(self):
        pass

    def calc(self, xyzn1: np.ndarray, xyzn2: np.ndarray) -> np.ndarray:
        """

        :param xyzn1:
            A list of singularities 1
            [[x1, y1, z1, nx1, ny1, nz1], [x2, y2, z2, nx2, ny2, nz2], ...]
            Where x y and z describes location of a vertex and nx, xy and xz describes the norm of the vertex.
        :param xyzn2:
            A list of singularities 2
        :return:

        Phi_1_2 = 1/A_2 integral(cos(theta_1) * cos(theta_2) / pi / S**2)dA_2

        Becomes to

        Phi_1_2 = cos(theta_1) * cos(theta_2) / pi / S**2
        """

        pass

    @staticmethod
    def unit_vector(v: np.ndarray) -> np.ndarray:
        """

        :param v:
            Vectors
            [[x1, y1, z1], [x2, y2, z2], ...]
        :return:
        """

        n = np.linalg.norm(v, axis=1)
        u = v / np.reshape(n, (n.shape[0], 1))

        return u

    @staticmethod
    def angle_between(v1: Union[tuple, list, np.ndarray], v2: Union[tuple, list, np.ndarray]) -> np.ndarray:
        """
        Calculates the angle between two vectors in radians.

        :param v1:  [[x1, y1, z1], [x2, y2, z2], ...] defines the first vector
        :param v2:  [[x1, y1, z1], [x2, y2, z2], ...] or [x1, y1, z1] defines the second vector
        :return:    Angle between `v1` and `v2` in radians. NB no angles are greater than pi (or 90 degrees)
        """

        unit_vector = Phi.unit_vector

        """ Returns the angle in theta_in_radians between vectors 'v1' and 'v2' """
        v1_u = unit_vector(v1)
        v2_u = unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


class TestPhi(Phi):
    def __init__(self):
        super().__init__()

    def run(self):
        self.test_unit_vector()

    def test_unit_vector(self):
        # single case
        print('hello')

        pass


if __name__ == '__main__':
    TestPhi().run()
