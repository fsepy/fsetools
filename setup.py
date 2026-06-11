import os
import sys

from setuptools import setup
from setuptools import Extension


ext_modules = []

if os.environ.get("FSETOOLS_NO_CYTHON"):
    print("FSETOOLS_NO_CYTHON is set — skipping Cython extension build", file=sys.stderr)
else:
    import numpy
    from Cython.Build import cythonize

    try:
        ext_modules = cythonize([
            Extension(
                "fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c",
                sources=[
                    f"src{os.sep}fsetools{os.sep}lib{os.sep}fse_bs_en_1993_1_2_heat_transfer_c.pyx"
                ],
                include_dirs=[numpy.get_include()],
            ),
        ])
    except Exception as e:
        print(
            "\n" + "=" * 72 + "\n"
            "ERROR: Failed to compile the Cython heat-transfer extension.\n\n"
            f"{e}\n\n"
            "Options:\n"
            "  1. Install Visual Studio Build Tools with 'Desktop development with C++'\n"
            "     https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022\n"
            "  2. Run from 'Developer PowerShell for VS 2022'\n"
            "  3. Set FSETOOLS_NO_CYTHON=1 to skip (pure-Python fallback)\n"
            + "=" * 72 + "\n",
            file=sys.stderr,
        )
        sys.exit(1)

setup(ext_modules=ext_modules)
