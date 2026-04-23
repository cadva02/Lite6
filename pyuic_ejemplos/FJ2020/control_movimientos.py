from __future__ import annotations

import sys
from typing import Callable

from PyQt5 import QtCore, QtWidgets

from Lite6 import Ui_MainWindow
from movimientos import Abajo, Arriba, Derecha, Izquierda, Posicion


class VentanaControl(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.posicion = Posicion(0, 0)
        self._movimiento_activo: tuple[str, Callable[[Posicion], Posicion]] | None = None
        self._hold_timer = QtCore.QTimer(self)
        self._hold_timer.setInterval(100)
        self._hold_timer.timeout.connect(self._ejecutar_continuo)

        self._hold_delay = QtCore.QTimer(self)
        self._hold_delay.setSingleShot(True)
        self._hold_delay.setInterval(300)
        self._hold_delay.timeout.connect(self._iniciar_repeticion)

        self._crear_indicadores()
        self._conectar_botones()
        self._actualizar_vista()

    def _crear_indicadores(self) -> None:
        self.lbl_posicion = QtWidgets.QLabel("Posicion: (0, 0)", self.ui.centralwidget)
        self.lbl_posicion.setGeometry(30, 225, 300, 24)
        self.lbl_posicion.setStyleSheet("color: white; font-weight: bold;")

    def _conectar_botones(self) -> None:
        self.ui.B_arriba.pressed.connect(
            lambda: self._iniciar_movimiento_continuo("arriba", Arriba().ejecutar)
        )
        self.ui.B_der.pressed.connect(
            lambda: self._iniciar_movimiento_continuo("derecha", Derecha().ejecutar)
        )
        self.ui.B_abaj.pressed.connect(
            lambda: self._iniciar_movimiento_continuo("abajo", Abajo().ejecutar)
        )
        self.ui.B_Izq.pressed.connect(
            lambda: self._iniciar_movimiento_continuo("izquierda", Izquierda().ejecutar)
        )

        self.ui.B_arriba.released.connect(self._detener_movimiento_continuo)
        self.ui.B_der.released.connect(self._detener_movimiento_continuo)
        self.ui.B_abaj.released.connect(self._detener_movimiento_continuo)
        self.ui.B_Izq.released.connect(self._detener_movimiento_continuo)

    def _iniciar_movimiento_continuo(
        self, nombre: str, accion: Callable[[Posicion], Posicion]
    ) -> None:
        self._movimiento_activo = (nombre, accion)
        self._ejecutar(nombre, accion)
        self._hold_delay.start()

    def _iniciar_repeticion(self) -> None:
        if self._movimiento_activo is not None:
            self._hold_timer.start()

    def _ejecutar_continuo(self) -> None:
        if self._movimiento_activo is None:
            return

        nombre, accion = self._movimiento_activo
        self._ejecutar(nombre, accion)

    def _detener_movimiento_continuo(self) -> None:
        self._hold_delay.stop()
        self._hold_timer.stop()
        self._movimiento_activo = None

    def _ejecutar(self, nombre: str, accion: Callable[[Posicion], Posicion]) -> None:
        self.posicion = accion(self.posicion)
        self._actualizar_vista()

    def _actualizar_vista(self) -> None:
        self.lbl_posicion.setText(f"Posicion: ({self.posicion.x}, {self.posicion.y})")


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    ventana = VentanaControl()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
