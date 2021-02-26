from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu

from resources import Resources


class ServersMenu(QMenu):
    def __init__(self, app):
        super(ServersMenu, self).__init__()
        self.app = app
        self.serverActions = []

        for server in self.app.guiConfig.guiConfig['serverList']:
            self.serverActions.append(self.addAction(server['remarks']))
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

    def editServers(self):
        print('edit server')
        self.app.editServersWindow.show()
