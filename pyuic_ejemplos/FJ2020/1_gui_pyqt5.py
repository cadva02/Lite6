from PyQt5.QtWidgets import *
app = QApplication([])
button = QPushButton('Presioname!!!')
def on_button_clicked():
    alert = QMessageBox()
    alert.setText('Pero no tan fuerte ;)')
    alert.exec_()

button.clicked.connect(on_button_clicked)
button.show()
app.exec_()
