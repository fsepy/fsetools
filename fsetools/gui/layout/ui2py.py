def ui2py():
    import os
    import subprocess

    list_ui_file_names = [
        'main.ui',
        'dialog_0103_merging_flow.ui',
        'dialog_0111_heat_detector_activation.ui',
        'dialog_0401_br187_parallel_simple.ui',
        'dialog_0403_br187_parallel_complex.ui',
        'dialog_0405_thermal_radiation_extreme.ui',
        'dialog_0601_naming_convention.ui',
        'dialog_0602_pd_7974_flame_height.ui',
    ]

    cwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui')
    destination_dir = os.path.dirname(os.path.realpath(__file__))

    cmds_list = list()
    for ui_file_name in list_ui_file_names:
        cmd = [
            'pyside2-uic',
            '--output', f'{os.path.join(destination_dir, ui_file_name.replace(".ui", ".py"))}',
            f'{os.path.join(cwd, ui_file_name)}'
        ]
        cmds_list.append(cmd)
    procs_list = [subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for cmd in cmds_list]
    for proc in procs_list:
        proc.wait()


if __name__ == '__main__':
    ui2py()
