#!/usr/bin/env python

import os
from codecs import open  # To use a consistent encoding

import setuptools

import fseutil

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md")) as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="fseutil",
    version=fseutil.__version__,
    description="Fire Safety Engineering Utility Tools",
    author="Ian Fu",
    author_email="fuyans@gmail.com",
    url="https://github.com/fsepy/fseutil",
    download_url="https://github.com/fsepy/fseutil/archive/master.zip",
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
        "fseutil",
        "fseutil.cli",
        "fseutil.etc",
        "fseutil.gui",
        "fseutil.gui.layout",
        "fseutil.gui.logic",
        "fseutil.lib",
        "fseutil.libstd",
    ],
    install_requires=requirements,
    include_package_data=True,
    entry_points={"console_scripts": ["fseutil=fseutil.cli.__main__:main"]},
)
