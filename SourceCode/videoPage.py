# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\CodeHub\CoLoRagent\PageUI\videoPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/color"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.videoView = QtWidgets.QWidget(self.splitter)
        self.videoView.setObjectName("videoView")
        self.channel = QtWidgets.QListView(self.splitter)
        self.channel.setObjectName("channel")
        self.verticalLayout.addWidget(self.splitter)
        self.videoSlider = QtWidgets.QSlider(self.centralwidget)
        self.videoSlider.setOrientation(QtCore.Qt.Horizontal)
        self.videoSlider.setObjectName("videoSlider")
        self.verticalLayout.addWidget(self.videoSlider)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.time_lcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.time_lcd.setObjectName("time_lcd")
        self.horizontalLayout.addWidget(self.time_lcd)
        self.back_10 = QtWidgets.QPushButton(self.centralwidget)
        self.back_10.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/button/control-skip-f"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_10.setIcon(icon1)
        self.back_10.setObjectName("back_10")
        self.horizontalLayout.addWidget(self.back_10)
        self.playOrPause = QtWidgets.QPushButton(self.centralwidget)
        self.playOrPause.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/button/control-play"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playOrPause.setIcon(icon2)
        self.playOrPause.setObjectName("playOrPause")
        self.horizontalLayout.addWidget(self.playOrPause)
        self.forward_10 = QtWidgets.QPushButton(self.centralwidget)
        self.forward_10.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/button/control-skip-b"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.forward_10.setIcon(icon3)
        self.forward_10.setObjectName("forward_10")
        self.horizontalLayout.addWidget(self.forward_10)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.volumn_mute = QtWidgets.QPushButton(self.centralwidget)
        self.volumn_mute.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/button/volume-mute"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.volumn_mute.setIcon(icon4)
        self.volumn_mute.setObjectName("volumn_mute")
        self.horizontalLayout.addWidget(self.volumn_mute)
        self.volumnSlider = QtWidgets.QSlider(self.centralwidget)
        self.volumnSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumnSlider.setObjectName("volumnSlider")
        self.horizontalLayout.addWidget(self.volumnSlider)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        self.open_local = QtWidgets.QAction(MainWindow)
        self.open_local.setObjectName("open_local")
        self.open_service = QtWidgets.QAction(MainWindow)
        self.open_service.setObjectName("open_service")
        self.menu.addAction(self.open_local)
        self.menu.addAction(self.open_service)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "视频通信"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.open_local.setText(_translate("MainWindow", "打开本地文件"))
        self.open_service.setText(_translate("MainWindow", "打开频道"))
import resource_rc
