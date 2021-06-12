import os
from os import path

import numpy as np

from fsetools.etc.safir import Thermal2DPPXML, Thermal2DRun


def beam_xys_weights():
    xys = [
        (0.804298, 0.985371), (0.6125, 0.98), (0.4375, 0.975), (0.2625, 0.97), (0.0746045, 0.964968), (0.1625, 0.8),
        (0.1625, 0.49), (0.1625, 0.18), (0.075, 0.0125),
        (0.2625, 0.0125), (0.4375, 0.0125), (0.6125, 0.0125), (0.8, 0.0125), (0.7125, 0.182619048),
        (0.7125, 0.497857143), (0.7125, 0.813095238)
    ]
    ws = np.array([
        0.004376785, 0.004376786, 0.004376786, 0.004376786, 0.004376785, 0.00775, 0.00775, 0.00775, 0.004375, 0.004375,
        0.004375, 0.004375, 0.004375, 0.00788095, 0.00788095,
        0.00788095,
    ])
    return xys, ws


def column_xys_weights():
    xys = [
        (0.64000, 0.83750),
        (0.52833, 0.79000),
        (0.32500, 0.79000),
        (0.12167, 0.79000),
        (0.01000, 0.83750),
        (0.01000, 0.66583),
        (0.01000, 0.43750),
        (0.01000, 0.20917),
        (0.01000, 0.03750),
        (0.12167, 0.08500),
        (0.32500, 0.08500),
        (0.52833, 0.08500),
        (0.64000, 0.03750),
        (0.64000, 0.20917),
        (0.64000, 0.43750),
        (0.64000, 0.66583),
    ]

    ws = np.array((
        0.00190,
        0.00407,
        0.00407,
        0.00407,
        0.00190,
        0.00457,
        0.00457,
        0.00457,
        0.00190,
        0.00407,
        0.00407,
        0.00407,
        0.00190,
        0.00457,
        0.00457,
        0.00457,
    ))
    return xys, ws


def VCC1_xys_weights():
    xys = [
        (-0.03597, 0.08293),
        (-0.25875, 0.3689),
        (-0.47385, 0.645),
        (-0.09002, 0.8331),
        (0.57953, 0.8331),
        (0.96325, 0.645),
        (0.74825, 0.3689),
        (0.52555, 0.08295),
        (0.40498, 0.27195),
        (0.08463, 0.27195),
        (0.2448, 0.72775),
    ]

    ws = np.array((
        0.00789219,
        0.02476605,
        0.00675359,
        0.01982131,
        0.01972401,
        0.00675359,
        0.02476051,
        0.00787952,
        0.009430065,
        0.009430065,
        0.0299475,
    ))
    return xys, ws


def VCC2_xys_weights():
    xys = [
        (-0.0295, 0.0586),
        (-0.3505, 0.2831),
        (-0.6334, 0.48915),
        (-0.3484, 0.7248),
        (0.29623, 1.0054),
        (0.7699, 0.46827),
        (0.58123, 0.3309),
        (0.2376, 0.0807),
        (0.08725, 0.36545),
        (-0.02008, 0.24875),
        (0.0686, 0.68287),
    ]

    ws = np.array((
        0.00788,
        0.02476,
        0.00676,
        0.02561,
        0.02568,
        0.00676,
        0.02477,
        0.00788,
        0.00732,
        0.00727,
        0.04201,
    ))
    return xys, ws


def VCC3_xys_weights():
    xys = [
        (-0.01803, 0.0631),
        (-0.29135, 0.34375),
        (-0.5307, 0.5991),
        (-0.0691, 0.90613),
        (0.1493, 1.15043),
        (0.54733, 0.72377),
        (0.80347, 0.57503),
        (0.51853, 0.27103),
        (0.268, 0.0147),
        (0.2579, 0.24695),
        (-0.00497, 0.21247),
        (0.1493, 0.60303),

    ]

    ws = np.array((
        0.00788,
        0.02475,
        0.00675,
        0.01963,
        0.01068,
        0.01966,
        0.00675,
        0.02475,
        0.00788,
        0.00718,
        0.00716,
        0.03392,
    ))
    return xys, ws


def equivalency_run(fp_input_file, T_target, xys, ws, **kwargs):
    case_run = Thermal2DRun()
    case_run.fp_input_file = fp_input_file
    case_run.run_solve_k(xys=xys, ws=ws, T_target=T_target, **kwargs)


def deterministic_run(fp_input_file, xys, ws, run: bool = True):
    case = Thermal2DRun()
    case_p = Thermal2DPPXML()

    case.fp_input_file = fp_input_file
    if run:
        case.run()
    case_p.xml = case.xml
    case_p.get_xys_temp_ave(
        xys=xys, ws=ws, mode='k_y_theta',
        fp_save_plot=path.splitext(case.fp_input_file)[0] + '.png',
        fp_save_num=path.splitext(case.fp_input_file)[0] + '.temp.csv',
        show_legend=False,
    )


def beam_equivalency():
    fps = [
        r'C:\Users\IanFu\Desktop\fleet st\beams\equivalency\beam_1\beam_1.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\equivalency\beam_2\beam_2.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\equivalency\beam_3\beam_3.in',
    ]
    for fp in fps:
        try:
            assert path.exists(fp)
        except AssertionError:
            print(fp)
    xys, ws = beam_xys_weights()

    teq_bc_old2new = list()
    for i in (1, 2, 3):
        for j in (1, 2, 3, 4):
            teq_bc_old2new.append((f'c{i:d}{j:d}.txt', 'FISO'))

    for fp in fps:
        print('Starting ', fp)
        equivalency_run(fp, 620., xys, ws, teq_solve=True, teq_bc_old2new=teq_bc_old2new)


def beam_deterministic():
    fps = [
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam1\beam1.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam2\beam2.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam3\beam3.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam_concrete1\beam_concrete1.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam_concrete2\beam_concrete2.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam_concrete3\beam_concrete3.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam_concrete_plate1\beam_concrete_plate1.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam_concrete_plate2\beam_concrete_plate2.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam_concrete_plate3\beam_concrete_plate3.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam_plate_1\beam_plate_1.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam_plate_2\beam_plate_2.in',
        r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic\beam_plate_3\beam_plate_3.in',
    ]
    for fp in fps:
        try:
            assert path.exists(fp)
        except AssertionError:
            print(fp)
    xys, ws = beam_xys_weights()
    for fp in fps:
        print(fp)
        deterministic_run(fp, xys, ws, run=True)


def column_deterministic():
    fps = [
        r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic\column_1\column_1.in',
        r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic\column_2\column_2.in',
        r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic\column_3\column_3.in',
        r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic\column_concrete_1\column_concrete_1.in',
        r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic\column_concrete_2\column_concrete_2.in',
        r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic\column_concrete_3\column_concrete_3.in',
        r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic\column_concrete_plate_1\column_concrete_plate_1.in',
        r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic\column_concrete_plate_2\column_concrete_plate_2.in',
        r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic\column_concrete_plate_3\column_concrete_plate_3.in',
    ]
    for fp in fps:
        try:
            assert path.exists(fp)
        except AssertionError:
            print(fp)
    xys, ws = column_xys_weights()
    for fp in fps:
        print(fp)
        deterministic_run(fp, xys, ws, run=True)


def vierendeel_corner_column_deterministic():
    fps = list()
    for root, dirs, files in os.walk(r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel'):
        if os.path.basename(root).endswith('.gid'):
            continue
        for file in files:
            if file.endswith(".in") or file.endswith(".IN"):
                fps.append(os.path.join(root, file))
                print(fps[-1])

    for fp in fps:
        try:
            assert path.exists(fp)
        except AssertionError:
            print(fp)
    xys, ws = beam_xys_weights()
    for fp in fps:
        print(fp)
        deterministic_run(fp, xys, ws, run=True)


def column_equivalency():
    fps = [
        r'C:\Users\IanFu\Desktop\fleet st\columns\equivalency\column_1\column_1.in',
        # r'C:\Users\IanFu\Desktop\fleet st\columns\equivalency\column_2\column_2.in',
        # r'C:\Users\IanFu\Desktop\fleet st\columns\equivalency\column_3\column_3.in',
        # r'C:\Users\IanFu\Desktop\fleet st\columns\equivalency\column_concrete_1\column_concrete_1.in',
        # r'C:\Users\IanFu\Desktop\fleet st\columns\equivalency\column_concrete_2\column_concrete_2.in',
        # r'C:\Users\IanFu\Desktop\fleet st\columns\equivalency\column_concrete_3\column_concrete_3.in',
    ]

    for fp in fps:
        try:
            assert path.exists(fp)
        except AssertionError:
            print(fp)

    xys, ws = column_xys_weights()

    teq_bc_old2new = list()
    for i in (1, 2, 3):
        for j in (1, 2, 3, 4):
            teq_bc_old2new.append((f'c{i:d}{j:d}.txt', 'FISO'))

    for fp in fps:
        print('Starting ', fp)
        equivalency_run(fp, 550., xys, ws, teq_solve=True, teq_bc_old2new=teq_bc_old2new)


def post_process_all_beams():
    fps_xml = list()
    for root, dirs, files in os.walk(r'C:\Users\IanFu\Desktop\fleet st\beams'):
        for file in files:
            if file.endswith(".xml") or file.endswith(".XML"):
                fps_xml.append(os.path.join(root, file))
                print(fps_xml[-1])

    case_p = Thermal2DPPXML()
    xys, ws = beam_xys_weights()
    for fp in fps_xml:
        print(fp)
        with open(fp, 'r') as f:
            case_p.xml = f.read()
        try:
            case_p.get_xys_temp_ave(
                xys=xys, ws=ws, mode='k_y_theta',
                fp_save_plot=path.splitext(fp)[0] + '.png',
                fp_save_num=path.splitext(fp)[0] + '.temp.csv',
                figsize=(2.8, 2.8)
            )
        except Exception as e:
            print(f'Failed, {e}')


def post_process_all_columns():
    fps_xml = list()
    for root, dirs, files in os.walk(r'C:\Users\IanFu\Desktop\fleet st\columns'):
        for file in files:
            if file.endswith(".xml") or file.endswith(".XML"):
                fps_xml.append(os.path.join(root, file))
                print(fps_xml[-1])

    case_p = Thermal2DPPXML()
    xys, ws = column_xys_weights()
    for fp in fps_xml:
        print(fp)
        with open(fp, 'r') as f:
            case_p.xml = f.read()
        try:
            case_p.get_xys_temp_ave(
                xys=xys, ws=ws, mode='k_y_theta',
                fp_save_plot=path.splitext(fp)[0] + '.png',
                fp_save_num=path.splitext(fp)[0] + '.temp.csv',
                figsize=(2.8, 2.8)
            )
        except Exception as e:
            print(f'Failed, {e}')


def post_process_VCC1():
    fps_xml = list()
    for root, dirs, files in os.walk(
            r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel_corner_columns'):
        if 'VCC1' not in os.path.basename(root):
            continue
        for file in files:
            if file.endswith(".xml") or file.endswith(".XML"):
                fps_xml.append(os.path.join(root, file))
                print(fps_xml[-1])

    case_p = Thermal2DPPXML()
    xys, ws = VCC1_xys_weights()
    for fp in fps_xml:
        print(fp)
        with open(fp, 'r') as f:
            case_p.xml = f.read()
        try:
            case_p.get_xys_temp_ave(
                xys=xys, ws=ws, mode='k_y_theta',
                fp_save_plot=path.splitext(fp)[0] + '.png',
                fp_save_num=path.splitext(fp)[0] + '.temp.csv',
                figsize=(2.8, 2.8)
            )
        except Exception as e:
            print(f'Failed, {e}')


def post_process_VCC2():
    fps_xml = list()
    for root, dirs, files in os.walk(
            r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel_corner_columns'):
        if 'VCC2' not in os.path.basename(root):
            continue
        for file in files:
            if file.endswith(".xml") or file.endswith(".XML"):
                fps_xml.append(os.path.join(root, file))
                print(fps_xml[-1])

    case_p = Thermal2DPPXML()
    xys, ws = VCC1_xys_weights()
    for fp in fps_xml:
        print(fp)
        with open(fp, 'r') as f:
            case_p.xml = f.read()
        try:
            case_p.get_xys_temp_ave(
                xys=xys, ws=ws, mode='k_y_theta',
                fp_save_plot=path.splitext(fp)[0] + '.png',
                fp_save_num=path.splitext(fp)[0] + '.temp.csv',
                figsize=(2.8, 2.8)
            )
        except Exception as e:
            print(f'Failed, {e}')


def move_files(origin: str, target: str, endswith: str):
    assert path.exists(origin)
    assert path.exists(target)

    fps_csv = list()

    for root, dirs, files in os.walk(origin):
        for file in files:
            if file.endswith(endswith.lower()) or file.endswith(endswith.upper()):
                fps_csv.append(os.path.join(root, file))
                print(fps_csv[-1])

    for fp in fps_csv:
        dst = path.join(path.realpath(target), path.basename(fp))
        print(f'Moving {fp}')
        if fp != dst:
            try:
                os.remove(dst)
            except:
                pass
            os.rename(fp, dst)


if __name__ == '__main__':
    # beam_deterministic()
    # column_deterministic()
    # vierendeel_corner_column_deterministic()
    #
    # beam_equivalency()
    # column_equivalency()
    #
    # post_process_all_beams()
    # post_process_all_columns()
    post_process_VCC1()
    post_process_VCC2()

    # move_files(r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic', r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic', '.temp.csv')
    # move_files(r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic', r'C:\Users\IanFu\Desktop\fleet st\columns\deterministic', '.png')
    # move_files(r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic', r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic', '.temp.csv')
    # move_files(r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic', r'C:\Users\IanFu\Desktop\fleet st\beams\deterministic', '.png')
    # move_files(r'C:\Users\IanFu\Desktop\fleet st\columns\equivalency', r'C:\Users\IanFu\Desktop\fleet st\columns\equivalency', '.temp.csv')
    # move_files(r'C:\Users\IanFu\Desktop\fleet st\columns\equivalency', r'C:\Users\IanFu\Desktop\fleet st\columns\equivalency', '.png')
    # move_files(r'C:\Users\IanFu\Desktop\fleet st\beams\equivalency', r'C:\Users\IanFu\Desktop\fleet st\beams\equivalency', '.temp.csv')
    # move_files(r'C:\Users\IanFu\Desktop\fleet st\beams\equivalency', r'C:\Users\IanFu\Desktop\fleet st\beams\equivalency', '.png')

    # move_files(r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel_corner_columns', r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel_corner_columns', '.temp.csv')
    # move_files(r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel_corner_columns', r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel_corner_columns', '.png')

    pass
