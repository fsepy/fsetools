# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_0601_naming_convention.ui'
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
        MainWindow.resize(391, 356)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(15, 15, 361, 291))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_16 = QLabel(self.verticalLayoutWidget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(121, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_16)

        self.lineEdit_1_date = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_1_date.setObjectName(u"lineEdit_1_date")
        self.lineEdit_1_date.setMinimumSize(QSize(0, 21))
        self.lineEdit_1_date.setMaximumSize(QSize(70, 16777215))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_1_date)

        self.label_15 = QLabel(self.verticalLayoutWidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(121, 21))
        self.label_15.setFont(font)
        self.label_15.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_15)

        self.comboBox_2_revision = QComboBox(self.verticalLayoutWidget)
        self.comboBox_2_revision.addItem("")
        self.comboBox_2_revision.addItem("")
        self.comboBox_2_revision.addItem("")
        self.comboBox_2_revision.addItem("")
        self.comboBox_2_revision.addItem("")
        self.comboBox_2_revision.addItem("")
        self.comboBox_2_revision.addItem("")
        self.comboBox_2_revision.setObjectName(u"comboBox_2_revision")
        self.comboBox_2_revision.setMinimumSize(QSize(0, 21))
        self.comboBox_2_revision.setMaximumSize(QSize(16777215, 16777215))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox_2_revision)

        self.label_14 = QLabel(self.verticalLayoutWidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(121, 21))
        self.label_14.setMaximumSize(QSize(90, 16777215))
        self.label_14.setFont(font)
        self.label_14.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_14)

        self.lineEdit_3_project_no = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_3_project_no.setObjectName(u"lineEdit_3_project_no")
        self.lineEdit_3_project_no.setMinimumSize(QSize(0, 21))
        self.lineEdit_3_project_no.setMaximumSize(QSize(90, 16777215))

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_3_project_no)

        self.label_17 = QLabel(self.verticalLayoutWidget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(121, 21))
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_17)

        self.lineEdit_4_project_stage = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_4_project_stage.setObjectName(u"lineEdit_4_project_stage")
        self.lineEdit_4_project_stage.setMinimumSize(QSize(0, 21))
        self.lineEdit_4_project_stage.setMaximumSize(QSize(90, 16777215))

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEdit_4_project_stage)

        self.label_18 = QLabel(self.verticalLayoutWidget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(121, 21))
        self.label_18.setFont(font)
        self.label_18.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_18)

        self.label_19 = QLabel(self.verticalLayoutWidget)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(121, 21))
        self.label_19.setFont(font)
        self.label_19.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_19)

        self.comboBox_6_type = QComboBox(self.verticalLayoutWidget)
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.addItem("")
        self.comboBox_6_type.setObjectName(u"comboBox_6_type")
        self.comboBox_6_type.setMinimumSize(QSize(0, 21))

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.comboBox_6_type)

        self.label_20 = QLabel(self.verticalLayoutWidget)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(121, 21))
        self.label_20.setFont(font)
        self.label_20.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_20)

        self.comboBox_7_security_status = QComboBox(self.verticalLayoutWidget)
        self.comboBox_7_security_status.addItem("")
        self.comboBox_7_security_status.addItem("")
        self.comboBox_7_security_status.addItem("")
        self.comboBox_7_security_status.addItem("")
        self.comboBox_7_security_status.setObjectName(u"comboBox_7_security_status")
        self.comboBox_7_security_status.setMinimumSize(QSize(0, 21))

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.comboBox_7_security_status)

        self.lineEdit_5_title = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_5_title.setObjectName(u"lineEdit_5_title")
        self.lineEdit_5_title.setMinimumSize(QSize(200, 21))

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.lineEdit_5_title)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.checkBox_replace_spaces = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_replace_spaces.setObjectName(u"checkBox_replace_spaces")

        self.verticalLayout.addWidget(self.checkBox_replace_spaces)

        self.lineEdit_out_result = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_out_result.setObjectName(u"lineEdit_out_result")

        self.verticalLayout.addWidget(self.lineEdit_out_result)

        self.line_2 = QFrame(self.verticalLayoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_copy = QPushButton(self.verticalLayoutWidget)
        self.pushButton_copy.setObjectName(u"pushButton_copy")

        self.horizontalLayout_2.addWidget(self.pushButton_copy)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 391, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.label_16.setToolTip(QCoreApplication.translate("MainWindow", u"Date in YYMMDD (i.e. 201231) or YYYYMMDD (i.e. 20201231) format.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_16.setStatusTip(QCoreApplication.translate("MainWindow", u"Date in YYMMDD (i.e. 201231) or YYYYMMDD (i.e. 20201231) format.", None))
#endif // QT_CONFIG(statustip)
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Date", None))
        self.lineEdit_1_date.setText(QCoreApplication.translate("MainWindow", u"20151021", None))
#if QT_CONFIG(tooltip)
        self.label_15.setToolTip(QCoreApplication.translate("MainWindow", u"Revision indicator.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_15.setStatusTip(QCoreApplication.translate("MainWindow", u"Revision indicator.", None))
#endif // QT_CONFIG(statustip)
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Revision", None))
        self.comboBox_2_revision.setItemText(0, QCoreApplication.translate("MainWindow", u"Q00: First issue for internal review", None))
        self.comboBox_2_revision.setItemText(1, QCoreApplication.translate("MainWindow", u"Q01: Reviewer's comments", None))
        self.comboBox_2_revision.setItemText(2, QCoreApplication.translate("MainWindow", u"Q02: Authoriser's comments", None))
        self.comboBox_2_revision.setItemText(3, QCoreApplication.translate("MainWindow", u"D00: First issue to others for comment", None))
        self.comboBox_2_revision.setItemText(4, QCoreApplication.translate("MainWindow", u"D01: Sub-sequent external reviews", None))
        self.comboBox_2_revision.setItemText(5, QCoreApplication.translate("MainWindow", u"R00: First issue", None))
        self.comboBox_2_revision.setItemText(6, QCoreApplication.translate("MainWindow", u"R01: Second issue", None))

#if QT_CONFIG(tooltip)
        self.label_14.setToolTip(QCoreApplication.translate("MainWindow", u"Project number.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_14.setStatusTip(QCoreApplication.translate("MainWindow", u"Project number.", None))
#endif // QT_CONFIG(statustip)
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Project No.", None))
        self.lineEdit_3_project_no.setText(QCoreApplication.translate("MainWindow", u"OX20001", None))
#if QT_CONFIG(tooltip)
        self.label_17.setToolTip(QCoreApplication.translate("MainWindow", u"Project stage.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_17.setStatusTip(QCoreApplication.translate("MainWindow", u"Project stage.", None))
#endif // QT_CONFIG(statustip)
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Project Stage", None))
        self.lineEdit_4_project_stage.setText(QCoreApplication.translate("MainWindow", u"WP1", None))
#if QT_CONFIG(tooltip)
        self.label_18.setToolTip(QCoreApplication.translate("MainWindow", u"File title in plain English.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_18.setStatusTip(QCoreApplication.translate("MainWindow", u"File title in plain English.", None))
#endif // QT_CONFIG(statustip)
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"File Title", None))
#if QT_CONFIG(tooltip)
        self.label_19.setToolTip(QCoreApplication.translate("MainWindow", u"Document type.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_19.setStatusTip(QCoreApplication.translate("MainWindow", u"Document type.", None))
#endif // QT_CONFIG(statustip)
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Document Type", None))
        self.comboBox_6_type.setItemText(0, QCoreApplication.translate("MainWindow", u"GA: General admin", None))
        self.comboBox_6_type.setItemText(1, QCoreApplication.translate("MainWindow", u"MD: Marketing", None))
        self.comboBox_6_type.setItemText(2, QCoreApplication.translate("MainWindow", u"FP: Fee proposal", None))
        self.comboBox_6_type.setItemText(3, QCoreApplication.translate("MainWindow", u"LT: Letter", None))
        self.comboBox_6_type.setItemText(4, QCoreApplication.translate("MainWindow", u"DN: Design note", None))
        self.comboBox_6_type.setItemText(5, QCoreApplication.translate("MainWindow", u"OF: Outline strategy", None))
        self.comboBox_6_type.setItemText(6, QCoreApplication.translate("MainWindow", u"DF: Detailed strategy", None))
        self.comboBox_6_type.setItemText(7, QCoreApplication.translate("MainWindow", u"RF: Retrospective strategy", None))
        self.comboBox_6_type.setItemText(8, QCoreApplication.translate("MainWindow", u"FA: Fire risk assessment", None))
        self.comboBox_6_type.setItemText(9, QCoreApplication.translate("MainWindow", u"FS: Fire survey report", None))
        self.comboBox_6_type.setItemText(10, QCoreApplication.translate("MainWindow", u"FN: File note", None))
        self.comboBox_6_type.setItemText(11, QCoreApplication.translate("MainWindow", u"MN: Meeting notes", None))
        self.comboBox_6_type.setItemText(12, QCoreApplication.translate("MainWindow", u"CS: Calculation sheet", None))
        self.comboBox_6_type.setItemText(13, QCoreApplication.translate("MainWindow", u"SK: Sketch", None))
        self.comboBox_6_type.setItemText(14, QCoreApplication.translate("MainWindow", u"DW: Drawing", None))
        self.comboBox_6_type.setItemText(15, QCoreApplication.translate("MainWindow", u"XO: Expert opinion", None))

#if QT_CONFIG(tooltip)
        self.label_20.setToolTip(QCoreApplication.translate("MainWindow", u"Security status.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_20.setStatusTip(QCoreApplication.translate("MainWindow", u"Security status.", None))
#endif // QT_CONFIG(statustip)
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Security Status", None))
        self.comboBox_7_security_status.setItemText(0, QCoreApplication.translate("MainWindow", u"CIC: Commercial in confidence", None))
        self.comboBox_7_security_status.setItemText(1, QCoreApplication.translate("MainWindow", u"WPC: Without prejudice and confidential", None))
        self.comboBox_7_security_status.setItemText(2, QCoreApplication.translate("MainWindow", u"SDS: Secure document", None))
        self.comboBox_7_security_status.setItemText(3, QCoreApplication.translate("MainWindow", u"FID: Free issue document (no security status)", None))

        self.lineEdit_5_title.setText(QCoreApplication.translate("MainWindow", u"Outline fire strategy report", None))
#if QT_CONFIG(tooltip)
        self.checkBox_replace_spaces.setToolTip(QCoreApplication.translate("MainWindow", u"Replace all spaces in the file name to underscore `_`.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.checkBox_replace_spaces.setStatusTip(QCoreApplication.translate("MainWindow", u"Replace all spaces in the file name to underscore `_`.", None))
#endif // QT_CONFIG(statustip)
        self.checkBox_replace_spaces.setText(QCoreApplication.translate("MainWindow", u"Replace Spaces with Underscore", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_out_result.setToolTip(QCoreApplication.translate("MainWindow", u"Composed file name.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEdit_out_result.setStatusTip(QCoreApplication.translate("MainWindow", u"Composed file name.", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_copy.setText(QCoreApplication.translate("MainWindow", u"Copy File Name (Press Enter)", None))
    # retranslateUi

