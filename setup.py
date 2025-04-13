import os

import numpy
from Cython.Build import cythonize
from setuptools import Extension, setup

extensions = [
    Extension("fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c",
              sources=[f'src{os.sep}fsetools{os.sep}lib{os.sep}fse_bs_en_1993_1_2_heat_transfer_c.pyx'],
              include_dirs=[numpy.get_include()]),
]

setup(
    ext_modules=cythonize(extensions)
)
