from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu

from utils.utils import read_text_file
from utils.resources import Resources


class HelpMenu(QMenu):
    def __init__(self, app):
        super(HelpMenu, self).__init__()
        self.app = app

        self.feedbackAction = self.addAction("feedback")
        self.aboutAction = self.addAction("About")

        self.init()

    def init(self):

        self.setStyleSheet(
            read_text_file(Resources.getResourcesPackagesPath('menu'))
        )
        pros = self.app.strings.properties
        self.feedbackAction.setText(pros["feedback"])
        self.aboutAction.setText(pros["about"])

        self.feedbackAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))

        self.aboutAction.triggered.connect(self.aboutActionTriggered)
        self.feedbackAction.triggered.connect(self.feedbackActionTriggered)

    def aboutActionTriggered(self):
        if self.app.aboutWindow.isVisible():
            self.app.aboutWindow.hide()
        self.app.aboutWindow.show()

    def feedbackActionTriggered(self):
        if self.app.feedbackWindow.isVisible():
            self.app.feedbackWindow.hide()
        self.app.feedbackWindow.show()
