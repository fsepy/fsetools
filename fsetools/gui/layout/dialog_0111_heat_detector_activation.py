# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ian/Documents/GitHub/fsetools/fsetools/gui/layout/ui/dialog_0111_heat_detector_activation.ui',
# licensing of '/Users/ian/Documents/GitHub/fsetools/fsetools/gui/layout/ui/dialog_0111_heat_detector_activation.ui' applies.
#
# Created: Thu Feb 20 22:28:39 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(826, 669)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 585, 826, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton_calculate = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_calculate.setGeometry(QtCore.QRect(715, 610, 96, 24))
        self.pushButton_calculate.setObjectName("pushButton_calculate")
        self.pushButton_test = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_test.setGeometry(QtCore.QRect(15, 610, 96, 24))
        self.pushButton_test.setObjectName("pushButton_test")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(15, 15, 796, 566))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../images/0111_1_heat_detector_794_560.png"))
        self.label.setObjectName("label")
        self.groupBox_in = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_in.setGeometry(QtCore.QRect(400, 320, 201, 256))
        self.groupBox_in.setObjectName("groupBox_in")
        self.label_51 = QtWidgets.QLabel(self.groupBox_in)
        self.label_51.setGeometry(QtCore.QRect(140, 225, 146, 21))
        self.label_51.setMinimumSize(QtCore.QSize(0, 0))
        self.label_51.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_51.setObjectName("label_51")
        self.label_48 = QtWidgets.QLabel(self.groupBox_in)
        self.label_48.setGeometry(QtCore.QRect(140, 150, 146, 21))
        self.label_48.setMinimumSize(QtCore.QSize(0, 0))
        self.label_48.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_48.setObjectName("label_48")
        self.label_in_R_label = QtWidgets.QLabel(self.groupBox_in)
        self.label_in_R_label.setGeometry(QtCore.QRect(10, 100, 60, 21))
        self.label_in_R_label.setMinimumSize(QtCore.QSize(60, 21))
        self.label_in_R_label.setMaximumSize(QtCore.QSize(60, 21))
        self.label_in_R_label.setObjectName("label_in_R_label")
        self.label_40 = QtWidgets.QLabel(self.groupBox_in)
        self.label_40.setGeometry(QtCore.QRect(10, 175, 60, 21))
        self.label_40.setMinimumSize(QtCore.QSize(60, 21))
        self.label_40.setMaximumSize(QtCore.QSize(60, 21))
        self.label_40.setObjectName("label_40")
        self.lineEdit_in_C_conv = QtWidgets.QLineEdit(self.groupBox_in)
        self.lineEdit_in_C_conv.setGeometry(QtCore.QRect(70, 200, 60, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_in_C_conv.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_C_conv.setSizePolicy(sizePolicy)
        self.lineEdit_in_C_conv.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_in_C_conv.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_in_C_conv.setBaseSize(QtCore.QSize(0, 0))
        self.lineEdit_in_C_conv.setObjectName("lineEdit_in_C_conv")
        self.label_31 = QtWidgets.QLabel(self.groupBox_in)
        self.label_31.setGeometry(QtCore.QRect(10, 25, 60, 21))
        self.label_31.setMinimumSize(QtCore.QSize(60, 21))
        self.label_31.setMaximumSize(QtCore.QSize(60, 21))
        self.label_31.setObjectName("label_31")
        self.lineEdit_in_T_act = QtWidgets.QLineEdit(self.groupBox_in)
        self.lineEdit_in_T_act.setGeometry(QtCore.QRect(70, 225, 60, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_in_T_act.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_T_act.setSizePolicy(sizePolicy)
        self.lineEdit_in_T_act.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_in_T_act.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_in_T_act.setBaseSize(QtCore.QSize(0, 0))
        self.lineEdit_in_T_act.setObjectName("lineEdit_in_T_act")
        self.label_49 = QtWidgets.QLabel(self.groupBox_in)
        self.label_49.setGeometry(QtCore.QRect(140, 175, 146, 21))
        self.label_49.setMinimumSize(QtCore.QSize(0, 0))
        self.label_49.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_49.setObjectName("label_49")
        self.lineEdit_in_R = QtWidgets.QLineEdit(self.groupBox_in)
        self.lineEdit_in_R.setGeometry(QtCore.QRect(70, 100, 60, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_in_R.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_R.setSizePolicy(sizePolicy)
        self.lineEdit_in_R.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_in_R.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_in_R.setBaseSize(QtCore.QSize(0, 0))
        self.lineEdit_in_R.setObjectName("lineEdit_in_R")
        self.label_39 = QtWidgets.QLabel(self.groupBox_in)
        self.label_39.setGeometry(QtCore.QRect(10, 150, 60, 21))
        self.label_39.setMinimumSize(QtCore.QSize(60, 21))
        self.label_39.setMaximumSize(QtCore.QSize(60, 21))
        self.label_39.setObjectName("label_39")
        self.label_in_R_unit = QtWidgets.QLabel(self.groupBox_in)
        self.label_in_R_unit.setGeometry(QtCore.QRect(140, 100, 146, 21))
        self.label_in_R_unit.setMinimumSize(QtCore.QSize(0, 0))
        self.label_in_R_unit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_in_R_unit.setObjectName("label_in_R_unit")
        self.lineEdit_in_C = QtWidgets.QLineEdit(self.groupBox_in)
        self.lineEdit_in_C.setGeometry(QtCore.QRect(70, 150, 60, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_in_C.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_C.setSizePolicy(sizePolicy)
        self.lineEdit_in_C.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_in_C.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_in_C.setBaseSize(QtCore.QSize(0, 0))
        self.lineEdit_in_C.setObjectName("lineEdit_in_C")
        self.label_47 = QtWidgets.QLabel(self.groupBox_in)
        self.label_47.setGeometry(QtCore.QRect(140, 125, 146, 21))
        self.label_47.setMinimumSize(QtCore.QSize(0, 0))
        self.label_47.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_47.setObjectName("label_47")
        self.label_35 = QtWidgets.QLabel(self.groupBox_in)
        self.label_35.setGeometry(QtCore.QRect(10, 50, 60, 21))
        self.label_35.setMinimumSize(QtCore.QSize(60, 21))
        self.label_35.setMaximumSize(QtCore.QSize(60, 21))
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.groupBox_in)
        self.label_36.setGeometry(QtCore.QRect(10, 75, 60, 21))
        self.label_36.setMinimumSize(QtCore.QSize(60, 21))
        self.label_36.setMaximumSize(QtCore.QSize(60, 21))
        self.label_36.setObjectName("label_36")
        self.lineEdit_in_RTI = QtWidgets.QLineEdit(self.groupBox_in)
        self.lineEdit_in_RTI.setGeometry(QtCore.QRect(70, 125, 60, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_in_RTI.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_RTI.setSizePolicy(sizePolicy)
        self.lineEdit_in_RTI.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_in_RTI.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_in_RTI.setBaseSize(QtCore.QSize(0, 0))
        self.lineEdit_in_RTI.setObjectName("lineEdit_in_RTI")
        self.label_45 = QtWidgets.QLabel(self.groupBox_in)
        self.label_45.setGeometry(QtCore.QRect(140, 75, 146, 21))
        self.label_45.setMinimumSize(QtCore.QSize(0, 0))
        self.label_45.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_45.setObjectName("label_45")
        self.lineEdit_in_H = QtWidgets.QLineEdit(self.groupBox_in)
        self.lineEdit_in_H.setGeometry(QtCore.QRect(70, 75, 60, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_in_H.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_H.setSizePolicy(sizePolicy)
        self.lineEdit_in_H.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_in_H.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_in_H.setBaseSize(QtCore.QSize(0, 0))
        self.lineEdit_in_H.setObjectName("lineEdit_in_H")
        self.lineEdit_in_t = QtWidgets.QLineEdit(self.groupBox_in)
        self.lineEdit_in_t.setGeometry(QtCore.QRect(70, 25, 60, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_in_t.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_t.setSizePolicy(sizePolicy)
        self.lineEdit_in_t.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_in_t.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_in_t.setBaseSize(QtCore.QSize(0, 0))
        self.lineEdit_in_t.setObjectName("lineEdit_in_t")
        self.label_43 = QtWidgets.QLabel(self.groupBox_in)
        self.label_43.setGeometry(QtCore.QRect(140, 25, 146, 21))
        self.label_43.setMinimumSize(QtCore.QSize(0, 0))
        self.label_43.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_43.setObjectName("label_43")
        self.lineEdit_in_alpha = QtWidgets.QLineEdit(self.groupBox_in)
        self.lineEdit_in_alpha.setGeometry(QtCore.QRect(70, 50, 60, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_in_alpha.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_alpha.setSizePolicy(sizePolicy)
        self.lineEdit_in_alpha.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_in_alpha.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_in_alpha.setBaseSize(QtCore.QSize(0, 0))
        self.lineEdit_in_alpha.setObjectName("lineEdit_in_alpha")
        self.label_41 = QtWidgets.QLabel(self.groupBox_in)
        self.label_41.setGeometry(QtCore.QRect(10, 200, 60, 21))
        self.label_41.setMinimumSize(QtCore.QSize(60, 21))
        self.label_41.setMaximumSize(QtCore.QSize(60, 21))
        self.label_41.setObjectName("label_41")
        self.label_44 = QtWidgets.QLabel(self.groupBox_in)
        self.label_44.setGeometry(QtCore.QRect(140, 50, 146, 21))
        self.label_44.setMinimumSize(QtCore.QSize(0, 0))
        self.label_44.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_44.setObjectName("label_44")
        self.label_42 = QtWidgets.QLabel(self.groupBox_in)
        self.label_42.setGeometry(QtCore.QRect(10, 225, 60, 21))
        self.label_42.setMinimumSize(QtCore.QSize(60, 21))
        self.label_42.setMaximumSize(QtCore.QSize(60, 21))
        self.label_42.setObjectName("label_42")
        self.label_38 = QtWidgets.QLabel(self.groupBox_in)
        self.label_38.setGeometry(QtCore.QRect(10, 125, 60, 21))
        self.label_38.setMinimumSize(QtCore.QSize(60, 21))
        self.label_38.setMaximumSize(QtCore.QSize(60, 21))
        self.label_38.setObjectName("label_38")
        self.lineEdit_in_HRRPUA = QtWidgets.QLineEdit(self.groupBox_in)
        self.lineEdit_in_HRRPUA.setGeometry(QtCore.QRect(70, 175, 60, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_in_HRRPUA.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_HRRPUA.setSizePolicy(sizePolicy)
        self.lineEdit_in_HRRPUA.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_in_HRRPUA.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_in_HRRPUA.setBaseSize(QtCore.QSize(0, 0))
        self.lineEdit_in_HRRPUA.setObjectName("lineEdit_in_HRRPUA")
        self.groupBox_gas_correlation = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_gas_correlation.setGeometry(QtCore.QRect(610, 430, 201, 80))
        self.groupBox_gas_correlation.setObjectName("groupBox_gas_correlation")
        self.radioButton_ceiling_jet = QtWidgets.QRadioButton(self.groupBox_gas_correlation)
        self.radioButton_ceiling_jet.setGeometry(QtCore.QRect(10, 25, 176, 20))
        self.radioButton_ceiling_jet.setObjectName("radioButton_ceiling_jet")
        self.radioButton_fire_plume = QtWidgets.QRadioButton(self.groupBox_gas_correlation)
        self.radioButton_fire_plume.setGeometry(QtCore.QRect(10, 50, 171, 20))
        self.radioButton_fire_plume.setObjectName("radioButton_fire_plume")
        self.groupBox_out = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_out.setGeometry(QtCore.QRect(610, 520, 201, 56))
        self.groupBox_out.setObjectName("groupBox_out")
        self.lineEdit_out_t_act = QtWidgets.QLineEdit(self.groupBox_out)
        self.lineEdit_out_t_act.setGeometry(QtCore.QRect(75, 25, 60, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_out_t_act.sizePolicy().hasHeightForWidth())
        self.lineEdit_out_t_act.setSizePolicy(sizePolicy)
        self.lineEdit_out_t_act.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_out_t_act.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_out_t_act.setToolTip("")
        self.lineEdit_out_t_act.setObjectName("lineEdit_out_t_act")
        self.label_11 = QtWidgets.QLabel(self.groupBox_out)
        self.label_11.setGeometry(QtCore.QRect(15, 25, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QtCore.QSize(61, 0))
        self.label_11.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label_11.setObjectName("label_11")
        self.label_25 = QtWidgets.QLabel(self.groupBox_out)
        self.label_25.setGeometry(QtCore.QRect(145, 25, 50, 21))
        self.label_25.setObjectName("label_25")
        self.pushButton_show_results_in_table = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_show_results_in_table.setEnabled(False)
        self.pushButton_show_results_in_table.setGeometry(QtCore.QRect(615, 610, 96, 24))
        self.pushButton_show_results_in_table.setObjectName("pushButton_show_results_in_table")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEdit_in_t, self.lineEdit_in_alpha)
        MainWindow.setTabOrder(self.lineEdit_in_alpha, self.lineEdit_in_H)
        MainWindow.setTabOrder(self.lineEdit_in_H, self.lineEdit_in_R)
        MainWindow.setTabOrder(self.lineEdit_in_R, self.lineEdit_in_RTI)
        MainWindow.setTabOrder(self.lineEdit_in_RTI, self.lineEdit_in_C)
        MainWindow.setTabOrder(self.lineEdit_in_C, self.lineEdit_in_HRRPUA)
        MainWindow.setTabOrder(self.lineEdit_in_HRRPUA, self.lineEdit_in_C_conv)
        MainWindow.setTabOrder(self.lineEdit_in_C_conv, self.lineEdit_in_T_act)
        MainWindow.setTabOrder(self.lineEdit_in_T_act, self.radioButton_ceiling_jet)
        MainWindow.setTabOrder(self.radioButton_ceiling_jet, self.radioButton_fire_plume)
        MainWindow.setTabOrder(self.radioButton_fire_plume, self.pushButton_calculate)
        MainWindow.setTabOrder(self.pushButton_calculate, self.pushButton_test)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.pushButton_calculate.setText(QtWidgets.QApplication.translate("MainWindow", "Calculate", None, -1))
        self.pushButton_test.setText(QtWidgets.QApplication.translate("MainWindow", "Example", None, -1))
        self.groupBox_in.setTitle(QtWidgets.QApplication.translate("MainWindow", "Inputs", None, -1))
        self.label_51.setText(QtWidgets.QApplication.translate("MainWindow", "°C", None, -1))
        self.label_48.setText(QtWidgets.QApplication.translate("MainWindow", "m<sup>0.5</sup>/s<sup>0.5</sup>", None, -1))
        self.label_in_R_label.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Lateral distance between HD and fire central axis", None, -1))
        self.label_in_R_label.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Lateral distance between HD and fire central axis", None, -1))
        self.label_in_R_label.setText(QtWidgets.QApplication.translate("MainWindow", "R", None, -1))
        self.label_40.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Heat release rate per unit area", None, -1))
        self.label_40.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Heat release rate per unit area", None, -1))
        self.label_40.setText(QtWidgets.QApplication.translate("MainWindow", "HRRPUA", None, -1))
        self.lineEdit_in_C_conv.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.lineEdit_in_C_conv.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.label_31.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Fire duration", None, -1))
        self.label_31.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Fire duration", None, -1))
        self.label_31.setText(QtWidgets.QApplication.translate("MainWindow", "t", None, -1))
        self.lineEdit_in_T_act.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.lineEdit_in_T_act.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.label_49.setText(QtWidgets.QApplication.translate("MainWindow", "kW/m²", None, -1))
        self.lineEdit_in_R.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.lineEdit_in_R.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.label_39.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Conduction factor", None, -1))
        self.label_39.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Conduction factor", None, -1))
        self.label_39.setText(QtWidgets.QApplication.translate("MainWindow", "C", None, -1))
        self.label_in_R_unit.setText(QtWidgets.QApplication.translate("MainWindow", "m", None, -1))
        self.lineEdit_in_C.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.lineEdit_in_C.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.label_47.setText(QtWidgets.QApplication.translate("MainWindow", "m<sup>0.5</sup>⋅s<sup>0.5</sup>", None, -1))
        self.label_35.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Fire growth factor for t-square fire", None, -1))
        self.label_35.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Fire growth factor for t-square fire", None, -1))
        self.label_35.setText(QtWidgets.QApplication.translate("MainWindow", "α", None, -1))
        self.label_36.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Vertical distance between the fire bed and the detecting element", None, -1))
        self.label_36.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Vertical distance between the fire bed and the detecting element", None, -1))
        self.label_36.setText(QtWidgets.QApplication.translate("MainWindow", "H", None, -1))
        self.lineEdit_in_RTI.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.lineEdit_in_RTI.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.label_45.setText(QtWidgets.QApplication.translate("MainWindow", "m", None, -1))
        self.lineEdit_in_H.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.lineEdit_in_H.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.lineEdit_in_t.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.lineEdit_in_t.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.label_43.setText(QtWidgets.QApplication.translate("MainWindow", "s", None, -1))
        self.lineEdit_in_alpha.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Positive float, {\'slow\': 0.0029, \'medium\': 0.0117, \'fast\': 0.0469, \'ultra-fast\': 0.1876}", None, -1))
        self.lineEdit_in_alpha.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Positive float, {\'slow\': 0.0029, \'medium\': 0.0117, \'fast\': 0.0469, \'ultra-fast\': 0.1876}", None, -1))
        self.label_41.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Percentage of convective heat release rate to total heat release rate", None, -1))
        self.label_41.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Percentage of convective heat release rate to total heat release rate", None, -1))
        self.label_41.setText(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>C<span style=\" vertical-align:sub;\">conv</span></p></body></html>", None, -1))
        self.label_44.setText(QtWidgets.QApplication.translate("MainWindow", "kW/s²", None, -1))
        self.label_42.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Heat detecting element activation temperature", None, -1))
        self.label_42.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Heat detecting element activation temperature", None, -1))
        self.label_42.setText(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>T<span style=\" vertical-align:sub;\">act</span></p></body></html>", None, -1))
        self.label_38.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Response time index", None, -1))
        self.label_38.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Response time index", None, -1))
        self.label_38.setText(QtWidgets.QApplication.translate("MainWindow", "RTI", None, -1))
        self.lineEdit_in_HRRPUA.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.lineEdit_in_HRRPUA.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Positive float", None, -1))
        self.groupBox_gas_correlation.setTitle(QtWidgets.QApplication.translate("MainWindow", "Gas Correlation", None, -1))
        self.radioButton_ceiling_jet.setToolTip(QtWidgets.QApplication.translate("MainWindow", "To use ceiling jet equations for calculating temperature and velocity", None, -1))
        self.radioButton_ceiling_jet.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "To use ceiling jet equations for calculating temperature and velocity", None, -1))
        self.radioButton_ceiling_jet.setText(QtWidgets.QApplication.translate("MainWindow", "Use Ceiling Jet Equations", None, -1))
        self.radioButton_fire_plume.setToolTip(QtWidgets.QApplication.translate("MainWindow", "To use plume equations for calculating temperature and velocity", None, -1))
        self.radioButton_fire_plume.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "To use plume equations for calculating temperature and velocity", None, -1))
        self.radioButton_fire_plume.setText(QtWidgets.QApplication.translate("MainWindow", "Use Plume Equations", None, -1))
        self.groupBox_out.setTitle(QtWidgets.QApplication.translate("MainWindow", "Outputs", None, -1))
        self.label_11.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Solved heat detecting element activation time", None, -1))
        self.label_11.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Solved heat detecting element activation time", None, -1))
        self.label_11.setText(QtWidgets.QApplication.translate("MainWindow", "t<sub>act<sub>", None, -1))
        self.label_25.setText(QtWidgets.QApplication.translate("MainWindow", "s", None, -1))
        self.pushButton_show_results_in_table.setText(QtWidgets.QApplication.translate("MainWindow", "Full Results", None, -1))

