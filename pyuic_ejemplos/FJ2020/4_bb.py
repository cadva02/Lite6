import sys
import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from uu1 import *

class Ui_Prueba(QtWidgets.QMainWindow,Ui_Prueba):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Ui_Prueba()
    window.show()
    app.exec_()
