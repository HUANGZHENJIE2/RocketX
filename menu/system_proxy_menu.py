from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu

from resources import Resources
import sysproxy


class SystemProxyMenu(QMenu):
    def __init__(self, app):
        super(SystemProxyMenu, self).__init__()
        self.app = app
        self.guiConfig = self.app.guiConfig

        self.disableAction = self.addAction("Disable")
        self.PACAction = self.addAction("PAC")
        self.globalAction = self.addAction("Global")

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
        self.setSystemProxyModelIcon()

        # 根据属性文件初始化菜单
        pros = self.app.strings.properties
        self.disableAction.setText(pros["disable"])
        self.PACAction.setText(pros["pac"])
        self.globalAction.setText(pros["global"])

        # 绑定信槽
        self.disableAction.triggered.connect(self.disableActionTriggered)
        self.PACAction.triggered.connect(self.PACActionTriggered)
        self.globalAction.triggered.connect(self.globalActionTriggered)

    def disableActionTriggered(self):
        self.guiConfig.guiConfig['systemProxy']['proxyMode'] = "Disable"
        self.guiConfig.write()
        self.setSystemProxyModelIcon()

    def PACActionTriggered(self):
        self.guiConfig.guiConfig['systemProxy']['proxyMode'] = "PAC"
        self.guiConfig.write()
        self.setSystemProxyModelIcon()

    def globalActionTriggered(self):
        self.guiConfig.guiConfig['systemProxy']['proxyMode'] = "Global"
        self.guiConfig.write()
        self.setSystemProxyModelIcon()

    def setSystemProxyModelIcon(self):
        if self.guiConfig.guiConfig['systemProxy']['proxyMode'] in "Disable":
            self.disableAction.setIcon(Resources.getIconByFilename('baseline_check_black_18dp.png'))
            self.PACAction.setIcon(Resources.getIconByFilename('hzj'))
            self.globalAction.setIcon(Resources.getIconByFilename('hzj'))
            sysproxy.off()
        elif self.guiConfig.guiConfig['systemProxy']['proxyMode'] in "PAC":
            self.PACAction.setIcon(Resources.getIconByFilename('baseline_check_black_18dp.png'))
            self.globalAction.setIcon(Resources.getIconByFilename('hzj'))
            self.disableAction.setIcon(Resources.getIconByFilename('hzj'))
            sysproxy.setAutoProxyUrl(self.guiConfig.guiConfig['systemProxy']['scriptAddress'])
        elif self.guiConfig.guiConfig['systemProxy']['proxyMode'] in "Global":
            self.globalAction.setIcon(Resources.getIconByFilename('baseline_check_black_18dp.png'))
            self.PACAction.setIcon(Resources.getIconByFilename('hzj'))
            self.disableAction.setIcon(Resources.getIconByFilename('hzj'))
            sysproxy.setWebProxy(f"{self.guiConfig.guiConfig['systemProxy']['proxyAddress']}:"
                                 f"{self.guiConfig.guiConfig['systemProxy']['proxyPort']}",
                                 self.guiConfig.guiConfig['systemProxy']['proxyOverride'])

    def setDisabledProxy(self):
        if self.guiConfig.guiConfig['systemProxy']['proxyMode'] not in "Disable":
            self.disableAction.setIcon(Resources.getIconByFilename('baseline_check_black_18dp.png'))
            self.PACAction.setIcon(Resources.getIconByFilename('hzj'))
            self.globalAction.setIcon(Resources.getIconByFilename('hzj'))
            sysproxy.off()

    def setEnabledProxy(self):
        self.setSystemProxyModelIcon()
