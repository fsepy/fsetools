from PySide2 import QtWidgets, QtGui, QtCore

from fseutil.etc.images_base64 import dialog_0402_br187_perpendicular_figure_1 as figure_1
from fseutil.gui.layout.dialog_0401_br187_parallel_simple import Ui_MainWindow
from fseutil.lib.fse_thermal_radiation import phi_perpendicular_any_br187, linear_solver


class Dialog0402(QtWidgets.QMainWindow):
    maximum_acceptable_thermal_radiation_heat_flux = 12.6

    def __init__(self, parent=None):
        # instantiation
        super(Dialog0402, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.change_mode_S_and_UA()
        self.setWindowTitle('BR 187 Thermal Radiation Calculation (Rectangle and Perpendicular)')

        from fseutil.gui.logic.common import filter_objects_by_name
        for i in filter_objects_by_name(self.ui.groupBox_out, object_types=[QtWidgets.QLineEdit]):
            try:
                i.setReadOnly(True)
            except AttributeError:
                i.setEnabled(False)

        # set up radiation figure
        ba = QtCore.QByteArray.fromBase64(figure_1)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.ui.label.setPixmap(pix_map)

        self.ui.comboBox_S_or_UA.currentTextChanged.connect(self.change_mode_S_and_UA)
        self.ui.pushButton_calculate.clicked.connect(self.calculate)
        self.ui.pushButton_test.clicked.connect(self.test)

    def keyPressEvent(self, event):
        if event.key() == 16777221 or event.key() == 16777220 or event.key() == QtCore.Qt.Key_Enter:
            self.calculate()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def test(self):

        self.ui.lineEdit_W.setText('50')
        self.ui.lineEdit_H.setText('50')
        self.ui.lineEdit_Q.setText('84')
        self.ui.comboBox_S_or_UA.setCurrentIndex(0)
        self.change_mode_S_and_UA()
        self.ui.lineEdit_S_or_UA.setText('2')

        self.calculate()

        self.repaint()

    def change_mode_S_and_UA(self):
        """update ui to align with whether to calculate boundary distance or unprotected area %"""

        # change input and output labels and units
        if self.ui.comboBox_S_or_UA.currentText() == '½S, emitter to boundary':  # to calculate separation to boundary
            self.ui.label_unit_S_or_UA.setText('m')
            self.ui.comboBox_S_or_UA.setToolTip('Separation distance from emitter to notional boundary.')
            self.ui.comboBox_S_or_UA.setStatusTip('Separation distance from emitter to notional boundary.')
            self.ui.label_out_S_or_UA.setText('Allowed unprotected area')
            self.ui.label_out_S_or_UA_unit.setText('%')
            self.ui.label_out_S_or_UA.setToolTip('Maximum permissible unprotected area')

        elif self.ui.comboBox_S_or_UA.currentText() == 'Allowed unprotected area':  # to calculate unprotected area percentage
            self.ui.label_unit_S_or_UA.setText('%')
            self.ui.comboBox_S_or_UA.setToolTip('Maximum permissible unprotected area.')
            self.ui.comboBox_S_or_UA.setStatusTip('Maximum permissible unprotected area.')
            self.ui.label_out_S_or_UA.setText('½S, emitter to boundary')
            self.ui.label_out_S_or_UA_unit.setText('m')
            self.ui.label_out_S_or_UA.setToolTip('Separation distance from emitter to notional boundary')
        else:
            raise ValueError('Unknown value for input UA or S.')

        # clear outputs
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')
        self.ui.lineEdit_out_S_or_UA.setText('')

        self.repaint()

    def calculate(self):

        # clear ui output fields

        self.ui.lineEdit_out_S_or_UA.setText('')
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')

        # parse inputs from ui
        try:
            W = float(self.ui.lineEdit_W.text())
            H = float(self.ui.lineEdit_H.text())
            Q = float(self.ui.lineEdit_Q.text())
        except ValueError:
            self.statusBar().showMessage(
                'Calculation unsuccessful. '
                'Unable to parse input parameters.'
            )
            self.repaint()
            raise ValueError

        # calculate

        q_target = self.maximum_acceptable_thermal_radiation_heat_flux

        if self.ui.comboBox_S_or_UA.currentText() == '½S, emitter to boundary':  # to calculate maximum unprotected area
            S = float(self.ui.lineEdit_S_or_UA.text()) * 2
            if S <= 2.:
                self.statusBar().showMessage(
                    'Calculation incomplete. '
                    'Separation to notional boundary should be > 1.0 m.'
                )
                self.repaint()
                raise ValueError

            try:
                phi_solved = phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=0., h_m=0., S_m=S)
            except ValueError:
                self.statusBar().showMessage(
                    'Calculation incomplete. '
                    'Failed due to an unknown erorr. '
                    'Please raise this issue for further investigation.'
                )
                self.repaint()
                raise ValueError

            q_solved = Q * phi_solved
            if q_solved == 0:
                UA_solved = 100
            else:
                UA_solved = max([min([q_target / q_solved * 100, 100]), 0])

            self.ui.lineEdit_out_Phi.setText(f'{phi_solved:.4f}')
            self.ui.lineEdit_out_q.setText(f'{q_solved:.2f}')
            self.ui.lineEdit_out_S_or_UA.setText(f'{UA_solved:.2f}')

            self.statusBar().showMessage('Calculation complete.')

        # to calculate minimum separation distance to boundary
        elif self.ui.comboBox_S_or_UA.currentText() == 'Allowed unprotected area':
            UA = float(self.ui.lineEdit_S_or_UA.text()) / 100.
            if not 0 < UA <= 1:
                self.statusBar().showMessage(
                    'Calculation failed. '
                    'Unprotected area should be greater >0% and <100%.'
                )
                self.repaint()
                raise ValueError

            phi_target = q_target / (Q * UA)

            try:
                S_solved = linear_solver(
                    func=phi_perpendicular_any_br187,
                    dict_params=dict(W_m=W, H_m=H, w_m=0., h_m=0., S_m=0),
                    x_name='S_m',
                    y_target=phi_target,
                    x_upper=1000,
                    x_lower=0.01,
                    y_tol=0.001,
                    iter_max=500,
                    func_multiplier=-1
                )
            except ValueError:
                self.statusBar().showMessage(
                    'Calculation failed. Inspect input parameters.'
                )
                self.repaint()
                raise ValueError
            if S_solved is None:
                self.statusBar().showMessage(
                    'Calculation failed. '
                    'Maximum iteration reached.'
                )
                self.repaint()
                raise ValueError

            phi_solved = phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=0.5 * W, h_m=0.5 * H, S_m=S_solved)
            q_solved = Q * phi_solved

            if S_solved == 1000:
                self.statusBar().showMessage(
                    'Calculation complete. '
                    'Solver\'s upper limit had reached.'
                )
            elif S_solved == 0.01:
                self.statusBar().showMessage(
                    'Calculation complete. '
                    'Solver\'s lower limit had reached and boundary separation is forced to 1.'
                )
                S_solved = 2
            elif S_solved < 2:
                self.statusBar().showMessage(
                    f'Calculation complete. '
                    f'Forced boundary separation to 1 from {S_solved:.3f} m.'
                )
                S_solved = 2
            else:
                self.statusBar().showMessage(
                    'Calculation complete.'
                )

            self.ui.lineEdit_out_Phi.setText(f'{phi_solved:.4f}')
            self.ui.lineEdit_out_q.setText(f'{q_solved:.2f}')
            self.ui.lineEdit_out_S_or_UA.setText(f'{S_solved / 2:.2f}')

        self.repaint()
