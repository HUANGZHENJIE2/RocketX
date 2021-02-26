from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QDialog

from resources import Resources
from .ui_transport_settings import Ui_TransportSettings



class TransportSettingsDialog(QDialog):
    def __init__(self, app):
        super(TransportSettingsDialog, self).__init__()
        self.app = app
        self.ui = Ui_TransportSettings()
        #self.setLayout(QHBoxLayout())
        self.setWindowTitle("About")
        self.setWindowIcon(Resources.getIconByFilename('app.ico'))
        self.ui.setupUi(self)


    def closeEvent(self, event):
        self.hide()
        event.ignore()