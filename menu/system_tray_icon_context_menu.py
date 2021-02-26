from PyQt5.QtWidgets import QMenu

from menu.help_menu import HelpMenu
from menu.servers_menu import ServersMenu
from menu.system_proxy_menu import SystemProxyMenu
from resources import Resources


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
        self.startBootAction = self.addAction("Start Boot")
        self.allowOtherDevicesToConnectAction = self.addAction("Allow other Devices to connect")
        self.addSeparator()
        self.helpMenu = HelpMenu(self.app)
        self.helpAction = self.addAction("Help")

        self.init()

    def init(self):
        self.setStyleSheet(
            '''
                 QMenu {
                    background-color: rgb(236,236,237);
                    border-width: 1px 1px 1px 1px;
                    border-style: solid;
                    border-color: #c6c6c6;
                    font: 9pt "Arial";
                    padding: 3px 0px
                }
                
                QMenu::item {
                    font-size:9pt "Arial";
                    color: rgb(0,0,0);
                    background-color: rgb(236,236,237);
                    padding: 8px 40px 8px 15px;
                }
                QMenu::icon{
                    position: absolute;
                    top: 1px;
                    right: 1px;
                    bottom: 1px;
                    left: 10px;
                }
                
                QMenu::item:selected {
                    background-color : rgb(255, 255, 255);
                }

            '''
        )

        # 根据配置初始化菜单
        self.setStartBoot()
        self.setAllowOtherDevicesToConnect()

        # 根据属性文件初始化菜单
        pros = self.app.strings.properties
        self.helpAction.setText(pros['systemTrayIconContextMenu.help'])

        # 绑定菜单
        self.helpAction.setMenu(self.helpMenu)
        self.systemProxyAction.setMenu(self.systemProxyMenu)
        self.serversAction.setMenu(self.serversMenu)

        # 绑定信槽
        self.startBootAction.triggered.connect(self.startBootActionTriggered)
        self.allowOtherDevicesToConnectAction.triggered.connect(self.allowOtherDevicesToConnectActionTriggered)
        self.connectAndDisconnectAction.triggered.connect(self.connectAndDisconnectActionTriggered)
        pass

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
        self.guiConfig.guiConfig['settings']['isConnected'] = not self.guiConfig.guiConfig['settings']['isConnected']
        self.guiConfig.write()
        self.setConnectAndDisconnectAction()
        self.setSystemTrayIconAndToolTip()

    def setStartBoot(self):
        startBoot = self.guiConfig.guiConfig['settings']['startBoot']
        if startBoot:
            self.startBootAction.setIcon(Resources.getIconByFilename('baseline_check_black_18dp.png'))
        else:
            self.startBootAction.setIcon(Resources.getIconByFilename('hzj'))

    def setAllowOtherDevicesToConnect(self):
        allowOtherDevicesToConnect = self.guiConfig.guiConfig['settings']['allowOtherDevicesToConnect']

        if allowOtherDevicesToConnect:
            self.allowOtherDevicesToConnectAction.setIcon(Resources.getIconByFilename('baseline_check_black_18dp.png'))
        else:
            self.allowOtherDevicesToConnectAction.setIcon(Resources.getIconByFilename('hzj'))

    def setConnectAndDisconnectAction(self):
        if self.guiConfig.guiConfig['settings']['isConnected']:
            self.connectAndDisconnectAction.setText("Disconnect")
        else:
            self.connectAndDisconnectAction.setText("Connect")

    def setSystemTrayIconAndToolTip(self):
        if self.guiConfig.guiConfig['settings']['isConnected']:
            self.app.systemTrayIcon.setIcon(Resources.getIconByFilename('baseline_public_black_18dp.png'))
            self.app.systemTrayIcon.setToolTip("Connected -Rocket X")
        else:
            self.app.systemTrayIcon.setIcon(Resources.getIconByFilename('baseline_public_off_black_18dp.png'))
            self.app.systemTrayIcon.setToolTip("Not connect -Rocket X")