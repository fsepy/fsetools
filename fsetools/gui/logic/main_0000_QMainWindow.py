import sys
import time

import numpy as np
from PySide2 import QtCore, QtWidgets, QtGui
from fsetools.gui.images_base64 import OFR_LOGO_1_PNG
import typing

class QMainWindow(QtWidgets.QMainWindow):
    def __init__(
            self,
            title: str,
            icon: typing.Union[bytes, QtCore.QByteArray] = OFR_LOGO_1_PNG,
            parent=None):
        super().__init__(parent=parent)

        # window properties
        if icon:
            ba = QtCore.QByteArray.fromBase64(icon)
            pix_map = QtGui.QPixmap()
            pix_map.loadFromData(ba)
            self.setWindowIcon(pix_map)
        if title:
            self.setWindowTitle(title)
