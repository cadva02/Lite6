# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui1.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 90, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(170, 190, 100, 20))
        self.radioButton.setObjectName("radioButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(210, 310, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(350, 100, 64, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(370, 180, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(260, 30, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.dial = QtWidgets.QDial(self.centralwidget)
        self.dial.setGeometry(QtCore.QRect(60, 220, 50, 64))
        self.dial.setObjectName("dial")
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(100, 320, 22, 160))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 250, 60, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuedicion = QtWidgets.QMenu(self.menubar)
        self.menuedicion.setObjectName("menuedicion")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionE1 = QtWidgets.QAction(MainWindow)
        self.actionE1.setObjectName("actionE1")
        self.actionE2 = QtWidgets.QAction(MainWindow)
        self.actionE2.setObjectName("actionE2")
        self.actionE3 = QtWidgets.QAction(MainWindow)
        self.actionE3.setObjectName("actionE3")
        self.actionedicio3 = QtWidgets.QAction(MainWindow)
        self.actionedicio3.setObjectName("actionedicio3")
        self.actionedicion4 = QtWidgets.QAction(MainWindow)
        self.actionedicion4.setObjectName("actionedicion4")
        self.menuMenu.addAction(self.actionE1)
        self.menuMenu.addAction(self.actionE2)
        self.menuMenu.addAction(self.actionE3)
        self.menuedicion.addAction(self.actionedicio3)
        self.menuedicion.addAction(self.actionedicion4)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuedicion.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "alerta m"))
        self.radioButton.setText(_translate("MainWindow", "elel"))
        self.label.setText(_translate("MainWindow", "Perilla"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuedicion.setTitle(_translate("MainWindow", "edicion"))
        self.actionE1.setText(_translate("MainWindow", "E1"))
        self.actionE2.setText(_translate("MainWindow", "E2"))
        self.actionE3.setText(_translate("MainWindow", "E3"))
        self.actionedicio3.setText(_translate("MainWindow", "edicio3"))
        self.actionedicion4.setText(_translate("MainWindow", "edicion4"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
