"""Opt-in visual display utilities for development inspection.

Set the environment variable ``FSETOOLS_SHOW_PLOTS=1`` to display plots
during test runs.  When unset, ``show()`` is a no-op.
"""

import os
from typing import Optional


def show(fig: Optional[object] = None) -> None:
    """Call ``plt.show()`` (or ``fig.show()``) only when FSETOOLS_SHOW_PLOTS=1."""
    if os.environ.get("FSETOOLS_SHOW_PLOTS") == "1":
        import matplotlib.pyplot as _plt

        if fig is not None:
            fig.show()
        else:
            _plt.show()


def show_blocking(fig: Optional[object] = None) -> None:
    """Same as ``show()`` but blocks until the figure window is closed."""
    if os.environ.get("FSETOOLS_SHOW_PLOTS") == "1":
        import matplotlib.pyplot as _plt

        if fig is not None:
            _plt.show(block=True)
        else:
            _plt.show(block=True)
