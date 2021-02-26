from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QMessageBox

from resources import Resources
from view.transport_settings_dialog import TransportSettingsDialog
from view.ui_edit_server import Ui_EditServerWindow


class EditServersWindow(QMainWindow):
    def __init__(self, app):
        super(EditServersWindow, self).__init__()
        self.app = app
        self.guiConfig = self.app.guiConfig
        self.selectedServerIndex = self.guiConfig.guiConfig['settings']['selectedServerIndex']
        self.ui = Ui_EditServerWindow()
        self.vmessServer = {}
        self.vlessServer = {}
        self.shadowscoksServer = {}
        self.trojanServer = {}
        self.shadowscoksServer = {}
        self.setWindowIcon(Resources.getIconByFilename('app.ico'))
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.init()

    '''
        self.ui.addPushButton.
        self.ui.addFromLinkPushButton.
        self.ui.deletePushButton.
        self.ui.showQRCodePushButton.
        self.ui.sharPushButton.
    '''

    def init(self):
        # 根据配置文件初始化

        if len(self.guiConfig.guiConfig['serverList']) == 0:
            self.add()
        else:
            for serverDetail in self.guiConfig.guiConfig['serverList']:
                print(serverDetail)
                item = QListWidgetItem()
                item.setText(f"{serverDetail['remarks']}")
                item.setIcon(Resources.getIconByFilename('baseline_public_black_18dp.png'))
                self.ui.listWidget.addItem(item)

            self.ui.listWidget.setCurrentRow(self.selectedServerIndex)
            self.setServer(self.guiConfig.guiConfig['serverList'][self.selectedServerIndex])

        # 绑定信槽
        self.ui.addPushButton.clicked.connect(self.add)
        self.ui.addFromLinkPushButton.clicked.connect(self.addFromLink)
        self.ui.deletePushButton.clicked.connect(self.delete)
        self.ui.showQRCodePushButton.clicked.connect(self.showQRCode)
        self.ui.sharPushButton.clicked.connect(self.share)

        self.ui.listWidget.clicked.connect(self.listWidgetItemClicked)

        self.ui.protocolComboBox.currentIndexChanged.connect(self.setProtocol)
        self.ui.transportSettingsPushButton.clicked.connect(self.transportSettings)

        self.ui.savePushButton.clicked.connect(self.save)
        self.ui.cancelPushButton.clicked.connect(self.close)
        self.ui.resetPushButton.clicked.connect(self.reset)
        pass

    def add(self):
        if self.ui.listWidget.count() > 0:
            if not self.save():
                return
        remarks = "New Server"
        item = QListWidgetItem()
        item.setText(remarks)
        item.setIcon(Resources.getIconByFilename('baseline_public_black_18dp.png'))
        self.vmessServer = {"protocol": "Vmess", "remarks": remarks}
        self.setServer(self.vmessServer)
        self.ui.listWidget.addItem(item)
        self.ui.listWidget.setCurrentRow(len(self.guiConfig.guiConfig['serverList']))



    def addFromLink(self):
        print("add from link ......")

    def delete(self):
        if len(self.app.guiConfig.guiConfig['serverList']) == 0:
            self.informationBox("Delete", "Can't delete it.")
            return
        print(self.ui.listWidget.currentIndex().row())
        selectedIndex = self.ui.listWidget.currentIndex().row()
        item = self.ui.listWidget.item(selectedIndex)
        result = QMessageBox.information(
            self, "Delete", f"Are you sure delete {item.text()}.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if result == QMessageBox.Yes:
            if item.text() != 'New Server':
                print(f"Delete {self.app.guiConfig.guiConfig['serverList'][selectedIndex]}")
                del self.app.guiConfig.guiConfig['serverList'][selectedIndex]
                self.app.guiConfig.write()
            self.ui.listWidget.takeItem(selectedIndex)
            selectedIndex = self.ui.listWidget.currentIndex().row()

            if len(self.app.guiConfig.guiConfig['serverList']) > 0:
                self.setServer(self.app.guiConfig.guiConfig['serverList'][selectedIndex])
                return
            self.setServer(None)

    # 做一个输入监听否则一刷新就没了
    def listWidgetItemClicked(self):
        selectedServer = None
        if len(self.guiConfig.guiConfig['serverList']) == self.ui.listWidget.currentIndex().row():
            selectedServer = self.vmessServer
        else:
            selectedServer = self.guiConfig.guiConfig['serverList'][self.ui.listWidget.currentIndex().row()]
        self.setServer(selectedServer)
        print(f"selected {selectedServer}")

    def showQRCode(self):
        print("show QR code")

    def share(self):
        print("share")

    def save(self):
        protocol = self.ui.protocolComboBox.currentText()
        if protocol in 'Vmess':
            return self.saveVmessServer()
        elif protocol in 'Vless':
            return self.saveVlessServer()
        elif protocol in 'Shadowscoks':
            return self.saveShadowscoksServer()
        elif protocol in 'Trojan':
            return self.saveTrojanServer()
        elif protocol in 'Socks':
            return self.saveSocksServer()
        print("save....")

    def reset(self):
        server = self.guiConfig.guiConfig['serverList'][self.ui.listWidget.currentIndex().row()]
        self.setServer(server)
        print(f"rest {server}")

    def transportSettings(self):
        transportSettingsDialog = TransportSettingsDialog(self.app)
        transportSettingsDialog.exec_()

    def setProtocol(self):
        protocol = self.ui.protocolComboBox.currentText()
        print('protocol:' + protocol)
        if protocol in 'Vmess':
            self.setVmessServer()
        elif protocol in 'Vless':
            self.setVlessServer()
        elif protocol in 'Shadowscoks':
            self.setShadowscoksServer()
        elif protocol in 'Trojan':
            self.setTrojanServer()
        elif protocol in 'Socks':
            self.setSocksServer()

    def setServer(self, serverDetail):
        if serverDetail is None:
            serverDetail = {"protocol": "Vmess", "remarks": "New Server"}
            item = QListWidgetItem()
            item.setText(serverDetail['remarks'])
            self.ui.listWidget.addItem(item)

        protocol = serverDetail['protocol']
        currentIndex = 0

        self.ui.remakeLineEdit.setText(serverDetail['remarks'])

        if 'address' in serverDetail:
            self.ui.addressLineEdit.setText(serverDetail['address'])
        else:
            self.ui.addressLineEdit.setText("")

        if 'port' in serverDetail:
            self.ui.portLineEdit.setText(str(serverDetail['port']))
        else:
            self.ui.portLineEdit.setText("37192")

        if protocol in 'Vmess':
            currentIndex = 0
            self.setVmessServer()
            if 'id' in serverDetail:
                self.ui.UUIDLineEdit.setText(serverDetail['id'])
            else:
                self.ui.UUIDLineEdit.setText("")

            if 'alterId' in serverDetail:
                self.ui.alterIdLineEdit.setText(str(serverDetail['alterId']))
            else:
                self.ui.alterIdLineEdit.setText("")

            if 'encryption' in serverDetail:
                if serverDetail['encryption'] is None:
                    self.ui.securityComboBox_2.setCurrentIndex(3)
                elif 'auto' in serverDetail['encryption']:
                    self.ui.securityComboBox_2.setCurrentIndex(0)
                elif 'aes-128-gcm' in serverDetail['encryption']:
                    self.ui.securityComboBox_2.setCurrentIndex(1)
                elif 'chacha20-poly1305' in serverDetail['encryption']:
                    self.ui.securityComboBox_2.setCurrentIndex(2)
            else:
                self.ui.securityComboBox_2.setCurrentIndex(1)

            if 'level' in serverDetail:
                self.ui.levelLineEdit.setText(str(serverDetail['level']))
            else:
                self.ui.levelLineEdit.setText("")
        elif protocol in 'Vless':
            currentIndex = 1
            self.setVlessServer()
            if 'id' in serverDetail:
                self.ui.UUIDLineEdit.setText(serverDetail['id'])
            else:
                self.ui.UUIDLineEdit.setText("")

            if 'encryption' in serverDetail:
                if serverDetail['encryption'] is None:
                    self.ui.securityComboBox_2.setCurrentIndex(3)
                elif 'auto' in serverDetail['encryption']:
                    self.ui.securityComboBox_2.setCurrentIndex(0)
                elif 'aes-128-gcm' in serverDetail['encryption']:
                    self.ui.securityComboBox_2.setCurrentIndex(1)
                elif 'chacha20-poly1305' in serverDetail['encryption']:
                    self.ui.securityComboBox_2.setCurrentIndex(2)
            else:
                self.ui.securityComboBox_2.setCurrentIndex(1)

            if 'level' in serverDetail:
                self.ui.levelLineEdit.setText(str(serverDetail['level']))
            else:
                self.ui.levelLineEdit.setText("")
        elif protocol in 'Shadowscoks':
            currentIndex = 3
            self.setShadowscoksServer()
            if 'password' in serverDetail:
                self.ui.passwordLineEdit.setText(serverDetail['password'])
            else:
                self.ui.passwordLineEdit.setText("")

            if 'method' in serverDetail:
                if 'aes-256-cfb' in serverDetail['method']:
                    self.ui.methodComboBox.setCurrentIndex(0)
                elif 'aes-128-cfb' in serverDetail['method']:
                    self.ui.methodComboBox.setCurrentIndex(1)
                elif 'chacha20' in serverDetail['method']:
                    self.ui.methodComboBox.setCurrentIndex(2)
                elif 'chacha20-ietf' in serverDetail['method']:
                    self.ui.methodComboBox.setCurrentIndex(3)
                elif 'aes-256-gcm' in serverDetail['method']:
                    self.ui.methodComboBox.setCurrentIndex(4)
                elif 'aes-128-gcm' in serverDetail['method']:
                    self.ui.methodComboBox.setCurrentIndex(5)
                elif 'chacha20-poly1305' in serverDetail['method']:
                    self.ui.methodComboBox.setCurrentIndex(6)
                elif 'chacha20-ietf-poly1305' in serverDetail['method']:
                    self.ui.methodComboBox.setCurrentIndex(7)
            else:
                self.ui.methodComboBox.setCurrentIndex(0)
        elif protocol in 'Trojan':
            currentIndex = 2
            self.setTrojanServer()
            if 'password' in serverDetail:
                self.ui.passwordLineEdit.setText(serverDetail['password'])
            else:
                self.ui.passwordLineEdit.setText("")

            if 'host' in serverDetail or serverDetail['host'] is None:
                self.ui.hostLineEdit.setText(serverDetail['host'])
            else:
                self.ui.hostLineEdit.setText("")

        elif protocol in 'Socks':
            currentIndex = 4
            self.setSocksServer()

            if 'password' in serverDetail or serverDetail['password'] is None:
                self.ui.passwordLineEdit.setText(serverDetail['password'])
            else:
                self.ui.passwordLineEdit.setText("")

            if 'user' in serverDetail or serverDetail['user'] is None:
                self.ui.userLineEdit.setText(serverDetail['user'])
            else:
                self.ui.userLineEdit.setText("")

        self.ui.protocolComboBox.setCurrentIndex(currentIndex)
        self.ui.remakeLineEdit.setText(serverDetail['remarks'])

    def setVmessServer(self):
        self.ui.frame_17.setVisible(True)
        self.ui.frame_18.setVisible(True)
        self.ui.alterIdLineEdit.setVisible(True)
        self.ui.alterIdLabel.setVisible(True)
        self.ui.frame_19.setVisible(False)
        self.ui.flowLabel.setVisible(False)
        self.ui.flowComboBox.setVisible(False)
        self.ui.frame_16.setVisible(False)
        self.ui.frame_3.setVisible(False)
        self.ui.frame_4.setVisible(False)
        self.ui.portLineEdit.setText("37192")
        self.ui.transportSettingsPushButton.setVisible(True)

    def setVlessServer(self):
        self.ui.frame_17.setVisible(True)
        self.ui.frame_18.setVisible(True)
        self.ui.frame_19.setVisible(False)
        self.ui.alterIdLineEdit.setVisible(False)
        self.ui.alterIdLabel.setVisible(False)
        self.ui.flowLabel.setVisible(True)
        self.ui.flowComboBox.setVisible(True)
        self.ui.frame_16.setVisible(False)
        self.ui.frame_3.setVisible(False)
        self.ui.frame_4.setVisible(False)
        self.ui.portLineEdit.setText("443")
        self.ui.securityLabel_2.setText("Encryption")
        self.ui.transportSettingsPushButton.setVisible(True)

    def setShadowscoksServer(self):
        self.ui.frame_17.setVisible(False)
        self.ui.frame_18.setVisible(False)
        self.ui.frame_19.setVisible(False)
        self.ui.frame_16.setVisible(False)
        self.ui.frame_3.setVisible(True)
        self.ui.frame_4.setVisible(True)
        self.ui.passwordLabel.setText("Password")
        self.ui.portLineEdit.setText("8388")
        self.ui.methodLabel.setText("Encryption Method")
        self.ui.otaLabel.setVisible(False)
        self.ui.otaComboBox.setVisible(False)
        self.ui.methodComboBox.setCurrentIndex(6)
        self.ui.transportSettingsPushButton.setVisible(False)

    def setTrojanServer(self):
        self.ui.frame_17.setVisible(False)
        self.ui.frame_18.setVisible(False)
        self.ui.frame_19.setVisible(True)
        self.ui.frame_16.setVisible(False)
        self.ui.frame_3.setVisible(True)
        self.ui.frame_4.setVisible(False)
        self.ui.passwordLabel.setText("Password")
        self.ui.portLineEdit.setText("443")
        self.ui.transportSettingsPushButton.setVisible(False)

    def setSocksServer(self):
        self.ui.frame_17.setVisible(False)
        self.ui.frame_18.setVisible(False)
        self.ui.frame_19.setVisible(False)
        self.ui.frame_16.setVisible(True)
        self.ui.frame_3.setVisible(True)
        self.ui.frame_4.setVisible(False)
        self.ui.userLabel.setText("Username (Optional)")
        self.ui.passwordLabel.setText("Password (Optional)")
        self.ui.portLineEdit.setText("1080")
        self.ui.transportSettingsPushButton.setVisible(False)

    def addServer(self):
        pass

    def saveVmessServer(self):
        self.vmessServer = {
            "protocol": self.ui.protocolComboBox.currentText(),
            "remarks": self.ui.remakeLineEdit.text(),
            "address": self.ui.addressLineEdit.text(),
            "port": self.ui.portLineEdit.text(),
            "id": self.ui.UUIDLineEdit.text(),
            "alterId": self.ui.alterIdLineEdit.text(),
            "encryption": self.ui.securityComboBox_2.currentText(),
            "level": self.ui.levelLineEdit.text()
        }

        if self.vmessServer['encryption'].strip() == 'none':
            self.vmessServer['encryption'] = None

        if self.vmessServer['address'].strip() == '':
            print("Server address invalid")
            self.informationBox('Info', "Server address invalid.")
            return False

        if self.vmessServer['port'].strip() == '':
            print("Server port invalid")
            self.informationBox('Info', "Server port invalid.")
            return False
        try:
            self.vmessServer['port'] = int(self.vmessServer['port'].strip())
        except BaseException:
            print("Server port invalid")
            self.informationBox('Info', "Server port invalid.")
            return False

        if self.vmessServer['id'].strip() == '':
            print("Server id invalid")
            self.informationBox('Info', "Server id invalid")
            return False

        if self.vmessServer['alterId'].strip() == '':
            print("Server alterId invalid")
            self.informationBox('info', "Server alterId invalid.")
            return False

        try:
            self.vmessServer['alterId'] = int(self.vmessServer['alterId'].strip())
        except BaseException:
            print("Server alterId invalid")
            self.informationBox('Info', "Server alterId invalid.")
            return False

        if self.vmessServer['level'].strip() == '':
            print("Server level invalid")
            self.informationBox('Info', "Server level invalid.")
            return False

        try:
            self.vmessServer['level'] = int(self.vmessServer['level'].strip())
        except BaseException:
            print("Server level invalid")
            self.informationBox('Info', "Server level invalid.")
            return False

        if self.vmessServer['id'].strip() == '':
            print("Server id invalid")
            self.informationBox('Info', "Server id invalid")
            return False

        if self.vmessServer['remarks'] in "New Server":
            self.vmessServer['remarks'] = f"{self.vmessServer['address']}:{self.vmessServer['port']}"

        self.ui.remakeLineEdit.setText(self.vmessServer['remarks'])
        self.ui.listWidget.item(self.ui.listWidget.currentIndex().row()).setText(self.vmessServer['remarks'])
        if len(self.guiConfig.guiConfig['serverList']) == self.ui.listWidget.currentIndex().row():
            self.guiConfig.guiConfig['serverList'].append(self.vmessServer)
        else:
            self.guiConfig.guiConfig['serverList'][self.ui.listWidget.currentIndex().row()] = self.vmessServer
        self.guiConfig.write()
        print("save " + str(self.vmessServer))
        self.vmessServer = {}
        return True

    def saveVlessServer(self):
        self.vlessServer = {
            "protocol": self.ui.protocolComboBox.currentText(),
            "remarks": self.ui.remakeLineEdit.text(),
            "address": self.ui.addressLineEdit.text(),
            "port": self.ui.portLineEdit.text(),
            "id": self.ui.UUIDLineEdit.text(),
            "encryption": self.ui.securityComboBox_2.currentText(),
            "level": self.ui.levelLineEdit.text()
        }

        if self.vlessServer['encryption'].strip() == 'none':
            self.vlessServer['encryption'] = None

        if self.vlessServer['address'].strip() == '':
            print("Server address invalid")
            self.informationBox('Info', "Server address invalid.")
            return False

        if self.vlessServer['port'].strip() == '':
            print("Server port invalid")
            self.informationBox('Info', "Server port invalid.")
            return False
        try:
            self.vlessServer['port'] = int(self.vlessServer['port'].strip())
        except BaseException:
            print("Server port invalid")
            self.informationBox('Info', "Server port invalid.")
            return False

        if self.vlessServer['id'].strip() == '':
            print("Server id invalid")
            self.informationBox('Info', "Server id invalid")
            return False


        if self.vlessServer['level'].strip() == '':
            print("Server level invalid")
            self.informationBox('Info', "Server level invalid.")
            return False

        try:
            self.vlessServer['level'] = int(self.vlessServer['level'].strip())
        except BaseException:
            print("Server level invalid")
            self.informationBox('Info', "Server level invalid.")
            return False

        if self.vlessServer['  '].strip() == '':
            print("Server id invalid")
            self.informationBox('Info', "Server id invalid")
            return False

        if self.vlessServer['remarks'] in "New Server":
            self.vlessServer['remarks'] = f"{self.vlessServer['address']}:{self.vlessServer['port']}"

        self.ui.remakeLineEdit.setText(self.vlessServer['remarks'])
        self.ui.listWidget.item(self.ui.listWidget.currentIndex().row()).setText(self.vlessServer['remarks'])
        if len(self.guiConfig.guiConfig['serverList']) == self.ui.listWidget.currentIndex().row():
            self.guiConfig.guiConfig['serverList'].append(self.vlessServer)
        else:
            self.guiConfig.guiConfig['serverList'][self.ui.listWidget.currentIndex().row()] = self.vlessServer
        self.guiConfig.write()
        print("save " + str(self.vlessServer))
        self.vlessServer = {}
        return True


    def saveShadowscoksServer(self):

        self.shadowscoksServer = {
            "protocol": self.ui.protocolComboBox.currentText(),
            "remarks": self.ui.remakeLineEdit.text(),
            "address": self.ui.addressLineEdit.text(),
            "port": self.ui.portLineEdit.text(),
            "password": self.ui.passwordLineEdit.text(),
            "method": self.ui.methodComboBox.currentText(),
        }


        print(f"debug {self.ui.methodComboBox.currentText()}")
        if self.shadowscoksServer['address'].strip() == '':
            print("Server address invalid")
            self.informationBox('Info', "Server address invalid.")
            return False

        if self.shadowscoksServer['port'].strip() == '':
            print("Server port invalid")
            self.informationBox('Info', "Server port invalid.")
            return False
        try:
            self.shadowscoksServer['port'] = int(self.shadowscoksServer['port'].strip())
        except BaseException:
            print("Server port invalid")
            self.informationBox('Info', "Server port invalid.")
            return False

        if self.shadowscoksServer['password'].strip() == '':
            print("Server password invalid")
            self.informationBox('Info', "Server password invalid.")
            return False

        if self.shadowscoksServer['remarks'] in "New Server":
            self.shadowscoksServer['remarks'] = f"{self.shadowscoksServer['address']}:{self.shadowscoksServer['port']}"

        self.ui.remakeLineEdit.setText(self.shadowscoksServer['remarks'])
        self.ui.listWidget.item(self.ui.listWidget.currentIndex().row()).setText(self.shadowscoksServer['remarks'])

        if len(self.guiConfig.guiConfig['serverList']) == self.ui.listWidget.currentIndex().row():
            self.guiConfig.guiConfig['serverList'].append(self.shadowscoksServer)
        else:
            self.guiConfig.guiConfig['serverList'][self.ui.listWidget.currentIndex().row()] = self.shadowscoksServer
        self.guiConfig.write()
        print("save " + str(self.shadowscoksServer))
        self.shadowscoksServer = {}
        return True

    # Trojan
    def saveTrojanServer(self):

        self.trojanServer = {
            "protocol": self.ui.protocolComboBox.currentText(),
            "remarks": self.ui.remakeLineEdit.text(),
            "address": self.ui.addressLineEdit.text(),
            "port": self.ui.portLineEdit.text(),
            "password": self.ui.passwordLineEdit.text(),
            "host": self.ui.hostLineEdit.text(),
        }

        if self.trojanServer['address'].strip() == '':
            print("Server address invalid")
            self.informationBox('Info', "Server address invalid.")
            return False

        if self.trojanServer['port'].strip() == '':
            print("Server port invalid")
            self.informationBox('Info', "Server port invalid.")
            return False
        try:
            self.trojanServer['port'] = int(self.trojanServer['port'].strip())
        except BaseException:
            print("Server port invalid")
            self.informationBox('Info', "Server port invalid.")
            return False

        if self.trojanServer['password'].strip() == '':
            print("Server password invalid")
            self.informationBox('Info', "Server password invalid.")
            return False

        if self.trojanServer['host'].strip() == '':
            self.trojanServer['host'] = None

        if self.trojanServer['remarks'] in "New Server":
            self.trojanServer['remarks'] = f"{self.trojanServer['address']}:{self.trojanServer['port']}"

        self.ui.remakeLineEdit.setText(self.trojanServer['remarks'])
        self.ui.listWidget.item(self.ui.listWidget.currentIndex().row()).setText(self.trojanServer['remarks'])

        if len(self.guiConfig.guiConfig['serverList']) == self.ui.listWidget.currentIndex().row():
            self.guiConfig.guiConfig['serverList'].append(self.trojanServer)
        else:
            self.guiConfig.guiConfig['serverList'][self.ui.listWidget.currentIndex().row()] = self.trojanServer
        self.guiConfig.write()
        print("save " + str(self.trojanServer))
        self.trojanServer = {}
        return True

    def saveSocksServer(self):

        self.socksServer = {
            "protocol": self.ui.protocolComboBox.currentText(),
            "remarks": self.ui.remakeLineEdit.text(),
            "address": self.ui.addressLineEdit.text(),
            "port": self.ui.portLineEdit.text(),
            "password": self.ui.passwordLineEdit.text(),
            "user": self.ui.userLineEdit.text(),
        }

        if self.socksServer['address'].strip() == '':
            print("Server address invalid")
            self.informationBox('Info', "Server address invalid.")
            return False

        if self.socksServer['port'].strip() == '':
            print("Server port invalid")
            self.informationBox('Info', "Server port invalid.")
            return False
        try:
            self.socksServer['port'] = int(self.socksServer['port'].strip())
        except BaseException:
            print("Server port invalid")
            self.informationBox('Info', "Server port invalid.")
            return False

        if self.socksServer['password'].strip() == '':
            self.socksServer['password'] = None

        if self.socksServer['user'].strip() == '':
            self.socksServer['user'] = None

        if self.socksServer['remarks'] in "New Server":
            self.socksServer['remarks'] = f"{self.socksServer['address']}:{self.socksServer['port']}"

        self.ui.remakeLineEdit.setText(self.socksServer['remarks'])
        self.ui.listWidget.item(self.ui.listWidget.currentIndex().row()).setText(self.socksServer['remarks'])

        if len(self.guiConfig.guiConfig['serverList']) == self.ui.listWidget.currentIndex().row():
            self.guiConfig.guiConfig['serverList'].append(self.socksServer)
        else:
            self.guiConfig.guiConfig['serverList'][self.ui.listWidget.currentIndex().row()] = self.socksServer
        self.guiConfig.write()
        print("save " + str(self.socksServer))
        self.socksServer = {}
        return True

    def informationBox(self, title, text):
        informationMessageBox = QMessageBox(self)
        informationMessageBox.setWindowIcon(Resources.getIconByFilename('app.ico'))
        informationMessageBox.setWindowTitle(title)
        informationMessageBox.setIcon(QMessageBox.Information)
        informationMessageBox.setText(text)
        informationMessageBox.exec()
        return

    def closeEvent(self, event):
        self.hide()
        event.ignore()
