# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\CodeHub\ProjectCloud\mainPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(620, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(620, 40, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(620, 70, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(620, 100, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(10, 10, 601, 541))
        self.treeWidget.setObjectName("treeWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "添加文件"))
        self.pushButton_3.setText(_translate("MainWindow", "注册全部"))
        self.pushButton_4.setText(_translate("MainWindow", "获取列表"))
        self.pushButton_5.setText(_translate("MainWindow", "下载全部"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "文件名"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "是否注册"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "是否本地保存"))
        self.treeWidget.headerItem().setText(3, _translate("MainWindow", "文件路径"))
        self.menu.setTitle(_translate("MainWindow", "额外选项"))
        self.action.setText(_translate("MainWindow", "打开仓库"))
        self.action.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_2.setText(_translate("MainWindow", "命令行模式"))
        self.action_2.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.action_3.setText(_translate("MainWindow", "视频模式"))
        self.action_3.setShortcut(_translate("MainWindow", "Ctrl+G"))
