# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mw.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(515, 255)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_1.setFont(font)
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.verticalLayout.addWidget(self.label_1, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.calc_btn = QtWidgets.QPushButton(self.centralwidget)
        self.calc_btn.setMinimumSize(QtCore.QSize(0, 140))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.calc_btn.setFont(font)
        self.calc_btn.setObjectName("calc_btn")
        self.horizontalLayout.addWidget(self.calc_btn)
        self.change_btn = QtWidgets.QPushButton(self.centralwidget)
        self.change_btn.setMinimumSize(QtCore.QSize(0, 140))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.change_btn.setFont(font)
        self.change_btn.setObjectName("change_btn")
        self.horizontalLayout.addWidget(self.change_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 515, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_1.setText(_translate("MainWindow", "Correction of grating/detector shifts (Gonios)"))
        self.calc_btn.setText(_translate("MainWindow", "PushButton"))
        self.change_btn.setText(_translate("MainWindow", "PushButton"))
