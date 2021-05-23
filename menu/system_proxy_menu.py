from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu

from utils.utils import read_text_file
from utils.resources import Resources
from myos import sysproxy


class SystemProxyMenu(QMenu):
    def __init__(self, app):
        super(SystemProxyMenu, self).__init__()
        self.app = app
        self.guiConfig = self.app.guiConfig

        self.disableAction = self.addAction("Disable")
        self.PACAction = self.addAction("PAC")
        self.globalAction = self.addAction("Global")

        self.init()

        # 绑定信槽
        self.disableAction.triggered.connect(self.disableActionTriggered)
        self.PACAction.triggered.connect(self.PACActionTriggered)
        self.globalAction.triggered.connect(self.globalActionTriggered)

    def init(self):
        theme = self.app.guiConfig.guiConfig['settings']['theme']
        self.setStyleSheet(
            read_text_file(Resources.getResourcesPathByTheme(theme, 'menu'))
        )


        # 根据属性文件初始化菜单
        pros = self.app.strings.properties
        self.disableAction.setText(pros["disable"])
        self.PACAction.setText(pros["pac"])
        self.globalAction.setText(pros["global"])



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
        theme = self.app.guiConfig.guiConfig['settings']['theme']
        if self.guiConfig.guiConfig['systemProxy']['proxyMode'] in "Disable":
            self.disableAction.setIcon(Resources.getIconByThemeAndFilename(theme, "selected.png"))
            self.PACAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))
            self.globalAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))
            sysproxy.off()
        elif self.guiConfig.guiConfig['systemProxy']['proxyMode'] in "PAC":
            self.PACAction.setIcon(Resources.getIconByThemeAndFilename(theme, "selected.png"))
            self.globalAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))
            self.disableAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))
            sysproxy.setAutoProxyUrl(self.guiConfig.guiConfig['systemProxy']['scriptAddress'])
        elif self.guiConfig.guiConfig['systemProxy']['proxyMode'] in "Global":
            self.globalAction.setIcon(Resources.getIconByThemeAndFilename(theme, "selected.png"))
            self.PACAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))
            self.disableAction.setIcon(Resources.getIconByFilename('none_black_18dp.png'))
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
