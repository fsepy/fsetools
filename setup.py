import os
import subprocess
import sys
import tempfile

from setuptools import setup
from setuptools import Extension


def _check_c_compiler():
    """Return True if a working MSVC compiler with standard headers is available."""
    if os.environ.get("FSETOOLS_NO_CYTHON"):
        return False

    src = "#include <io.h>\nint main(void) { return 0; }\n"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            src_file = os.path.join(tmp, "test.c")
            exe_file = os.path.join(tmp, "test.exe")
            with open(src_file, "w") as f:
                f.write(src)
            result = subprocess.run(
                ["cl.exe", "/nologo", src_file, f"/Fe:{exe_file}"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0
    except FileNotFoundError:
        return False
    except Exception:
        return False


def _build_cython_extension():
    """Build the Cython extension.  Fails hard if prerequisites are missing."""
    import numpy
    from Cython.Build import cythonize

    extensions = [
        Extension(
            "fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c",
            sources=[
                f"src{os.sep}fsetools{os.sep}lib{os.sep}fse_bs_en_1993_1_2_heat_transfer_c.pyx"
            ],
            include_dirs=[numpy.get_include()],
        ),
    ]
    return cythonize(extensions)


ext_modules = []

if os.environ.get("FSETOOLS_NO_CYTHON"):
    print("FSETOOLS_NO_CYTHON is set — skipping Cython extension build", file=sys.stderr)
elif not _check_c_compiler():
    print(
        "\n" + "=" * 72 + "\n"
        "ERROR: C compiler (MSVC) not found or missing Windows SDK headers.\n"
        "The Cython heat-transfer extension is REQUIRED for this installation.\n\n"
        "Options:\n"
        "  1. Install Visual Studio Build Tools with 'Desktop development with C++'\n"
        "     https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022\n"
        "  2. Run this command from 'Developer PowerShell for VS 2022'\n"
        "  3. Set FSETOOLS_NO_CYTHON=1 to skip (pure-Python fallback will be used)\n"
        + "=" * 72 + "\n",
        file=sys.stderr,
    )
    sys.exit(1)
else:
    ext_modules = _build_cython_extension()

setup(ext_modules=ext_modules)
