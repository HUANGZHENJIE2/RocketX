from PyQt5.QtWidgets import QMenu, QMessageBox

from utils.utils import read_text_file
from menu.help_menu import HelpMenu
from menu.servers_menu import ServersMenu
from menu.system_proxy_menu import SystemProxyMenu
from menu.theme_menu import ThemeMenu
from utils.resources import Resources
from services import server
import sys


class SystemTrayIconContextMenu(QMenu):
    def __init__(self, app):
        super(SystemTrayIconContextMenu, self).__init__()
        self.app = app
        self.guiConfig = self.app.guiConfig

        self.connectAndDisconnectAction = self.addAction("Connect")
        self.systemProxyMenu = SystemProxyMenu(self.app)
        self.systemProxyAction = self.addAction("System Proxy")
        self.serversMenu = ServersMenu(self.app)
        self.serversAction = self.addAction("Servers")
        self.pacAction = self.addAction("PAC")
        self.forwardProxyAction = self.addAction("Forward Proxy")
        self.addSeparator()
        self.connectAutomaticallyAction = self.addAction("Connect Automatically")
        self.startBootAction = self.addAction("Start Boot")
        self.allowOtherDevicesToConnectAction = self.addAction("Allow other Devices to connect")
        self.addSeparator()
        self.themeAction = self.addAction("Theme")
        self.helpMenu = HelpMenu(self.app)
        self.themeMenu = ThemeMenu(self.app)
        self.helpAction = self.addAction("Help")
        self.exitAction = self.addAction("Exit")
        self.isConnected = False

        self.init()

        # 绑定菜单
        self.helpAction.setMenu(self.helpMenu)
        self.systemProxyAction.setMenu(self.systemProxyMenu)
        self.serversAction.setMenu(self.serversMenu)
        self.themeAction.setMenu(self.themeMenu)

        # 绑定信槽
        self.connectAutomaticallyAction.triggered.connect(self.connectAutomaticallyActionTriggered)
        self.startBootAction.triggered.connect(self.startBootActionTriggered)
        self.allowOtherDevicesToConnectAction.triggered.connect(self.allowOtherDevicesToConnectActionTriggered)
        self.connectAndDisconnectAction.triggered.connect(self.connectAndDisconnectActionTriggered)
        self.exitAction.triggered.connect(self.exit)

    def init(self):
        print("init() .....................")
        theme = self.guiConfig.guiConfig['settings']['theme']
        self.setStyleSheet(
            read_text_file(Resources.getResourcesPathByTheme(theme, 'menu'))
        )

        pros = self.app.strings.properties

        # 根据配置初始化菜单
        self.setStartBoot()
        self.setConnectAutomatically()
        self.setAllowOtherDevicesToConnect()

        connectAutomatically = self.guiConfig.guiConfig['settings']['connectAutomatically']
        if connectAutomatically:
            self.app.guiConfig.writeNewJsonFile('forwardServer', 'config.json')
            self.connectServer()

        server.start_pac_server(self.app.guiConfig.guiConfig['pac']['host'],
                                self.app.guiConfig.guiConfig['pac']['port'])

        # 根据属性文件初始化菜单
        self.helpAction.setText(pros['help'])
        self.allowOtherDevicesToConnectAction.setText(pros['allowOtherDevicesToConnectAction'])
        self.startBootAction.setText(pros['startBoot'])
        self.forwardProxyAction.setText(pros['forwardProxy'])
        self.pacAction.setText(pros['PAC'])
        self.serversAction.setText(pros['servers'])
        self.systemProxyAction.setText(pros['systemProxy'])
        self.connectAutomaticallyAction.setText(pros['connectAutomatically'])
        self.themeAction.setText(pros['theme'])
        self.exitAction.setText(pros['exit'])



    def reloadServer(self):
        self.serversMenu = ServersMenu(self.app)
        self.serversAction.setMenu(self.serversMenu)
        print("debug reloadServer")

    def connectAutomaticallyActionTriggered(self):
        self.guiConfig.guiConfig['settings']['connectAutomatically'] = not self.guiConfig.guiConfig['settings']['connectAutomatically']
        self.guiConfig.write()
        self.setConnectAutomatically()

    def startBootActionTriggered(self):
        self.guiConfig.guiConfig['settings']['startBoot'] = not self.guiConfig.guiConfig['settings']['startBoot']
        self.guiConfig.write()
        self.setStartBoot()

    def allowOtherDevicesToConnectActionTriggered(self):
        self.guiConfig.guiConfig['settings']['allowOtherDevicesToConnect'] = not self.guiConfig.guiConfig['settings'][
            'allowOtherDevicesToConnect']
        self.guiConfig.write()
        self.setAllowOtherDevicesToConnect()

    def connectAndDisconnectActionTriggered(self):
        if self.isConnected:
            self.disconnectServer()
        else:
            self.connectServer()

    def connectServer(self):
        theme = self.guiConfig.guiConfig['settings']['theme']
        pros = self.app.strings.properties
        if len(self.app.guiConfig.guiConfig['serverList']) == 0:
            self.informationBox(pros['connect'], pros['connectFailed'])
            return

        server.start_forward_server()
        self.isConnected = True
        self.connectAndDisconnectAction.setText(pros['disconnect'])
        self.app.systemTrayIcon.setIcon(Resources.getIconByThemeAndFilename(theme, 'public.png'))
        self.app.systemTrayIcon.setToolTip(pros['connected'].replace(
            '{0}',
            self.guiConfig.guiConfig["serverList"][self.guiConfig.guiConfig['settings']['selectedServerIndex']][
                'remarks']
        ).replace(
            '{1}', pros['appName']).replace(
            '{2}', pros[self.guiConfig.guiConfig['systemProxy']['proxyMode']]))
        self.systemProxyMenu.setEnabledProxy()

    def disconnectServer(self):
        theme = self.guiConfig.guiConfig['settings']['theme']
        pros = self.app.strings.properties
        server.kill_forward_server()
        self.isConnected = False
        self.connectAndDisconnectAction.setText(pros['connect'])
        self.app.systemTrayIcon.setIcon(Resources.getIconByThemeAndFilename(theme, 'public_off.png'))
        self.app.systemTrayIcon.setToolTip(pros['notConnected'].replace('{0}', pros['appName']))
        self.systemProxyMenu.setDisabledProxy()

    def setConnectAutomatically(self):
        theme = self.guiConfig.guiConfig['settings']['theme']
        connectAutomatically = self.guiConfig.guiConfig['settings']['connectAutomatically']
        if connectAutomatically:
            self.connectAutomaticallyAction.setIcon(Resources.getIconByThemeAndFilename(theme, "selected.png"))
        else:
            self.connectAutomaticallyAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))

    def setStartBoot(self):
        theme = self.guiConfig.guiConfig['settings']['theme']
        startBoot = self.guiConfig.guiConfig['settings']['startBoot']
        if startBoot:
            self.startBootAction.setIcon(Resources.getIconByThemeAndFilename(theme, "selected.png"))
        else:
            self.startBootAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))

    def setAllowOtherDevicesToConnect(self):
        theme = self.guiConfig.guiConfig['settings']['theme']
        allowOtherDevicesToConnect = self.guiConfig.guiConfig['settings']['allowOtherDevicesToConnect']

        if allowOtherDevicesToConnect:
            self.allowOtherDevicesToConnectAction.setIcon(Resources.getIconByThemeAndFilename(theme, "selected.png"))
        else:
            self.allowOtherDevicesToConnectAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))

    def setConnectAndDisconnectAction(self):
        if self.guiConfig.guiConfig['settings']['isConnected']:
            self.connectAndDisconnectAction.setText("Disconnect")
        else:
            self.connectAndDisconnectAction.setText("Connect")

    def setSystemTrayIconAndToolTip(self):
        theme = self.guiConfig.guiConfig['settings']['theme']
        if self.guiConfig.guiConfig['settings']['isConnected']:
            self.app.systemTrayIcon.setIcon(Resources.getIconByThemeAndFilename(theme, 'public.png'))
            self.app.systemTrayIcon.setToolTip("Connected -Rocket X")
        else:
            self.app.systemTrayIcon.setIcon(Resources.getIconByThemeAndFilename(theme, 'public_off.png'))
            self.app.systemTrayIcon.setToolTip("Not connect -Rocket X")

    def exit(self):
        self.disconnectServer()
        sys.exit()

    def informationBox(self, title, text):
        informationMessageBox = QMessageBox(self)
        informationMessageBox.setWindowIcon(Resources.getIconByFilename('app.ico'))
        informationMessageBox.setWindowTitle(title)
        informationMessageBox.setIcon(QMessageBox.Information)
        informationMessageBox.setText(text)
        informationMessageBox.exec()
        return
