from PySide2 import QtWidgets, QtGui, QtCore
from fsetools.gui.logic.main_0000_QMainWindow import QMainWindow

from fsetools.gui.images_base64 import dialog_0103_bs9999_merging_flow_context as image_context
from fsetools.gui.images_base64 import dialog_0103_bs9999_mergine_flow_figure_1 as image_figure_1
from fsetools.gui.images_base64 import dialog_0103_bs9999_mergine_flow_figure_2 as image_figure_2
from fsetools.gui.images_base64 import dialog_0103_bs9999_mergine_flow_figure_3 as image_figure_3

from fsetools.gui.layout.dialog_0103_merging_flow import Ui_MainWindow
from fsetools.gui.logic.common import filter_objects_by_name
from fsetools.libstd.bs_9999_2017 import (
    clause_15_6_6_e_merging_flow_1, clause_15_6_6_e_merging_flow_2, clause_15_6_6_e_merging_flow_3
)


class Dialog0103(QMainWindow):

    maximum_acceptable_thermal_radiation_heat_flux = 12.6

    def __init__(self, parent=None):
        # instantiation
        super().__init__(parent=parent, title='Means of Escape Merging Flow')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.setWindowTitle('Means of Escape Merging Flow')

        # construct pixmaps that are used in this app
        self.dict_images_pixmap = dict(
            image_context=image_context,
            image_figure_1=image_figure_1,
            image_figure_2=image_figure_2,
            image_figure_3=image_figure_3,
        )
        for k, v in self.dict_images_pixmap.items():
            ba = QtCore.QByteArray.fromBase64(v)
            self.dict_images_pixmap[k] = QtGui.QPixmap()
            self.dict_images_pixmap[k].loadFromData(ba)

        # set all outputs lineedit to readonly
        for i in filter_objects_by_name(
                self.ui.groupBox_outputs,
                object_types=[QtWidgets.QLineEdit, QtWidgets.QCheckBox]):
            try:
                i.setReadOnly(True)
            except AttributeError:
                i.setEnabled(False)

        # set up context image
        self.ui.label_image_context.setPixmap(self.dict_images_pixmap['image_context'])

        # entry default values
        self.ui.radioButton_opt_scenario_1.setChecked(True)
        self.change_option_scenarios()

        # set up validators

        # signals
        self.ui.pushButton_calculate.clicked.connect(self.calculate)
        self.ui.pushButton_test.clicked.connect(self.test)
        self.ui.radioButton_opt_scenario_1.toggled.connect(self.change_option_scenarios)
        self.ui.radioButton_opt_scenario_2.toggled.connect(self.change_option_scenarios)
        self.ui.radioButton_opt_scenario_3.toggled.connect(self.change_option_scenarios)

    def keyPressEvent(self, event):
        if event.key() == 16777221 or event.key() == 16777220 or event.key() == QtCore.Qt.Key_Enter:
            self.calculate()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def change_option_scenarios(self):
        """When mode changes, turn off (grey them out) not required inputs and clear their value."""

        # enable everything in input group to start with.
        # ui items will be disabled for scenario 1 or 2 (if applicable) below.
        list_obj = filter_objects_by_name(
            self.ui.groupBox_inputs, [QtWidgets.QLabel, QtWidgets.QLineEdit], ['_in_S_dn', '_in_W_SE', '_in_B', '_in_N']
        )
        for i in list_obj:
            i.setEnabled(True)

        # disable items in accordance with the selected mode
        if self.ui.radioButton_opt_scenario_1.isChecked():  # scenario 1, flow from upper levels + ground floor
            # get items that to be processed
            list_obj = filter_objects_by_name(
                self.ui.groupBox_inputs, [QtWidgets.QLabel, QtWidgets.QLineEdit], ['_in_S_dn', '_in_B']
            )
            # disable items that are not required in scenario 1
            for i in list_obj:
                i.setEnabled(False)
                if isinstance(i, QtWidgets.QLineEdit):
                    i.setText('')
            # set figure to scenario 1
            self.ui.label_image_figure.setPixmap(self.dict_images_pixmap['image_figure_1'])

        elif self.ui.radioButton_opt_scenario_2.isChecked():  # scenario 2, flow from upper levels + basement
            list_obj = filter_objects_by_name(
                self.ui.groupBox_inputs, [QtWidgets.QLabel, QtWidgets.QLineEdit], ['_in_W_SE', '_in_N']
            )
            for i in list_obj:
                i.setEnabled(False)
                if isinstance(i, QtWidgets.QLineEdit):
                    i.setText('')
            # set figure to scenario 2
            self.ui.label_image_figure.setPixmap(self.dict_images_pixmap['image_figure_2'])

        else:
            # set figure to scenario 3
            self.ui.label_image_figure.setPixmap(self.dict_images_pixmap['image_figure_3'])

    def test(self):
        self.ui.lineEdit_in_X.setText('3.06')
        self.ui.lineEdit_in_D.setText('2.1')
        self.ui.lineEdit_in_S_up.setText('1400')
        self.ui.lineEdit_in_N.setText('270')
        self.ui.lineEdit_in_W_SE.setText('1050')

        self.ui.radioButton_opt_scenario_1.setChecked(True)

        self.calculate()

    def calculate(self):

        # clear ui output fields
        self.ui.checkBox_out_check.setChecked(False)
        self.ui.lineEdit_out_W_FE.setText('')

        # parse inputs from ui
        try:
            S_up = float(self.ui.lineEdit_in_S_up.text()) / 1e3
            S_dn = float(self.ui.lineEdit_in_S_dn.text()) / 1e3 if self.ui.lineEdit_in_S_dn.isEnabled() else None
            B = float(self.ui.lineEdit_in_B.text()) / 1e3 if self.ui.lineEdit_in_B.isEnabled() else None
            X = float(self.ui.lineEdit_in_X.text()) / 1e3
            D = float(self.ui.lineEdit_in_D.text())
            N = float(self.ui.lineEdit_in_N.text()) if self.ui.lineEdit_in_N.isEnabled() else None
            W_SE = float(self.ui.lineEdit_in_W_SE.text()) / 1e3 if self.ui.lineEdit_in_W_SE.isEnabled() else None
        except Exception as e:
            self.statusBar().showMessage(f'Unable to parse input. Error: {e}.')
            self.repaint()
            raise ValueError

        # calculate
        try:
            if self.ui.radioButton_opt_scenario_1.isChecked():
                W_FE, condition_check = clause_15_6_6_e_merging_flow_1(
                    N=N,
                    X=X,
                    D=D,
                    S_up=S_up,
                    W_SE=W_SE,
                )
            elif self.ui.radioButton_opt_scenario_2.isChecked():
                W_FE, condition_check = clause_15_6_6_e_merging_flow_2(
                    B=B,
                    X=X,
                    D=D,
                    S_up=S_up,
                    S_dn=S_dn,
                )
            elif self.ui.radioButton_opt_scenario_3.isChecked():
                W_FE, condition_check = clause_15_6_6_e_merging_flow_3(
                    B=B,
                    X=X,
                    D=D,
                    S_up=S_up,
                    S_dn=S_dn,
                    N=N,
                    W_SE=W_SE,
                )
            else:
                raise ValueError('Unknown scenario.')
        except Exception as e:
            self.statusBar().showMessage(f'Calculation failed. Error: {e}')
            self.repaint()
            raise ValueError

        self.ui.checkBox_out_check.setChecked(condition_check)
        self.ui.lineEdit_out_W_FE.setText(f'{W_FE*1e3:.1f}')

        self.statusBar().showMessage('Calculation complete.')
        self.repaint()
