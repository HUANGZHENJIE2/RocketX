# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/feedback.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from utils.resources import Resources


class Ui_Feedback(object):
    def setupUi(self, Feedback):
        Feedback.setObjectName("Feedback")
        Feedback.resize(534, 534)
        self.centralwidget = QtWidgets.QWidget(Feedback)
        self.centralwidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.discriptionLabel = QtWidgets.QLabel(self.centralwidget)
        self.discriptionLabel.setObjectName("discriptionLabel")
        self.verticalLayout.addWidget(self.discriptionLabel)
        self.imgLabel = QtWidgets.QLabel(self.centralwidget)
        self.imgLabel.setText("")
        self.imgLabel.setPixmap(QtGui.QPixmap(Resources.getQPixmapByFilename("my_wechat_qrcode.jpg")))
        self.imgLabel.setObjectName("imgLabel")
        self.verticalLayout.addWidget(self.imgLabel)
        Feedback.setCentralWidget(self.centralwidget)

        self.retranslateUi(Feedback)
        QtCore.QMetaObject.connectSlotsByName(Feedback)

    def retranslateUi(self, Feedback):
        _translate = QtCore.QCoreApplication.translate
        Feedback.setWindowTitle(_translate("Feedback", "Feedback"))
        self.discriptionLabel.setText(_translate("Feedback", "<html><head/><body><p><span style=\" font-family:\'system-ui,sans-serif\'; font-size:x-large; font-weight:600; color:#262626;\">My QR Code</span></p><p><span style=\" font-family:\'system-ui,sans-serif\'; font-size:14px; color:#262626; background-color:#f7f7f7;\">San the QR code to add me on WeChat.</span></p></body></html>"))

