from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from resources import Resources
from view.ui_feedback import Ui_Feedback


class FeedbackWindow(QMainWindow):
    def __init__(self, app):
        super(FeedbackWindow, self).__init__()
        self.app = app
        self.ui = Ui_Feedback()
        self.setWindowIcon(Resources.getIconByFilename('app.ico'))
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def closeEvent(self, event):
        self.hide()
        event.ignore()