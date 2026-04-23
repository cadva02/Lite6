# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uu1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Prueba(object):
    def setupUi(self, Prueba):
        Prueba.setObjectName("Prueba")
        Prueba.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Prueba.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Prueba)
        self.centralwidget.setObjectName("centralwidget")
        Prueba.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Prueba)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        Prueba.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Prueba)
        self.statusbar.setObjectName("statusbar")
        Prueba.setStatusBar(self.statusbar)
        self.actionFile = QtWidgets.QAction(Prueba)
        self.actionFile.setObjectName("actionFile")
        self.actionSave_as = QtWidgets.QAction(Prueba)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionClose = QtWidgets.QAction(Prueba)
        self.actionClose.setObjectName("actionClose")
        self.actionExit = QtWidgets.QAction(Prueba)
        self.actionExit.setObjectName("actionExit")
        self.menuMenu.addAction(self.actionFile)
        self.menuMenu.addAction(self.actionSave_as)
        self.menuMenu.addAction(self.actionClose)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionExit)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(Prueba)
        QtCore.QMetaObject.connectSlotsByName(Prueba)

    def retranslateUi(self, Prueba):
        _translate = QtCore.QCoreApplication.translate
        Prueba.setWindowTitle(_translate("Prueba", "MainWindow"))
        self.menuMenu.setTitle(_translate("Prueba", "Menu"))
        self.actionFile.setText(_translate("Prueba", "File"))
        self.actionSave_as.setText(_translate("Prueba", "Save as"))
        self.actionClose.setText(_translate("Prueba", "Close"))
        self.actionExit.setText(_translate("Prueba", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Prueba = QtWidgets.QMainWindow()
    ui = Ui_Prueba()
    ui.setupUi(Prueba)
    Prueba.show()
    sys.exit(app.exec_())

