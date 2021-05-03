import os
from PyQt5.QtGui import QIcon, QPixmap
import sys
import platform

class Resources:
    @staticmethod
    def getBaseResourcesPath():
        if sys.platform in 'win32':
            return os.getcwd() + "\\resources"
        return os.getcwd() + "/resources"

    @staticmethod
    def getLibPath(path):
        osname = platform.system()
        if sys.platform in 'win32':
            return os.getcwd() + "\\lib\\" + osname + "\\" + path
        return os.getcwd() + "/lib/" + osname + '/' + path

    @staticmethod
    def getResourcesPath(path):
        if sys.platform in 'win32':
            return Resources.getBaseResourcesPath() + "\\" + path
        return Resources.getBaseResourcesPath() + "/" + path

    @staticmethod
    def getResourcesPackagesPath(path):
        if sys.platform in 'win32':
            return os.getcwd() + "\\.packages\\" + path
        return os.getcwd() + "/.packages/" + path

    @staticmethod
    def getIconByFilename(filename):
        return QIcon(Resources.getResourcesPath(filename))

    @staticmethod
    def getBasePath(path):
        if sys.platform in 'win32':
            return os.getcwd() + "\\" + path
        return os.getcwd() + "/" + path

    @staticmethod
    def getQPixmapByFilename2(filename, theme):
        if sys.platform in 'win32':
            return QPixmap(Resources.getResourcesPath(f"themes\\{theme}\\"+filename))
        return QPixmap(Resources.getResourcesPath(f"themes/{theme}/" + filename))


    @staticmethod
    def getQPixmapByFilename(filename):
        return QPixmap(Resources.getResourcesPath(filename))

    @staticmethod
    def getConfigPath(path):
        if sys.platform in 'win32':
            return os.getcwd() + "\\config\\" + path
        return os.getcwd() + "/config/" + path

    @staticmethod
    def getValuesPath(path):
        if sys.platform in 'win32':
            return os.getcwd() + "\\.values\\" + path
        return os.getcwd() + "/.values/" + path
