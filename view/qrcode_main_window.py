from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from utils.resources import Resources
from .ui_about import Ui_AboutWindow
from .ui_qrcode import Ui_QRCodeMainWindow
import qrcode
import image
import base64


class QRCodeMainWindow(QMainWindow):
    def __init__(self, app):
        super(QRCodeMainWindow, self).__init__()
        self.app = app
        self.ui = Ui_QRCodeMainWindow()

        self.setWindowIcon(Resources.getIconByFilename('app.ico'))
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.init()

    def init(self, index=None):
        if index is None:
            index = self.app.guiConfig.guiConfig['settings']['selectedServerIndex']

        len_ = len(self.app.guiConfig.guiConfig['serverList'])
        print(f"debug 29 {len_ == 0}-{(len_ - 1) < index}")
        if len_ == 0 or (len_ - 1) < index:
            return ""

        url = self.serverToUrl(index)
        qrCodeImage: image = qrcode.make(url)
        qrCodeImage.save('hzj.qr')
        self.ui.qrcodeLabel.setScaledContents(True)
        self.ui.qrcodeLabel.setMaximumSize(QSize(400, 400))
        self.ui.urLabel.setMaximumSize(QSize(400, 400))
        self.ui.qrcodeLabel.setPixmap(QPixmap('hzj.qr'))
        self.ui.urLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.ui.urLabel.setText(url)
        self.ui.label.setText(self.app.guiConfig.guiConfig['serverList'][
            index]['remarks'])

    def serverToUrl(self, index):
        len_ = len(self.app.guiConfig.guiConfig['serverList'])
        print(f"debug 47 {len_ == 0}-{(len_-1) < index}")
        if len_ == 0 or (len_-1) < index:
            return ""
        server = self.app.guiConfig.guiConfig['serverList'][
                index]

        protocol = server['protocol']
        if protocol in 'Vmess':

            jsonStr = f'''
                  "v": "2",
                  "ps": "{server['remarks']}",
                  "add": "{server['address']}",
                  "port": "{server['port']}",
                  "id": "{server['id']}",
                  "aid": "{{server['alterId']}}",
                  "net": "tcp",
                  "type": "none",
                  "host": "",
                  "path": "",
                  "tls": ""
            '''
            baseSrt = base64.b64encode(bytes('{'+jsonStr+'}', encoding='utf-8'))
            return f"vmess://{str(baseSrt,encoding='utf-8')}"
        elif protocol in 'Shadowscoks':
            baseSrt = base64.b64encode(bytes(f"{server['method']}:{server['password']}@{server['address']}:"
                                             f"{server['port']}", encoding="utf-8"))
            return f"ss://{str(baseSrt,encoding='utf-8')}"
        elif protocol in 'Trojan':
            return f"trojan://{server['password']}@{server['address']}:{server['port']}"
        elif protocol in 'Socks':
            user = ""
            password = ""
            if server['user'] is not None and server['password'] is not None:
                user = server['user']
                password = server['password']
            baseStr = base64.b64encode(bytes(f"{user}:{password}@{server['address']}:{server['port']}", encoding="utf-8"))
            return f"socks://{str(baseStr, encoding='utf-8')}"
        return ""

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def show(self) -> None:
        self.init()
        super(QRCodeMainWindow, self).show()

    def show_(self, index) -> None:
        self.init(index)
        super(QRCodeMainWindow, self).show()
