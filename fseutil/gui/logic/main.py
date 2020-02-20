from PySide2 import QtWidgets, QtGui, QtCore

import fseutil
from fseutil.gui.images_base64 import OFR_LOGO_1_PNG
from fseutil.gui.images_base64 import OFR_LOGO_2_PNG
from fseutil.gui.layout.main import Ui_MainWindow
from fseutil.gui.logic.dialog_0101_adb_datasheet_1 import Dialog as Dialog0101
from fseutil.gui.logic.dialog_0102_bs9999_datasheet_1 import Dialog as Dialog0102
from fseutil.gui.logic.dialog_0103_bs9999_merging_flow import Dialog0103 as Dialog0103
from fseutil.gui.logic.dialog_0111_pd7974_heat_detector_activation import Dialog0111 as Dialog0111
from fseutil.gui.logic.dialog_0401_br187_parallel_simple import Dialog0401 as Dialog0401
from fseutil.gui.logic.dialog_0402_br187_perpendicular_simple import Dialog0402 as Dialog0402
from fseutil.gui.logic.dialog_0403_br187_parallel_complex import Dialog0403 as Dialog0403
from fseutil.gui.logic.dialog_0404_br187_perpendicular_complex import Dialog0404 as Dialog0404
from fseutil.gui.logic.dialog_0405_thermal_radiation_extreme import Dialog0405 as Dialog0405
from fseutil.gui.logic.dialog_0601_naming_convention import Dialog0601 as Dialog0601
from fseutil.gui.logic.dialog_0602_pd7974_flame_height import Dialog0602 as Dialog0602

try:
    from fseutil.__key__ import key
    KEY = key()
except ModuleNotFoundError:
    KEY = None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # ui setup
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # window properties
        self.setWindowTitle('OFR Fire Safety Engineering Utility Tools')
        self.statusBar().setSizeGripEnabled(False)
        self.setFixedSize(self.width(), self.height())

        # signals
        self.init_buttons()

        # default values
        self.ui.label_big_name.setText('FSE Toolbox')
        self.ui.label_version.setText('Version ' + fseutil.__version__)
        self.ui.label_version.setStyleSheet('color: grey;')
        self.ui.label_version.setStatusTip('Version ' + fseutil.__version__)
        self.ui.label_version.setToolTip('Version ' + fseutil.__version__)
        self.init_logos()  # logo
        self.ui.dialog_error = QtWidgets.QErrorMessage(self)
        self.ui.dialog_error.setWindowTitle('Message')

    def init_logos(self):
        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_1_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.setWindowIcon(pix_map)

        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_2_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.ui.label_logo.setPixmap(pix_map)

        # tips
        self.ui.label_logo.setToolTip('Click to go to ofrconsultants.com')
        self.ui.label_logo.setStatusTip('Click to go to ofrconsultants.com')

        # signals
        self.ui.label_logo.mousePressEvent = self.label_logo_mousePressEvent

    def label_logo_mousePressEvent(self, event=None):
        if event:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://ofrconsultants.com/"))

    def init_buttons(self):

        self.ui.pushButton_0101_adb2_datasheet_1.clicked.connect(lambda: self.activate_app(Dialog0101))
        self.ui.pushButton_0102_bs9999_datasheet_1.clicked.connect(lambda: self.activate_app(Dialog0102))
        self.ui.pushButton_0103_merging_flow.clicked.connect(lambda: self.activate_app(Dialog0103))
        self.ui.pushButton_0111_heat_detector_activation.clicked.connect(lambda: self.activate_app(Dialog0111))

        self.ui.pushButton_0401_br187_parallel_simple.clicked.connect(lambda: self.activate_app(Dialog0401))
        self.ui.pushButton_0402_br187_perpendicular_simple.clicked.connect(lambda: self.activate_app(Dialog0402))
        self.ui.pushButton_0403_br187_parallel_complex.clicked.connect(lambda: self.activate_app(Dialog0403))
        self.ui.pushButton_0404_br187_perpendicular_complex.clicked.connect(lambda: self.activate_app(Dialog0404))
        self.ui.pushButton_0405_thermal_radiation_extreme.clicked.connect(lambda: self.activate_app(Dialog0405))

        self.ui.pushButton_0601_naming_convention.clicked.connect(lambda: self.activate_app(Dialog0601))
        self.ui.pushButton_0602_pd7974_flame_height.clicked.connect(lambda: self.activate_app(Dialog0602))

    def activate_app(self, app_):
        app_ = app_(self)
        app_.show()
        try:
            app_.exec_()
        except AttributeError:
            pass
        return app_
