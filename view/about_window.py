from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from utils.utils import read_text_file
from utils.resources import Resources
from .ui_about import Ui_AboutWindow


class AboutWindow(QMainWindow):
    def __init__(self, app):
        super(AboutWindow, self).__init__()
        self.app = app
        self.ui = Ui_AboutWindow()
        self.setLayout(QHBoxLayout())
        self.setWindowIcon(Resources.getIconByFilename('app.ico'))
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.init()

    def init(self):
        self.setStyleSheet(
            read_text_file(Resources.getResourcesPackagesPath('window'))
        )

    def closeEvent(self, event):
        self.hide()
        event.ignore()