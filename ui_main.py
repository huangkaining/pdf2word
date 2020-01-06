# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TextResult = QtWidgets.QTextBrowser(self.centralwidget)
        self.TextResult.setGeometry(QtCore.QRect(320, 20, 461, 531))
        self.TextResult.setObjectName("TextResult")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 20, 301, 241))
        self.groupBox_2.setObjectName("groupBox_2")
        self.LabelFile = QtWidgets.QLabel(self.groupBox_2)
        self.LabelFile.setGeometry(QtCore.QRect(10, 30, 271, 51))
        self.LabelFile.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.LabelFile.setObjectName("LabelFile")
        self.btnUploadFile = QtWidgets.QPushButton(self.groupBox_2)
        self.btnUploadFile.setGeometry(QtCore.QRect(190, 100, 93, 28))
        self.btnUploadFile.setObjectName("btnUploadFile")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 100, 121, 121))
        self.groupBox.setObjectName("groupBox")
        self.ChoicePdfminer = QtWidgets.QRadioButton(self.groupBox)
        self.ChoicePdfminer.setGeometry(QtCore.QRect(20, 40, 115, 19))
        self.ChoicePdfminer.setObjectName("ChoicePdfminer")
        self.ChoiceButtonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.ChoiceButtonGroup.setObjectName("ChoiceButtonGroup")
        self.ChoiceButtonGroup.addButton(self.ChoicePdfminer)
        self.ChoiceOCR = QtWidgets.QRadioButton(self.groupBox)
        self.ChoiceOCR.setGeometry(QtCore.QRect(20, 70, 115, 19))
        self.ChoiceOCR.setObjectName("ChoiceOCR")
        self.ChoiceButtonGroup.addButton(self.ChoiceOCR)
        self.btnAnalyse = QtWidgets.QPushButton(self.groupBox_2)
        self.btnAnalyse.setGeometry(QtCore.QRect(190, 140, 93, 28))
        self.btnAnalyse.setObjectName("btnAnalyse")
        self.ChoiceWriteFile = QtWidgets.QCheckBox(self.groupBox_2)
        self.ChoiceWriteFile.setGeometry(QtCore.QRect(170, 180, 111, 31))
        self.ChoiceWriteFile.setObjectName("ChoiceWriteFile")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 280, 301, 151))
        self.groupBox_3.setObjectName("groupBox_3")
        self.btnPrintScreen = QtWidgets.QPushButton(self.groupBox_3)
        self.btnPrintScreen.setGeometry(QtCore.QRect(10, 20, 93, 28))
        self.btnPrintScreen.setObjectName("btnPrintScreen")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
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
        self.groupBox_2.setTitle(_translate("MainWindow", "pdf文件转换"))
        self.LabelFile.setText(_translate("MainWindow", "文件路径"))
        self.btnUploadFile.setText(_translate("MainWindow", "选择文件"))
        self.groupBox.setTitle(_translate("MainWindow", "识别方式"))
        self.ChoicePdfminer.setText(_translate("MainWindow", "Pdfminer"))
        self.ChoiceOCR.setText(_translate("MainWindow", "OCR"))
        self.btnAnalyse.setText(_translate("MainWindow", "分析"))
        self.ChoiceWriteFile.setText(_translate("MainWindow", "生成同名txt"))
        self.groupBox_3.setTitle(_translate("MainWindow", "截屏转换"))
        self.btnPrintScreen.setText(_translate("MainWindow", "截屏转换"))

