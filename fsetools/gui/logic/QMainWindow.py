import typing

from PySide2 import QtCore, QtWidgets, QtGui

from fsetools.gui.images_base64 import OFR_LOGO_1_PNG
from fsetools.gui.logic.common import filter_objects_by_name
CSS = \
    {
        'QWidget':
            {
                'background-color': 'white',
            },
        'QLabel#label':
            {
                'color': '#888888',
                'background-color': '#444444',
                'font-weight': 'bold',
            },
        'QLabel#label:active':
            {
                'color': '#1d90cd',
            },
        'QPushButton#button':
            {
                'color': 'grey',
                'background-color': 'grey',
                # 'font-weight': 'bold',
                'border': '1px',
                # 'padding': '5px',
            },
        'QPushButton#button:active':
            {
                'color': '#ffffff',
            },
        'QPushButton#button:hover':
            {
                'color': 'red',
            }
    }


def dictToCSS(dictionary):
    stylesheet = ""
    for item in dictionary:
        stylesheet += item + "\n{\n"
        for attribute in dictionary[item]:
            stylesheet += "  " + attribute + ": " + dictionary[item][attribute] + ";\n"
        stylesheet += "}\n"
    return stylesheet


class QMainWindow(QtWidgets.QMainWindow):
    def __init__(
            self,
            title: str,
            icon: typing.Union[bytes, QtCore.QByteArray] = OFR_LOGO_1_PNG,
            parent=None):

        super().__init__(parent=parent)
        self.__title = title
        self.__icon = icon

    def init(self):

        # window properties
        ba = QtCore.QByteArray.fromBase64(self.__icon)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.setWindowIcon(pix_map)
        self.setWindowTitle(self.__title)
        # self.setStyleSheet(
        #     "QMainWindow {background: 'white';};"
        #     "#QPushButton {background: 'white';}"
        # )

        self.setStyleSheet(dictToCSS(CSS))
        # for i in filter_objects_by_name(self, object_types=[QtWidgets.QPushButton]):
        #     i.setStyleSheet("background-color: white")
