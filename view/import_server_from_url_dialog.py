# ImportServerFromURLDialog


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QDialog

from resources import Resources
from .ui_import_server_from_url import Ui_ImportServerFromURLDialog


class ImportServerFromURLDialog(QDialog):
    def __init__(self, app):
        super(ImportServerFromURLDialog, self).__init__()
        self.app = app
        self.ui = Ui_ImportServerFromURLDialog()
        self.setWindowIcon(Resources.getIconByFilename('app.ico'))
        self.ui.setupUi(self)

    def closeEvent(self, event):
        self.hide()
        event.ignore()
