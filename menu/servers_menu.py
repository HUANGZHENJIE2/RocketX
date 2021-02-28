from functools import partial

import pyperclip as pyperclip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu

import utils
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
        self.showServerQRCodeAction = self.addAction("Show selected server QR code")

        self.init()

    def init(self):
        self.setStyleSheet(
            utils.read_text_file(Resources.getResourcesPackagesPath('menu'))
        )

        pros = self.app.strings.properties
        self.editServersAction.setText(pros["editServers"])
        self.importServerFromUrlAction.setText(pros["importServerFromUrl"])
        self.copySelectedServerUrlAction.setText(pros["copySelectedServerUrlAction"])
        self.showServerQRCodeAction.setText(pros["showServerQRCode"])

        if len(self.app.guiConfig.guiConfig['serverList']) > 0:
            if self.app.guiConfig.guiConfig['settings']['selectedServerIndex'] > \
                    (len(self.app.guiConfig.guiConfig['serverList']) - 1):
                self.app.guiConfig.guiConfig['settings']['selectedServerIndex'] = 0
                self.app.guiConfig.write()
                self.app.systemTrayIconContextMenu.disconnectServer()
                self.app.systemTrayIcon.showMessage(pros["reset"], pros['resetSelectedIndex'])
                self.setServer(self.app.guiConfig.guiConfig['settings']['selectedServerIndex'])
                self.app.systemTrayIconContextMenu.connectServer()
            self.serverActions[self.app.guiConfig.guiConfig['settings']['selectedServerIndex']] \
                .setIcon(Resources.getIconByFilename('baseline_check_black_18dp.png'))

        self.editServersAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))

        self.showServerQRCodeAction.triggered.connect(self.showServerQRCode)
        self.editServersAction.triggered.connect(self.editServers)
        self.importServerFromUrlAction.triggered.connect(self.importServerFromUrl)
        self.copySelectedServerUrlAction.triggered.connect(self.copySelectedServerUrl)

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

    def importServerFromUrl(self):
        self.app.editServersWindow.show()
        self.app.editServersWindow.addFromLink()

    def copySelectedServerUrl(self):
        pros = self.app.strings.properties
        url = self.app.qrcodeMainWindow.serverToUrl(self.app.guiConfig.guiConfig['settings']['selectedServerIndex'])
        pyperclip.copy(url)
        print(f"copy url {url}")
        self.app.systemTrayIcon.showMessage(pros['appName'], pros['copyUrl'].replace("{0}", ""),
                                            Resources.getIconByFilename('app.ico'))

    def showServerQRCode(self):
        self.app.qrcodeMainWindow.show()

    def editServers(self):
        print('edit server')
        self.app.editServersWindow.show()


