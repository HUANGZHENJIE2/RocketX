from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu

from resources import Resources


class ServersMenu(QMenu):
    def __init__(self, app):
        super(ServersMenu, self).__init__()
        self.app = app
        self.serverActions = []

        for index, server in enumerate(self.app.guiConfig.guiConfig['serverList']):
            action = self.addAction(server['remarks'])
            self.serverActions.append(action)
            action.triggered.connect(partial(self.setServer, index))

        self.addSeparator()
        # self.serverDemo.setIcon(Resources.getIconByFilename('baseline_public_off_black_18dp.png'))
        self.editServersAction = self.addAction("Edit Servers")
        self.importServerFromUrlAction = self.addAction("Import server from url")
        self.addSeparator()
        self.copySelectedServerUrlAction = self.addAction("Copy selected server url")
        self.showServerQRCode = self.addAction("Show selected server QR code")

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

        pros = self.app.strings.properties
        self.editServersAction.setText(pros["editServers"])
        self.importServerFromUrlAction.setText(pros["importServerFromUrl"])
        self.copySelectedServerUrlAction.setText(pros["copySelectedServerUrlAction"])
        self.showServerQRCode.setText(pros["showServerQRCode"])

        self.serverActions[self.app.guiConfig.guiConfig['settings']['selectedServerIndex']] \
            .setIcon(Resources.getIconByFilename('baseline_check_black_18dp.png'))
        self.editServersAction.triggered.connect(self.editServers)


    def setServer(self, index):
        self.serverActions[self.app.guiConfig.guiConfig['settings']['selectedServerIndex']] \
            .setIcon(Resources.getIconByFilename(''))
        self.app.guiConfig.guiConfig['settings']['selectedServerIndex'] = index
        self.serverActions[self.app.guiConfig.guiConfig['settings']['selectedServerIndex']] \
            .setIcon(Resources.getIconByFilename('baseline_check_black_18dp.png'))
        self.app.guiConfig.write()
        self.app.guiConfig.guiConfig['forwardServer']['outbounds'][0] = self.getOutbound()
        self.app.guiConfig.write()
        self.app.guiConfig.writeNewJsonFile('forwardServer', 'config.json')
        if self.app.systemTrayIconContextMenu.isConnected:
            self.app.systemTrayIconContextMenu.disconnectServer()
            self.app.systemTrayIconContextMenu.connectServer()

    def getOutbound(self):
        index = self.app.guiConfig.guiConfig['settings']['selectedServerIndex']
        server = self.app.guiConfig.guiConfig['serverList'][index]
        outbound = self.app.guiConfig.guiConfig['protocolOutbounds'][server['protocol']]
        print(f'set {server}')
        if server['protocol'] == 'Vmess':
            outbound['settings']['vnext'][0]['address'] = server['address']
            outbound['settings']['vnext'][0]['port'] = server['port']
            outbound['settings']['vnext'][0]['users'][0]['id'] = server['id']
            outbound['settings']['vnext'][0]['users'][0]['alterId'] = server['alterId']
            outbound['settings']['vnext'][0]['users'][0]['security'] = server['encryption']
            outbound['settings']['vnext'][0]['users'][0]['level'] = server['level']
            return outbound
        if server['protocol'] == 'Shadowscoks':
            outbound['settings']['servers'][0]['address'] = server['address']
            outbound['settings']['servers'][0]['port'] = server['port']
            outbound['settings']['servers'][0]['password'] = server['password']
            outbound['settings']['servers'][0]['method'] = server['method']
            return outbound
        if server['protocol'] == 'Trojan':
            outbound['settings']['servers'][0]['address'] = server['address']
            outbound['settings']['servers'][0]['port'] = server['port']
            outbound['settings']['servers'][0]['password'] = server['password']

            if server['host'] is not None:
                outbound['streamSettings']['tlsSettings']['serverName'] = server['host']
            print(f"debug outbound {outbound['streamSettings']}")
            outbound['streamSettings']['tlsSettings']['serverName'] = server['address']
            return outbound
        if server['protocol'] == 'Socks':
            outbound['settings']['servers'][0]['address'] = server['address']
            outbound['settings']['servers'][0]['port'] = server['port']
            if server['password'] is None or server['user'] is None:
                outbound['users'] = []
                outbound['users'].append({"user": "test user", server['user']: server['password'], "level": 0})
            else:
                if 'users' in outbound:
                    del outbound['users']
            return outbound
        if server['protocol'] == 'Vless':
            outbound['settings']['vnext'][0]['address'] = server['address']
            outbound['settings']['vnext'][0]['port'] = server['port']
            outbound['settings']['vnext'][0]['users'][0]['id'] = server['id']
            outbound['settings']['vnext'][0]['users'][0]['security'] = server['encryption']
            outbound['settings']['vnext'][0]['users'][0]['level'] = server['level']
            return outbound
        return outbound

    def editServers(self):
        print('edit server')
        self.app.editServersWindow.show()
