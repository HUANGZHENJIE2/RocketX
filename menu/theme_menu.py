from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu

from utils.utils import read_text_file
from utils.resources import Resources


class ThemeMenu(QMenu):
    def __init__(self, app):
        super(ThemeMenu, self).__init__()
        self.app = app

        self.lightAction = self.addAction("Light")
        self.darkAction = self.addAction("Dark")

        self.init()

        self.lightAction.triggered.connect(self.lightActionTriggered)
        self.darkAction.triggered.connect(self.darkActionTriggered)

    def init(self):

        theme = self.app.guiConfig.guiConfig['settings']['theme']
        self.setStyleSheet(
            read_text_file(Resources.getResourcesPathByTheme(theme, 'menu'))
        )
        pros = self.app.strings.properties
        self.lightAction.setText(pros["light"])
        self.darkAction.setText(pros["dark"])

        theme = self.app.guiConfig.guiConfig['settings']['theme']
        if theme == 'light':
            self.lightAction.setIcon(Resources.getIconByThemeAndFilename(theme, "selected.png"))

        if theme == "dark":
            self.darkAction.setIcon(Resources.getIconByThemeAndFilename(theme, "selected.png"))



    def lightActionTriggered(self):
        theme = self.app.guiConfig.guiConfig['settings']['theme']
        self.app.guiConfig.guiConfig['settings']['theme'] = "light"
        self.app.guiConfig.write()
        self.lightAction.setIcon(Resources.getIconByThemeAndFilename(theme, "selected.png"))
        self.darkAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))

        self.app.refresh()
        print("Refresh ui (light)")

    def darkActionTriggered(self):
        theme = self.app.guiConfig.guiConfig['settings']['theme']
        self.app.guiConfig.guiConfig['settings']['theme'] = "dark"
        self.app.guiConfig.write()
        self.darkAction.setIcon(Resources.getIconByThemeAndFilename(theme, "selected.png"))
        self.lightAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))

        self.app.refresh()
        print("Refresh ui (dark)")
