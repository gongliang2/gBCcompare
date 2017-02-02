# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gBCcompare.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 86)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hLayout1 = QtWidgets.QHBoxLayout()
        self.hLayout1.setObjectName("hLayout1")
        self.pb_compare = QtWidgets.QPushButton(self.centralwidget)
        self.pb_compare.setMaximumSize(QtCore.QSize(80, 28))
        self.pb_compare.setObjectName("pb_compare")
        self.hLayout1.addWidget(self.pb_compare)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMaximumSize(QtCore.QSize(80, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.hLayout1.addWidget(self.pushButton_2)
        self.pb_next = QtWidgets.QPushButton(self.centralwidget)
        self.pb_next.setMaximumSize(QtCore.QSize(80, 28))
        self.pb_next.setObjectName("pb_next")
        self.hLayout1.addWidget(self.pb_next)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hLayout1.addItem(spacerItem)
        self.verticalLayout.addLayout(self.hLayout1)
        self.hLayout2 = QtWidgets.QHBoxLayout()
        self.hLayout2.setObjectName("hLayout2")
        self.verticalLayout.addLayout(self.hLayout2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pb_compare.setText(_translate("MainWindow", "compare"))
        self.pushButton_2.setText(_translate("MainWindow", "last Diff"))
        self.pb_next.setText(_translate("MainWindow", "next Diff"))

