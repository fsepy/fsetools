import operator
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore


class TableWindow(QtWidgets.QDialog):
    def __init__(self, data_list, header, window_title: str = None, parent=None, *args):
        super().__init__(parent, *args)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        # QtWidgets.QWidget.__init__(self, *args)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 200, 570, 450)
        if window_title:
            self.setWindowTitle(window_title)
        self.TableModel = TableModel(self, data_list, header)
        table_view = QtWidgets.QTableView()
        table_view.setModel(self.TableModel)
        # set font
        font = QtGui.QFont("Courier New", 14)
        table_view.setFont(font)
        # set column width to fit contents (set font first!)
        table_view.resizeColumnsToContents()
        # enable sorting
        table_view.setSortingEnabled(True)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(table_view)
        self.setLayout(layout)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, content: list, row_header: list, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.content = content
        self.row_header = row_header

    def rowCount(self, parent):
        return len(self.content)

    def columnCount(self, parent):
        return len(self.content[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.content[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.row_header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.content = sorted(
            self.content,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.content.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))


if __name__ == '__main__':
    # the solvent data ...
    header = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)']
    # use numbers for numeric data to sort properly
    data_list = [
        ('ACETIC ACID', 117.9, 16.7, 1.049),
        ('ACETIC ANHYDRIDE', 140.1, -73.1, 1.087),
        ('ACETONE', 56.3, -94.7, 0.791),
        ('ACETONITRILE', 81.6, -43.8, 0.786)
    ]

    app = QtWidgets.QApplication([])
    win = TableWindow(data_list, header)
    win.show()
    app.exec_()
