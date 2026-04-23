#pyuic5.exe -x p1.ui -o p1.py
import os
from PyQt5 import QtGui, QtCore
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from ui1 import *

class Ui_MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        #-------------------------
        self.dial.setMinimum(0)
        self.dial.setMaximum(100)
        self.dial.setValue(40)
        self.lineEdit.setText("Haz clic en el boton")
        self.pushButton.setText("Presioname")
        #-------------------------
        self.dial.valueChanged.connect(self.sliderMoved)
        self.pushButton.clicked.connect(self.actualizar)
        self.radioButton.toggled.connect(self.onClicked)
        self.actionE3.triggered.connect(self.close)

    def sliderMoved(self):
        self.lcdNumber.display(self.dial.value())

    def onClicked(self):
        self.textBrowser.setFont(QtGui.QFont('SansSerif', 30))
        self.textBrowser.setText("Hola")

    def actualizar(self):
        self.lineEdit.setText("")
        self.lineEdit.setText("Acabas de hacer clic en el boton!")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Ui_MainWindow()
    window.show()
    app.exec_()
