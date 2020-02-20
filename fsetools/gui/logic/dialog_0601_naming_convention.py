from datetime import datetime

from PySide2 import QtWidgets, QtCore, QtGui

from fsetools.gui.layout.dialog_0601_naming_convention import Ui_MainWindow


class Dialog0601(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # init
        super(Dialog0601, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('OFR File Name Generator')

        # default values
        self.ui.lineEdit_1_date.setText(datetime.today().strftime('%Y%m%d')[2:])
        self.ui.comboBox_6_type.setCurrentIndex(4)
        self.ui.checkBox_replace_spaces.setChecked(True)

        # validators
        self.ui.lineEdit_1_date.setValidator((QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]{6,8}'))))
        self.ui.lineEdit_3_project_no.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[A-Z]{1,2}[0-9]{1,5}')))
        self.ui.lineEdit_4_project_stage.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[\w\-. ]+$')))
        self.ui.lineEdit_5_title.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[\w\-. ]+$')))

        # signal and slots
        self.ui.lineEdit_1_date.textChanged.connect(self.make_file_name)
        self.ui.comboBox_2_revision.currentTextChanged.connect(self.make_file_name)
        self.ui.lineEdit_3_project_no.textChanged.connect(self.make_file_name)
        self.ui.lineEdit_4_project_stage.textChanged.connect(self.make_file_name)
        self.ui.lineEdit_5_title.textChanged.connect(self.make_file_name)
        self.ui.comboBox_6_type.currentTextChanged.connect(self.make_file_name)
        self.ui.comboBox_7_security_status.currentTextChanged.connect(self.make_file_name)
        self.ui.checkBox_replace_spaces.stateChanged.connect(self.make_file_name)
        self.ui.pushButton_copy.clicked.connect(self.copy_file_name)

        # clean up
        self.make_file_name()  # make file name, do not leave the output slot empty
        self.repaint()

    def keyPressEvent(self, event):
        if event.key() == 16777221 or event.key() == 16777220 or event.key() == QtCore.Qt.Key_Enter:
            self.copy_file_name()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def make_file_name(self):
        aa = self.ui.lineEdit_1_date.text()
        bb = self.ui.comboBox_2_revision.currentText()[0:3]
        cc = self.ui.lineEdit_3_project_no.text()
        dd = self.ui.lineEdit_4_project_stage.text()
        ee = self.ui.lineEdit_5_title.text()
        ff = self.ui.comboBox_6_type.currentText()[0:2]
        gg = self.ui.comboBox_7_security_status.currentText()[0:3]

        if self.ui.checkBox_replace_spaces.isChecked():
            dd = dd.replace(' ', '_')
            ee = ee.replace(' ', '_')

        self.ui.lineEdit_out_result.setText('-'.join([aa, bb, cc, dd, ee, ff, gg]))

        self.repaint()

    def copy_file_name(self):
        clipboard = QtGui.QGuiApplication.clipboard()
        clipboard.setText(self.ui.lineEdit_out_result.text())
        self.ui.lineEdit_out_result.selectAll()

        self.ui.statusbar.showMessage('File name is copied.')
