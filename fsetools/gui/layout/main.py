# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'make_nsh_files.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(461, 507)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.action_0101_ADB_Vol_2_Datasheet = QAction(MainWindow)
        self.action_0101_ADB_Vol_2_Datasheet.setObjectName(u"action_0101_ADB_Vol_2_Datasheet")
        self.action_0102_BS_9999_Datasheet = QAction(MainWindow)
        self.action_0102_BS_9999_Datasheet.setObjectName(u"action_0102_BS_9999_Datasheet")
        self.action_0103_BS_9999_Merging_flow = QAction(MainWindow)
        self.action_0103_BS_9999_Merging_flow.setObjectName(u"action_0103_BS_9999_Merging_flow")
        self.action_0104_PD_7974_HD_activation = QAction(MainWindow)
        self.action_0104_PD_7974_HD_activation.setObjectName(u"action_0104_PD_7974_HD_activation")
        self.action_0401_BR_187_parallel_simple = QAction(MainWindow)
        self.action_0401_BR_187_parallel_simple.setObjectName(u"action_0401_BR_187_parallel_simple")
        self.action_0402_BR_187_perpendicular_simple = QAction(MainWindow)
        self.action_0402_BR_187_perpendicular_simple.setObjectName(u"action_0402_BR_187_perpendicular_simple")
        self.action_0403_BR_187_parallel_complex = QAction(MainWindow)
        self.action_0403_BR_187_parallel_complex.setObjectName(u"action_0403_BR_187_parallel_complex")
        self.action_0404_BR_187_perpendicular_complex = QAction(MainWindow)
        self.action_0404_BR_187_perpendicular_complex.setObjectName(u"action_0404_BR_187_perpendicular_complex")
        self.action_0601_OFR_naming_protocol = QAction(MainWindow)
        self.action_0601_OFR_naming_protocol.setObjectName(u"action_0601_OFR_naming_protocol")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(15, 110, 381, 106))
        self.pushButton_0102_bs9999_datasheet_1 = QPushButton(self.groupBox_3)
        self.pushButton_0102_bs9999_datasheet_1.setObjectName(u"pushButton_0102_bs9999_datasheet_1")
        self.pushButton_0102_bs9999_datasheet_1.setGeometry(QRect(85, 20, 70, 70))
        self.pushButton_0103_merging_flow = QPushButton(self.groupBox_3)
        self.pushButton_0103_merging_flow.setObjectName(u"pushButton_0103_merging_flow")
        self.pushButton_0103_merging_flow.setEnabled(True)
        self.pushButton_0103_merging_flow.setGeometry(QRect(155, 20, 70, 70))
        self.pushButton_0111_heat_detector_activation = QPushButton(self.groupBox_3)
        self.pushButton_0111_heat_detector_activation.setObjectName(u"pushButton_0111_heat_detector_activation")
        self.pushButton_0111_heat_detector_activation.setGeometry(QRect(225, 20, 70, 70))
        self.b4_01_br187_parallel_10 = QPushButton(self.groupBox_3)
        self.b4_01_br187_parallel_10.setObjectName(u"b4_01_br187_parallel_10")
        self.b4_01_br187_parallel_10.setEnabled(False)
        self.b4_01_br187_parallel_10.setGeometry(QRect(295, 20, 70, 70))
        self.pushButton_0101_adb2_datasheet_1 = QPushButton(self.groupBox_3)
        self.pushButton_0101_adb2_datasheet_1.setObjectName(u"pushButton_0101_adb2_datasheet_1")
        self.pushButton_0101_adb2_datasheet_1.setGeometry(QRect(15, 20, 70, 70))
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(15, 340, 311, 106))
        self.pushButton_0601_naming_convention = QPushButton(self.groupBox_2)
        self.pushButton_0601_naming_convention.setObjectName(u"pushButton_0601_naming_convention")
        self.pushButton_0601_naming_convention.setGeometry(QRect(15, 20, 70, 70))
        self.b4_01_br187_parallel_11 = QPushButton(self.groupBox_2)
        self.b4_01_br187_parallel_11.setObjectName(u"b4_01_br187_parallel_11")
        self.b4_01_br187_parallel_11.setEnabled(False)
        self.b4_01_br187_parallel_11.setGeometry(QRect(85, 20, 70, 70))
        self.b4_01_br187_parallel_12 = QPushButton(self.groupBox_2)
        self.b4_01_br187_parallel_12.setObjectName(u"b4_01_br187_parallel_12")
        self.b4_01_br187_parallel_12.setEnabled(False)
        self.b4_01_br187_parallel_12.setGeometry(QRect(155, 20, 70, 70))
        self.pushButton_0602_pd7974_flame_height = QPushButton(self.groupBox_2)
        self.pushButton_0602_pd7974_flame_height.setObjectName(u"pushButton_0602_pd7974_flame_height")
        self.pushButton_0602_pd7974_flame_height.setGeometry(QRect(225, 20, 70, 70))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(15, 225, 381, 106))
        self.pushButton_0401_br187_parallel_simple = QPushButton(self.groupBox)
        self.pushButton_0401_br187_parallel_simple.setObjectName(u"pushButton_0401_br187_parallel_simple")
        self.pushButton_0401_br187_parallel_simple.setGeometry(QRect(15, 20, 70, 70))
        self.pushButton_0402_br187_perpendicular_simple = QPushButton(self.groupBox)
        self.pushButton_0402_br187_perpendicular_simple.setObjectName(u"pushButton_0402_br187_perpendicular_simple")
        self.pushButton_0402_br187_perpendicular_simple.setGeometry(QRect(85, 20, 70, 70))
        self.pushButton_0403_br187_parallel_complex = QPushButton(self.groupBox)
        self.pushButton_0403_br187_parallel_complex.setObjectName(u"pushButton_0403_br187_parallel_complex")
        self.pushButton_0403_br187_parallel_complex.setGeometry(QRect(155, 20, 70, 70))
        self.pushButton_0404_br187_perpendicular_complex = QPushButton(self.groupBox)
        self.pushButton_0404_br187_perpendicular_complex.setObjectName(u"pushButton_0404_br187_perpendicular_complex")
        self.pushButton_0404_br187_perpendicular_complex.setGeometry(QRect(225, 20, 70, 70))
        self.pushButton_0405_thermal_radiation_extreme = QPushButton(self.groupBox)
        self.pushButton_0405_thermal_radiation_extreme.setObjectName(u"pushButton_0405_thermal_radiation_extreme")
        self.pushButton_0405_thermal_radiation_extreme.setEnabled(True)
        self.pushButton_0405_thermal_radiation_extreme.setGeometry(QRect(295, 20, 70, 70))
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(15, 15, 431, 84))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_big_name = QLabel(self.horizontalLayoutWidget)
        self.label_big_name.setObjectName(u"label_big_name")
        self.label_big_name.setMinimumSize(QSize(0, 26))
        font = QFont()
        font.setPointSize(18)
        self.label_big_name.setFont(font)
        self.label_big_name.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_big_name)

        self.label_copy_right = QLabel(self.horizontalLayoutWidget)
        self.label_copy_right.setObjectName(u"label_copy_right")
        self.label_copy_right.setMinimumSize(QSize(0, 28))
        self.label_copy_right.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_copy_right)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_logo = QLabel(self.horizontalLayoutWidget)
        self.label_logo.setObjectName(u"label_logo")
        self.label_logo.setMinimumSize(QSize(194, 80))
        self.label_logo.setPixmap(QPixmap(u"../images/OFR_LOGO_2_194_80.png"))

        self.horizontalLayout.addWidget(self.label_logo)

        self.label_version = QLabel(self.centralwidget)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setGeometry(QRect(15, 450, 157, 14))
        self.label_version.setMinimumSize(QSize(0, 14))
        font1 = QFont()
        font1.setPointSize(6)
        self.label_version.setFont(font1)
        self.label_version.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 461, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.pushButton_0101_adb2_datasheet_1, self.pushButton_0102_bs9999_datasheet_1)
        QWidget.setTabOrder(self.pushButton_0102_bs9999_datasheet_1, self.pushButton_0103_merging_flow)
        QWidget.setTabOrder(self.pushButton_0103_merging_flow, self.pushButton_0111_heat_detector_activation)
        QWidget.setTabOrder(self.pushButton_0111_heat_detector_activation, self.b4_01_br187_parallel_10)
        QWidget.setTabOrder(self.b4_01_br187_parallel_10, self.pushButton_0401_br187_parallel_simple)
        QWidget.setTabOrder(self.pushButton_0401_br187_parallel_simple, self.pushButton_0402_br187_perpendicular_simple)
        QWidget.setTabOrder(self.pushButton_0402_br187_perpendicular_simple, self.pushButton_0403_br187_parallel_complex)
        QWidget.setTabOrder(self.pushButton_0403_br187_parallel_complex, self.pushButton_0404_br187_perpendicular_complex)
        QWidget.setTabOrder(self.pushButton_0404_br187_perpendicular_complex, self.pushButton_0601_naming_convention)
        QWidget.setTabOrder(self.pushButton_0601_naming_convention, self.b4_01_br187_parallel_11)
        QWidget.setTabOrder(self.b4_01_br187_parallel_11, self.b4_01_br187_parallel_12)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("")
        self.action_0101_ADB_Vol_2_Datasheet.setText(QCoreApplication.translate("MainWindow", u"ADB Vol. 2 Datasheet No. 1", None))
        self.action_0102_BS_9999_Datasheet.setText(QCoreApplication.translate("MainWindow", u"BS 9999 Datasheet No. 1", None))
        self.action_0103_BS_9999_Merging_flow.setText(QCoreApplication.translate("MainWindow", u"BS 9999 Merging flow calculation", None))
        self.action_0104_PD_7974_HD_activation.setText(QCoreApplication.translate("MainWindow", u"PD 7974 HD activation time calculation", None))
        self.action_0401_BR_187_parallel_simple.setText(QCoreApplication.translate("MainWindow", u"BR 187 parallel plane calculation", None))
        self.action_0402_BR_187_perpendicular_simple.setText(QCoreApplication.translate("MainWindow", u"BR 187 perpendicular plane calculation", None))
        self.action_0403_BR_187_parallel_complex.setText(QCoreApplication.translate("MainWindow", u"BR 187 parallel plane calculation (complex)", None))
        self.action_0404_BR_187_perpendicular_complex.setText(QCoreApplication.translate("MainWindow", u"BR 187 perpendicular plain calculation (complex)", None))
        self.action_0601_OFR_naming_protocol.setText(QCoreApplication.translate("MainWindow", u"OFR file naming protocol", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"B1 Means of escape", None))
#if QT_CONFIG(tooltip)
        self.pushButton_0102_bs9999_datasheet_1.setToolTip(QCoreApplication.translate("MainWindow", u"Data sheet 1 for BS 9999:2017, for B1.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_0102_bs9999_datasheet_1.setStatusTip(QCoreApplication.translate("MainWindow", u"Data sheet 1 for BS 9999:2017, for B1.", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_0102_bs9999_datasheet_1.setText(QCoreApplication.translate("MainWindow", u"BS 9999\n"
"Datasheet\n"
"No. 1", None))
#if QT_CONFIG(tooltip)
        self.pushButton_0103_merging_flow.setToolTip(QCoreApplication.translate("MainWindow", u"Merging flow calculation in accordance with BS 9999:2017.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_0103_merging_flow.setStatusTip(QCoreApplication.translate("MainWindow", u"Merging flow calculation in accordance with BS 9999:2017.", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_0103_merging_flow.setText(QCoreApplication.translate("MainWindow", u"Merging\n"
"Flow", None))
#if QT_CONFIG(tooltip)
        self.pushButton_0111_heat_detector_activation.setToolTip(QCoreApplication.translate("MainWindow", u"Heat detector activation time (ceiling jet) in accordance with PD 7974-1:2019.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_0111_heat_detector_activation.setStatusTip(QCoreApplication.translate("MainWindow", u"Heat detector activation time (ceiling jet) in accordance with PD 7974-1:2019.", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_0111_heat_detector_activation.setText(QCoreApplication.translate("MainWindow", u"PD 7974\n"
"HD\n"
"Activation\n"
"Time", None))
#if QT_CONFIG(tooltip)
        self.b4_01_br187_parallel_10.setToolTip(QCoreApplication.translate("MainWindow", u"Not implemented.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.b4_01_br187_parallel_10.setStatusTip(QCoreApplication.translate("MainWindow", u"Not implemented.", None))
#endif // QT_CONFIG(statustip)
        self.b4_01_br187_parallel_10.setText(QCoreApplication.translate("MainWindow", u"Zone\n"
"Model", None))
#if QT_CONFIG(tooltip)
        self.pushButton_0101_adb2_datasheet_1.setToolTip(QCoreApplication.translate("MainWindow", u"Data sheet 1 for Approved Document B (2019) Vol. 2, for B1.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_0101_adb2_datasheet_1.setStatusTip(QCoreApplication.translate("MainWindow", u"Data sheet 1 for Approved Document B (2019) Vol. 2, for B1.", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_0101_adb2_datasheet_1.setText(QCoreApplication.translate("MainWindow", u"ADB 2\n"
"Datasheet\n"
"No. 1", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Miscellaneous", None))
#if QT_CONFIG(tooltip)
        self.pushButton_0601_naming_convention.setToolTip(QCoreApplication.translate("MainWindow", u"File name generator in accordance with OFR file naming protocal.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_0601_naming_convention.setStatusTip(QCoreApplication.translate("MainWindow", u"File name generator in accordance with OFR file naming protocal.", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_0601_naming_convention.setText(QCoreApplication.translate("MainWindow", u"File\n"
"Naming\n"
"Protocol", None))
        self.b4_01_br187_parallel_11.setText(QCoreApplication.translate("MainWindow", u"CFD\n"
"Required\n"
"Vent. Size", None))
#if QT_CONFIG(tooltip)
        self.b4_01_br187_parallel_12.setToolTip(QCoreApplication.translate("MainWindow", u"To estimate optimal mesh resolution.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.b4_01_br187_parallel_12.setStatusTip(QCoreApplication.translate("MainWindow", u"To estimate optimal mesh resolution.", None))
#endif // QT_CONFIG(statustip)
        self.b4_01_br187_parallel_12.setText(QCoreApplication.translate("MainWindow", u"CFD\n"
"Mesh Size", None))
#if QT_CONFIG(tooltip)
        self.pushButton_0602_pd7974_flame_height.setToolTip(QCoreApplication.translate("MainWindow", u"Flame height in accordance with PD 7974-1:2019.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_0602_pd7974_flame_height.setStatusTip(QCoreApplication.translate("MainWindow", u"Flame height in accordance with PD 7974-1:2019.", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_0602_pd7974_flame_height.setText(QCoreApplication.translate("MainWindow", u"PD 7974\n"
"Flame\n"
"Height", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"B4 External flame spread", None))
#if QT_CONFIG(tooltip)
        self.pushButton_0401_br187_parallel_simple.setToolTip(QCoreApplication.translate("MainWindow", u"Thermal radiation calculation following BR 187 (Parallel rectangular orientation).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_0401_br187_parallel_simple.setStatusTip(QCoreApplication.translate("MainWindow", u"Thermal radiation calculation following BR 187 (Parallel rectangular orientation).", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_0401_br187_parallel_simple.setText(QCoreApplication.translate("MainWindow", u"BR 187\n"
"Parallel", None))
#if QT_CONFIG(tooltip)
        self.pushButton_0402_br187_perpendicular_simple.setToolTip(QCoreApplication.translate("MainWindow", u"Thermal radiation calculation following BR 187 (Perpendicular rectangular orientation).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_0402_br187_perpendicular_simple.setStatusTip(QCoreApplication.translate("MainWindow", u"Thermal radiation calculation following BR 187 (Perpendicular rectangular orientation).", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_0402_br187_perpendicular_simple.setText(QCoreApplication.translate("MainWindow", u"BR 187\n"
"Perp.", None))
#if QT_CONFIG(tooltip)
        self.pushButton_0403_br187_parallel_complex.setToolTip(QCoreApplication.translate("MainWindow", u"Thermal radiation calculation following BR 187 (Parallel rectangular orientation).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_0403_br187_parallel_complex.setStatusTip(QCoreApplication.translate("MainWindow", u"Thermal radiation calculation following BR 187 (Parallel rectangular orientation).", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_0403_br187_parallel_complex.setText(QCoreApplication.translate("MainWindow", u"BR 187\n"
"Parallel 2", None))
#if QT_CONFIG(tooltip)
        self.pushButton_0404_br187_perpendicular_complex.setToolTip(QCoreApplication.translate("MainWindow", u"Thermal radiation calculation following BR 187 (Perpendicular rectangular orientation).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_0404_br187_perpendicular_complex.setStatusTip(QCoreApplication.translate("MainWindow", u"Thermal radiation calculation following BR 187 (Perpendicular rectangular orientation).", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_0404_br187_perpendicular_complex.setText(QCoreApplication.translate("MainWindow", u"BR 187\n"
"Perp. 2", None))
#if QT_CONFIG(tooltip)
        self.pushButton_0405_thermal_radiation_extreme.setToolTip(QCoreApplication.translate("MainWindow", u"General purpose thermal radiation calculator.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_0405_thermal_radiation_extreme.setStatusTip(QCoreApplication.translate("MainWindow", u"General purpose thermal radiation calculator.", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_0405_thermal_radiation_extreme.setText(QCoreApplication.translate("MainWindow", u"Therm. Rad.\n"
"Analysis", None))
        self.label_big_name.setText(QCoreApplication.translate("MainWindow", u"OFR TOOLBOX", None))
        self.label_copy_right.setText(QCoreApplication.translate("MainWindow", u"\u00a9 OFR Consultants Ltd.\n"
"All rights reserved.", None))
        self.label_logo.setText("")
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"Version #.#.#", None))
    # retranslateUi

