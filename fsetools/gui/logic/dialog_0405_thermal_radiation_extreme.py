from PySide2 import QtWidgets, QtGui, QtCore
import numpy as np
from fsetools.lib.fse_thermal_radiation_3d import single_receiver, heat_flux_to_temperature
from fsetools.gui.images_base64 import dialog_0404_br187_perpendicular_figure_1
from fsetools.gui.layout.dialog_0405_thermal_radiation_extreme import Ui_MainWindow


class Dialog0405(QtWidgets.QMainWindow):
    maximum_acceptable_thermal_radiation_heat_flux = 12.6

    def __init__(self, parent=None):
        super(Dialog0405, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Thermal Radiation Analysis Extreme')

        from fsetools.gui.logic.common import filter_objects_by_name
        for i in filter_objects_by_name(self.ui.groupBox_out, object_types=[QtWidgets.QLineEdit]):
            try:
                i.setReadOnly(True)
            except AttributeError:
                i.setEnabled(False)

        # set up radiation figure
        ba = QtCore.QByteArray.fromBase64(dialog_0404_br187_perpendicular_figure_1)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.ui.label.setPixmap(pix_map)

        # set default values
        self.ui.lineEdit_in_emitter_points.setText('1000')
        self.ui.lineEdit_in_receiver_initial_temperature.setText('293.15')

        # set signals
        self.ui.pushButton_test.clicked.connect(self.test)
        self.ui.pushButton_calculate.clicked.connect(self.calculate)

    def keyPressEvent(self, event):
        if event.key() == 16777221 or event.key() == 16777220 or event.key() == QtCore.Qt.Key_Enter:
            self.copy_file_name()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def test(self):

        self.ui.plainTextEdit_in_emiter_xyz.setPlainText('0,0,5\n0,5,5\n5,5,5\n5,0,5')
        self.ui.lineEdit_in_emitter_normal.setText('0,0,-1')
        self.ui.lineEdit_in_receiver_location.setText('2.5,2.5,0')
        self.ui.lineEdit_in_receiver_normal.setText('0,0,1')
        self.ui.lineEdit_in_Q.setText('100')

        self.calculate()

        self.repaint()

    def calculate(self):

        # clear ui output fields
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')
        self.ui.lineEdit_out_T.setText('')

        # parse inputs from ui
        emitter_points = int(self.ui.lineEdit_in_emitter_points.text())
        emitter_vertices = list()
        for i in [i.split(',') for i in str.strip(self.ui.plainTextEdit_in_emiter_xyz.toPlainText()).replace(' ', '').split('\n')]:
            if len(i) == 0:
                continue
            i_ = list()
            for j in i:
                i_.append(float(j))
            emitter_vertices.append(i_)
        emitter_normal = [float(i) for i in self.ui.lineEdit_in_emitter_normal.text().split(',')]
        receiver_xyz = [float(i) for i in self.ui.lineEdit_in_receiver_location.text().split(',')]
        receiver_normal = [float(i) for i in self.ui.lineEdit_in_receiver_normal.text().split(',')]
        receiver_initial_temperature = float(self.ui.lineEdit_in_receiver_initial_temperature.text())
        Q = float(self.ui.lineEdit_in_Q.text())

        # calculate
        emitter_temperature = heat_flux_to_temperature(Q*1000)
        receiver_heat_flux, phi = single_receiver(
            ep_vertices=np.array(emitter_vertices),
            ep_norm=np.array(emitter_normal),
            ep_temperature=emitter_temperature,
            n_points=emitter_points,  # number of hot spots
            rp_vertices=np.array(receiver_xyz),
            rp_norm=np.array(receiver_normal),
            rp_temperature=receiver_initial_temperature
        )

        # write results to ui
        self.ui.lineEdit_out_Phi.setText(f'{phi:.4f}')
        self.ui.lineEdit_out_q.setText(f'{receiver_heat_flux/1000:.2f}')
        self.ui.lineEdit_out_T.setText(f'{emitter_temperature:.2f}')

        # refresh ui
        self.repaint()
