# fseutil

Fire Safety Engineering Tools. Note this project is currently WIP and use with caution.

## Getting Started

Documentation is under construction.

### Installation

[Python](https://www.python.org/downloads/) 3.7 or later is required. [Anaconda Distribution](https://www.anaconda.com/distribution/#download-section) is recommended for new starters, it includes Python and few useful packages including a package management tool pip (see below).

[pip](https://pypi.org/) is a package management system for installing and updating Python packages. pip comes with Python, so you get pip simply by installing Python. On Ubuntu and Fedora Linux, you can simply use your system package manager to install the `python3-pip` package. [The Hitchhiker's Guide to Python](https://docs.python-guide.org/starting/installation/) provides some guidance on how to install Python on your system if it isn't already; you can also install Python directly from [python.org](https://www.python.org/getit/). You might want to [upgrade pip](https://pip.pypa.io/en/stable/installing/) before using it to install other programs.

1. to use `pip` install from PyPI:

    ```sh
    pip install --upgrade fseutil
    ```

2. to use `pip` install from GitHub (requires [git](https://git-scm.com/downloads)):  

    *Note installing `fseutil` via this route will include the latest commits/changes to the library.*  

    ```sh
    pip install --upgrade "git+https://github.com/fsepy/fseutil.git@dev"
    ```


### Command line interface

Once `fseutil` is installed, CLI help can be summoned:

```shell
(base) C:\Users\IanFu>fseutil -h
```

## Authors

**Ian Fu** - *fuyans@gmail.com*
