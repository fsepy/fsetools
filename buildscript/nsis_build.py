import os
import subprocess
import sys
from os.path import join, realpath, dirname

from buildscript.pyinstaller_build import main as main_pyinstaller
from fsetools.gui.layout.ui2py import ui2py


def find_all_dist_files(dir_build: str, include_root_name: bool = True):
    list_fp = list()

    for root, dirs, files in os.walk(dir_build):
        for file in files:
            if include_root_name:
                list_fp.append(join(root, file))
            else:
                list_fp.append(join(root, file).replace(dir_build, ''))

    return list_fp


def make_nsh_files():
    fp_list = find_all_dist_files(join(dirname(realpath(__file__)), 'dist', 'FSETOOLS'), False)
    for i in fp_list:
        print(i)

    with open('nsis_build_inst_list.nsh', 'w+') as f:
        f.writelines([f'file {join("dist", "FSETOOLS")}{i}\n' for i in fp_list])

    with open('nsis_build_uninst_list.nsh', 'w+') as f:
        f.writelines([f'delete $INSTDIR{i}\n' for i in fp_list])


def main():

    cmd = ['makensis', 'nsis_build.nsi']

    with open('nsis_build.log', 'wb') as f:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for c in iter(lambda: process.stdout.read(1), b''):  # replace '' with b'' for Python 3
            sys.stdout.write(c.decode('utf-8'))
            f.write(c)


if __name__ == '__main__':
    ui2py()
    main_pyinstaller()
    make_nsh_files()
    main()
