#!/usr/bin/env python

import os
from codecs import open  # To use a consistent encoding

import numpy as np
import setuptools
from Cython.Build import cythonize
from setuptools import Extension

import fsetools

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md")) as f:
    long_description = f.read()

try:
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")) as f:
        requirements = f.read().splitlines()

extensions = [
    Extension("fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c", [os.path.join('fsetools', 'lib', 'fse_bs_en_1993_1_2_heat_transfer_c.pyx')], include_dirs=[np.get_include()])
]

setuptools.setup(
    name="fsetools",
    version=fsetools.__version__,
    description="Fire Safety Engineering Tools",
    author="Ian Fu",
    author_email=''.join([chr(ord(v) + i) for i, v in enumerate(r'ftw^jn:`eX_a"Va^')]),
    url="https://github.com/fsepy/fsetools",
    download_url="https://github.com/fsepy/fsetools/archive/master.zip",
    keywords=["fire", "safety", "engineering"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "fsetools",
        "fsetools.etc",
        "fsetools.lib",
        "fsetools.libstd",
    ],
    ext_modules=cythonize(extensions),
    install_requires=requirements,
    include_package_data=True,
)
