import os
from PyQt5.QtGui import QIcon, QPixmap


class Resources:
    @staticmethod
    def getBaseResourcesPath():
        return os.getcwd() + "\\res"

    @staticmethod
    def getLibPath():
        return os.getcwd() + "\\lib"

    @staticmethod
    def getResourcesPath(path):
        return Resources.getBaseResourcesPath() + "\\" + path

    @staticmethod
    def getIconByFilename(filename):
        return QIcon(Resources.getResourcesPath(filename))

    @staticmethod
    def getBasePath(path):
        return os.getcwd() + "\\" + path

    @staticmethod
    def getQPixmapByFilename(filename):
        return QPixmap(Resources.getResourcesPath(filename))

    @staticmethod
    def getConfigPath(path):
        return os.getcwd() + "\\config\\" + path

    @staticmethod
    def getValuesPath(path):
        return os.getcwd() + "\\values\\" + path
