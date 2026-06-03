import os
import subprocess
import sys
import tempfile

from setuptools import setup


def _can_compile_c():
    """Return True if a working C compiler with standard headers is available."""
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
    except Exception:
        return False


ext_modules = []

if os.environ.get("FSETOOLS_NO_CYTHON"):
    print("FSETOOLS_NO_CYTHON is set — skipping Cython extension build", file=sys.stderr)
elif not _can_compile_c():
    print(
        "C compiler cannot find standard headers (io.h missing) — "
        "skipping Cython extension. Install Windows SDK or set "
        "FSETOOLS_NO_CYTHON=1 to suppress this check.",
        file=sys.stderr,
    )
else:
    try:
        import numpy
        from Cython.Build import cythonize
        from setuptools import Extension

        extensions = [
            Extension(
                "fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c",
                sources=[
                    f'src{os.sep}fsetools{os.sep}lib{os.sep}fse_bs_en_1993_1_2_heat_transfer_c.pyx'
                ],
                include_dirs=[numpy.get_include()],
            ),
        ]
        ext_modules = cythonize(extensions)
    except Exception as e:
        print(
            f"Warning: Cython extension build skipped due to error: {e}",
            file=sys.stderr,
        )

setup(ext_modules=ext_modules)
