from PySide2 import QtWidgets, QtGui, QtCore

import fsetools
from fsetools.gui.images_base64 import OFR_LOGO_1_PNG
from fsetools.gui.images_base64 import OFR_LOGO_2_PNG
from fsetools.gui.layout.main import Ui_MainWindow
from fsetools.gui.logic.dialog_0101_adb_datasheet_1 import Dialog as Dialog0101
from fsetools.gui.logic.dialog_0102_bs9999_datasheet_1 import Dialog as Dialog0102
from fsetools.gui.logic.dialog_0103_bs9999_merging_flow import Dialog0103 as Dialog0103
from fsetools.gui.logic.dialog_0111_pd7974_heat_detector_activation import Dialog0111 as Dialog0111
from fsetools.gui.logic.dialog_0401_br187_parallel_simple import Dialog0401 as Dialog0401
from fsetools.gui.logic.dialog_0402_br187_perpendicular_simple import Dialog0402 as Dialog0402
from fsetools.gui.logic.dialog_0403_br187_parallel_complex import Dialog0403 as Dialog0403
from fsetools.gui.logic.dialog_0404_br187_perpendicular_complex import Dialog0404 as Dialog0404
from fsetools.gui.logic.dialog_0405_thermal_radiation_extreme import Dialog0405 as Dialog0405
from fsetools.gui.logic.dialog_0601_naming_convention import Dialog0601 as Dialog0601
from fsetools.gui.logic.dialog_0602_pd7974_flame_height import Dialog0602 as Dialog0602
from fsetools.etc.util import check_online_version

import threading
from packaging import version


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # ui setup
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # check update
        check_update = threading.Timer(1, self.check_update)
        check_update.start()  # after 60 seconds, 'callback' will be called

        # window properties
        self.setWindowTitle('Fire Safety Engineering Tools')
        self.statusBar().setSizeGripEnabled(False)
        self.setFixedSize(self.width(), self.height())
        self.ui.label_version.setText(f'Version {fsetools.__version__}')
        self.ui.label_version.setStatusTip(f'Version {fsetools.__version__}')
        self.ui.label_version.setToolTip(f'Version {fsetools.__version__}')

        # signals
        self.init_buttons()

        # default values
        self.ui.label_big_name.setText('FSE Tools')
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
        self.ui.label_version.mousePressEvent = self.label_version_mousePressEvent

    def label_logo_mousePressEvent(self, event=None):
        if event:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://ofrconsultants.com/"))

    def label_version_mousePressEvent(self, event=None):
        if event:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/fsepy/fsetools/releases"))

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

    def check_update(self):
        online_version = check_online_version(
            url=r'https://raw.githubusercontent.com/fsepy/fsetools/master/fsetools/__init__.py',
            current_version=fsetools.__version__
        )

        version_label_text = online_version

        if len(version_label_text) == 0:
            version_label_text = 'Version ' + fsetools.__version__
            self.ui.label_version.setStyleSheet('color: black;')
        elif version.parse(online_version) > version.parse(fsetools.__version__):
            version_label_text = f'New version {version_label_text} available.' + ' Click to download.'
            self.ui.label_version.setStyleSheet('color: red;')
        else:
            version_label_text = 'Version ' + online_version
            self.ui.label_version.setStyleSheet('color: grey;')

        self.ui.label_version.setText(version_label_text)
        self.ui.label_version.setStatusTip(version_label_text)
        self.ui.label_version.setToolTip(version_label_text)
