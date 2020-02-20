# !/usr/bin/python
# coding:utf-8

import sys

from PySide2 import QtCore, QtWidgets

from fsetools.gui.logic.main import MainWindow

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


def main():

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
