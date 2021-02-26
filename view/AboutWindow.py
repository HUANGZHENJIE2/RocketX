from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from resources import Resources
from .ui_about import Ui_AboutWindow


class AboutWindow(QMainWindow):
    def __init__(self, app):
        super(AboutWindow, self).__init__()
        self.app = app
        self.ui = Ui_AboutWindow()
        self.setLayout(QHBoxLayout())
        self.setWindowTitle("About")
        self.setWindowIcon(Resources.getIconByFilename('app.ico'))
        # self.ui.label_5.setPixmap(Resources.getQPixmapByFilename('app.ico'))
        self.ui.setupUi(self)

        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def closeEvent(self, event):
        self.hide()
        event.ignore()