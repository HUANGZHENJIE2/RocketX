import sys

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from gui_config import GuiConfig
from menu.system_tray_icon_context_menu import SystemTrayIconContextMenu
from properties import Properties
from utils.resources import Resources
from view.about_window import AboutWindow
from view.edit_servers_window import EditServersWindow
from view.feedback_window import FeedbackWindow
from view.qrcode_main_window import QRCodeMainWindow


class Application:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.guiConfig = GuiConfig()
        self.strings = Properties()
        self.aboutWindow = AboutWindow(self)
        self.feedbackWindow = FeedbackWindow(self)
        self.qrcodeMainWindow = QRCodeMainWindow(self)
        self.editServersWindow = EditServersWindow(self)
        self.systemTrayIcon = QSystemTrayIcon(None)
        self.systemTrayIconContextMenu = SystemTrayIconContextMenu(self)

        self.selectedServer = {}
        self.selectedServerIndex = 0

        self.init()
        pass

    def init(self):
        if len(self.guiConfig.guiConfig['serverList']) == 0:
            self.editServersWindow.show()
        self.systemTrayIcon.setContextMenu(self.systemTrayIconContextMenu)
        self.systemTrayIcon.setIcon(Resources.getIconByFilename('app.ico'))

    def run(self):
        self.systemTrayIcon.show()
        sys.exit(self.app.exec_())
        pass

    def refresh(self):
        self.systemTrayIconContextMenu.init()
        self.systemTrayIconContextMenu.themeMenu.init()
        self.systemTrayIconContextMenu.systemProxyMenu.init()
        self.systemTrayIconContextMenu.serversMenu.init()
        self.systemTrayIconContextMenu.helpMenu.init()

