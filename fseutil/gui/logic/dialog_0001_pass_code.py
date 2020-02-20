from PySide2 import QtWidgets, QtGui, QtCore

import fseutil
from fseutil.gui.images_base64 import OFR_LOGO_1_PNG

EXPIRY_DATE_PERIOD = 90


class Dialog0001(QtWidgets.QDialog):
    _pass_code = None

    def __init__(self, parent=None):
        super().__init__(parent)

        # ui elements instantiation
        self.label = QtWidgets.QLabel(
            f'Software is too old to run.\nEither to get the latest version or enter passcode.\n{fseutil.__version__}.')
        self.edit = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton('Submit')

        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # window properties
        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_1_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.setWindowIcon(pix_map)
        self.setWindowTitle('Warning')

        # signals and slots
        self.button.clicked.connect(self.submit)

    def submit(self):
        self._pass_code = self.edit.text()
        QtWidgets.QApplication.exit()

    @property
    def pass_code(self) -> str:
        return self._pass_code
