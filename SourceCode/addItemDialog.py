# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\CodeHub\ProjectCloud\PageUI\addItemDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(446, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setObjectName("label_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_1)
        self.fileName = QtWidgets.QLineEdit(Dialog)
        self.fileName.setObjectName("fileName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fileName)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.choosePath = QtWidgets.QPushButton(Dialog)
        self.choosePath.setObjectName("choosePath")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.choosePath)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.addtionText = QtWidgets.QTextEdit(Dialog)
        self.addtionText.setObjectName("addtionText")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.addtionText)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.needRegister = QtWidgets.QCheckBox(Dialog)
        self.needRegister.setText("")
        self.needRegister.setObjectName("needRegister")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.needRegister)
        self.horizontalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.label_1.setBuddy(self.fileName)
        self.label_2.setBuddy(self.choosePath)
        self.label_3.setBuddy(self.addtionText)
        self.label_4.setBuddy(self.needRegister)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_1.setText(_translate("Dialog", "文件名"))
        self.label_2.setText(_translate("Dialog", "文件路径"))
        self.choosePath.setText(_translate("Dialog", "..."))
        self.label_3.setText(_translate("Dialog", "文件说明"))
        self.label_4.setText(_translate("Dialog", "是否需要注册"))
