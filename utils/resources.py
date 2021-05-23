import os
from PyQt5.QtGui import QIcon, QPixmap
import sys
import platform



class Resources:
    @staticmethod
    def getBaseResourcesPath():
        return os.path.join(os.getcwd(), "resources")

    @staticmethod
    def getLibPath(path):
        return os.path.join(os.getcwd(), "lib", platform.system(), path)

    @staticmethod
    def getResourcesPath(path):
        return os.path.join(Resources.getBaseResourcesPath(), path)

    @staticmethod
    def getResourcesPathByTheme(theme, path):
        return os.path.join(Resources.getBaseResourcesPath(), "themes", theme, path)

    @staticmethod
    def getResourcesPackagesPath(path):
        return os.path.join(os.getcwd(), ".packages", path)

    @staticmethod
    def getIconByFilename(filename):
        return QIcon(Resources.getResourcesPath(filename))

    @staticmethod
    def getIconByThemeAndFilename(theme, filename):
        print(Resources.getResourcesPathByTheme(theme, filename))
        return QIcon(Resources.getResourcesPathByTheme(theme, filename))

    @staticmethod
    def getBasePath(path):
        return os.path.join(os.getcwd(), path)



    @staticmethod
    def getQPixmapByFilename(filename):
        return QPixmap(Resources.getResourcesPath(filename))

    @staticmethod
    def getConfigPath(path):
        return os.path.join(os.getcwd(), "config", path)



    @staticmethod
    def getValuesPath(path):
        return os.path.join(os.getcwd(), ".values", path)
