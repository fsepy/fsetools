from PySide2 import QtWidgets, QtGui, QtCore

from fsetools.gui.images_base64 import dialog_0101_adb2_datasheet_1
from fsetools.gui.images_base64 import OFR_LOGO_1_PNG


class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

        self.resize(800, 600)

        self.label = QtWidgets.QLabel()
        ba = QtCore.QByteArray.fromBase64(dialog_0101_adb2_datasheet_1)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.label.setPixmap(pix_map)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.label)

        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

        # window properties
        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_1_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.setWindowIcon(pix_map)
        self.setWindowTitle('Approved Document B 2019 Vol. 2 Data Sheet 1')

        self.repaint()
