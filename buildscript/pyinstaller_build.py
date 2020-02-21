# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from os.path import join, realpath, dirname

import fsetools

try:
    from buildscript.__key__ import key as key_
    key = key_()
except ValueError:
    key = None


def build_gui(app_name: str = 'FSETOOLS', fp_target_py: str = 'pyinstaller_build_entry.py', options: list = None):
    print('\n' * 2)

    os.chdir(dirname(realpath(__file__)))

    cmd_option_list = [
        f'-n={app_name}',
        "--icon=" + realpath(join("etc", "ofr_logo_1_80_80.ico")),
    ]
    if 'dev' in fsetools.__version__:
        print('Dev. build is enabled.')
    else:
        cmd_option_list.append('--windowed')
        print('Dev. build is not enabled.')

    if options:
        cmd_option_list.extend(options)

    # add encryption to pyz
    if key:
        cmd_option_list.append(f'--key={key}')
        print('Encryption is enabled.')
    else:
        print('Encryption is not enabled.')

    cmd = ['pyinstaller'] + cmd_option_list + [fp_target_py]
    print('COMMAND:', ' '.join(cmd))

    with open('pyinstaller_build.log', 'wb') as f:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for c in iter(lambda: process.stdout.read(1), b''):  # replace '' with b'' for Python 3
            sys.stdout.write(c.decode('utf-8'))
            f.write(c)


def main():
    build_gui(
        options=[
            "--onedir",  # output unpacked dist to one directory, including an .exe file
            "--noconfirm",  # replace output directory without asking for confirmation
            "--clean",  # clean pyinstaller cache and remove temporary files
            f'--add-data={realpath(join("etc", "ofr_logo_1_80_80.ico"))}{os.pathsep}etc',
        ]
    )
    # build_gui(
    #     options=[
    #         "--onefile",  # output one .exe file
    #         "--noconfirm",  # replace output directory without asking for confirmation
    #     ]
    # )


if __name__ == "__main__":
    main()
