import os
from os import path

import numpy as np

from fsetools.etc.safir import Thermal2DPPXML


def post_process_VCC1(fp: str, fn_prefix: str='VCC1'):
    fps_xml = list()
    for root, dirs, files in os.walk(fp):
        if fn_prefix in os.path.basename(root):
            for file in files:
                if file.endswith(".xml") or file.endswith(".XML"):
                    fps_xml.append(os.path.join(root, file))
                    print(fps_xml[-1])

    case_p = Thermal2DPPXML()

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


def post_process_VCC2(fp: str, fn_prefix: str='VCC2'):
    fps_xml = list()
    for root, dirs, files in os.walk(fp):
        if fn_prefix in os.path.basename(root):
            for file in files:
                if file.endswith(".xml") or file.endswith(".XML"):
                    fps_xml.append(os.path.join(root, file))
                    print(fps_xml[-1])

    case_p = Thermal2DPPXML()
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


def post_process_VCC3(fp: str, fn_prefix: str='VCC3'):
    fps_xml = list()
    for root, dirs, files in os.walk(fp):
        if fn_prefix in os.path.basename(root):
            for file in files:
                if file.endswith(".xml") or file.endswith(".XML"):
                    fps_xml.append(os.path.join(root, file))
                    print(fps_xml[-1])

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

    case_p = Thermal2DPPXML()
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


def post_process_TypicalF45W25(fp: str, fn_prefix: str = 'TypicalF45W25'):
    fps_xml = list()
    for root, dirs, files in os.walk(fp):
        if fn_prefix in os.path.basename(root):
            for file in files:
                if file.endswith(".xml") or file.endswith(".XML"):
                    fps_xml.append(os.path.join(root, file))
                    print(fps_xml[-1])

    xys = [
        (0.75833, 0.03),
        (0.425, 0.0225),
        (0.075, 0.0225),
        (0.15833, 0.65167),
        (0.05, 0.985),
        (0.33333, 0.985),
        (0.75833, 0.985),
        (0.70833, 0.65167),
    ]

    ws = np.array((
        0.00788,
        0.02475,
        0.00675,
        0.02275,
        0.00675,
        0.02475,
        0.00788,
        0.02275,
    ))

    case_p = Thermal2DPPXML()
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


def post_process_TypicalF45W45(fp: str, fn_prefix: str = 'TypicalF45W45'):
    fps_xml = list()
    for root, dirs, files in os.walk(fp):
        if fn_prefix in os.path.basename(root):
            for file in files:
                if file.endswith(".xml") or file.endswith(".XML"):
                    fps_xml.append(os.path.join(root, file))
                    print(fps_xml[-1])

    xys = [
        (0.745, 0.03),
        (0.415, 0.0225),
        (0.075, 0.0225),
        (0.165, 0.65167),
        (0.745, 0.985),
        (0.32667, 0.985),
        (0.05, 0.985),
        (0.695, 0.65167),
    ]

    ws = np.array((
        0.00878,
        0.02385,
        0.00675,
        0.04095,
        0.00877,
        0.02385,
        0.00675,
        0.04095,
    ))

    case_p = Thermal2DPPXML()
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


if __name__ == '__main__':
    post_process_VCC1(
        fp=r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel_corner_columns_GF')
    post_process_VCC2(
        fp=r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel_corner_columns_GF')
    post_process_VCC3(
        fp=r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel_corner_columns_GF')
    post_process_TypicalF45W25(
        fp=r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel_typical_columns_GF')
    post_process_TypicalF45W45(
        fp=r'D:\projects_fse\fleet_st\03 Therm2D\01_analysis\trial_01\safir\vierendeel_typical_columns_GF')
