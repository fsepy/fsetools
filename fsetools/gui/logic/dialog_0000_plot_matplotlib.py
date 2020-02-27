import sys
import time

import numpy as np
from PySide2 import QtCore, QtWidgets, QtGui

# from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5

try:
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
except ModuleNotFoundError:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, figure, title: str = None, icon: bytes = None):
        super().__init__()

        # window properties
        if icon:
            ba = QtCore.QByteArray.fromBase64(QtCore.QByteArray(icon))
            pix_map = QtGui.QPixmap()
            pix_map.loadFromData(ba)
            self.setWindowIcon(pix_map)
        if title:
            self.setWindowTitle(title)

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        figure_canvas = FigureCanvas(figure)
        layout.addWidget(figure_canvas)
        self.addToolBar(NavigationToolbar(figure_canvas, self))

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()


if __name__ == "__main__":
    from matplotlib.figure import Figure
    from fsetools.gui.images_base64 import OFR_LOGO_1_PNG

    fig = Figure()
    ax = fig.subplots()
    ax.set_xlabel('x-axis label')
    ax.set_ylabel('y-axis label')

    ax.axis('off')

    t = np.linspace(0, 10, 501)
    ax.plot(t, np.tan(t), ".")

    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow(fig, title='Test Window Title', icon=OFR_LOGO_1_PNG)
    app.show()
    qapp.exec_()
