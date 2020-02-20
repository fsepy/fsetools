"""fseutil CLI Help.
Usage:
    fseutil

Commands:
    fseutil
        `fseutil` graphical user interface.
"""


import os

from docopt import docopt

import fseutil
from fseutil.gui.__main__ import main as main_gui


def helper_get_list_filepath_end_width(cwd: str, end_with: str) -> list:
    filepath_all = list()
    for (dirpath, dirnames, filenames) in os.walk(cwd):
        filepath_all.extend(filenames)
        break  # terminate at level 1, do not go to sub folders.

    filepath_end_with = list()
    for i in filepath_all:
        if i.endswith(end_with):
            filepath_end_with.append(os.path.join(cwd, i))

    return filepath_end_with


def gui():
    print(fseutil.__version__)
    main_gui()


def main():
    arguments = docopt(__doc__)
    if len(arguments) == 0:
        gui()
