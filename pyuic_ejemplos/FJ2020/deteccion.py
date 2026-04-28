import argparse
import math
import os
from functools import lru_cache
from dataclasses import dataclass
from typing import Any, Optional

import cv2
from inference import get_model
import supervision as sv

try:
    from xarm.wrapper import XArmAPI
except ImportError:
    XArmAPI = None

# 1. FORZAR COMPATIBILIDAD CON EL ENTORNO GRÁFICO (X11)
# Esto soluciona el error de Wayland en Ubuntu
os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["OPENCV_VIDEOIO_DEBUG"] = "1"  # Activa debug para ver si la cámara falla

# Tus credenciales por defecto
MODEL_ID = "shapeclassifier_group_9_id_409/1"
API_KEY = "1zTntUVnABXCBtOPSfPx"

DEFAULT_PORT = 4747
DEFAULT_PATH = "/video"
DEFAULT_PHONE_IP = "10.50.120.60"
ROBOT_HOME = (281.7, 0.80, 121.8, 171.0, 6.7, 125.9)
ROBOT_WORK = (303.3, -17, 87.5, 174.4, 1.2, 88.3)
VISION_SPAN_MM = (140.0, 140.0)

SHAPE_SEQUENCE = ("triangulo", "cuadrado", "circulo")
LABEL_ALIASES = {
    "triangle": "triangulo",
    "triangulo": "triangulo",
    "triángulo": "triangulo",
    "square": "cuadrado",
    "cuadrado": "cuadrado",
    "circle": "circulo",
    "circulo": "circulo",
    "círculo": "circulo",
}


@dataclass(frozen=True)
class DroidCamConfig:
    ip: str
    port: int = DEFAULT_PORT
    path: str = DEFAULT_PATH

    @property
    def url(self) -> str:
        return f"http://{self.ip}:{self.port}{self.path}"


@dataclass(frozen=True)
class ShapeDetection:
    label: str
    confidence: float
    center_x: float
    center_y: float
    box: tuple[float, float, float, float]


def _normalizar_etiqueta(label: object) -> Optional[str]:
    if label is None:
        return None

    texto = str(label).strip().lower()
    return LABEL_ALIASES.get(texto)


def _coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _shape_from_prediction(prediction: object) -> Optional[ShapeDetection]:
    if isinstance(prediction, dict):
        label = prediction.get("class_name") or prediction.get("class") or prediction.get("label")
        confidence = _coerce_float(prediction.get("confidence"), 0.0)
        center_x = prediction.get("x")
        center_y = prediction.get("y")
        left = prediction.get("left")
        top = prediction.get("top")
        width = prediction.get("width")
        height = prediction.get("height")
    else:
        label = getattr(prediction, "class_name", None) or getattr(prediction, "class", None) or getattr(prediction, "label", None)
        confidence = _coerce_float(getattr(prediction, "confidence", None), 0.0)
        center_x = getattr(prediction, "x", None)
        center_y = getattr(prediction, "y", None)
        left = getattr(prediction, "left", None)
        top = getattr(prediction, "top", None)
        width = getattr(prediction, "width", None)
        height = getattr(prediction, "height", None)

    canonical = _normalizar_etiqueta(label)
    if canonical is None:
        return None

    if center_x is None or center_y is None:
        if None in (left, top, width, height):
            return None
        center_x = _coerce_float(left) + _coerce_float(width) / 2.0
        center_y = _coerce_float(top) + _coerce_float(height) / 2.0

    if None in (left, top, width, height):
        width = 0.0
        height = 0.0
        left = _coerce_float(center_x)
        top = _coerce_float(center_y)

    return ShapeDetection(
        label=canonical,
        confidence=confidence,
        center_x=_coerce_float(center_x),
        center_y=_coerce_float(center_y),
        box=(
            _coerce_float(left),
            _coerce_float(top),
            _coerce_float(width),
            _coerce_float(height),
        ),
    )


def _shape_detections_from_results(results: object, detections: sv.Detections) -> list[ShapeDetection]:
    shapes: list[ShapeDetection] = []

    predictions = getattr(results, "predictions", None)
    if predictions:
        for prediction in predictions:
            shape = _shape_from_prediction(prediction)
            if shape is not None:
                shapes.append(shape)

    if shapes:
        return shapes

    data = getattr(detections, "data", None) or {}
    class_names = None
    for key in ("class_name", "class_names", "labels"):
        if key in data:
            class_names = list(data[key])
            break

    xyxy = getattr(detections, "xyxy", None)
    if xyxy is None:
        return shapes

    confidences = getattr(detections, "confidence", None)
    for index, box in enumerate(xyxy):
        label = None
        if class_names is not None and index < len(class_names):
            label = class_names[index]

        canonical = _normalizar_etiqueta(label)
        if canonical is None:
            continue

        x1, y1, x2, y2 = [float(value) for value in box]
        confidence = 0.0
        if confidences is not None and index < len(confidences):
            confidence = _coerce_float(confidences[index], 0.0)

        shapes.append(
            ShapeDetection(
                label=canonical,
                confidence=confidence,
                center_x=(x1 + x2) / 2.0,
                center_y=(y1 + y2) / 2.0,
                box=(x1, y1, x2, y2),
            )
        )

    return shapes


def _mejor_por_figura(shapes: list[ShapeDetection]) -> dict[str, ShapeDetection]:
    mejores: dict[str, ShapeDetection] = {}
    for shape in shapes:
        actual = mejores.get(shape.label)
        if actual is None or shape.confidence >= actual.confidence:
            mejores[shape.label] = shape
    return mejores


@lru_cache(maxsize=1)
def cargar_modelo() -> Any:
    return get_model(model_id=MODEL_ID, api_key=API_KEY)


def procesar_frame(
    frame: Any,
    model: Any,
    box_annotator: Any | None = None,
    label_annotator: Any | None = None,
) -> tuple[Any, dict[str, ShapeDetection], sv.Detections]:
    results = model.infer(frame)[0]
    detections = sv.Detections.from_inference(results)
    figuras = _shape_detections_from_results(results, detections)
    mejores_figuras = _mejor_por_figura(figuras)

    annotated_frame = frame.copy()
    if box_annotator is not None:
        annotated_frame = box_annotator.annotate(scene=annotated_frame, detections=detections)
    if label_annotator is not None:
        annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections)
    annotated_frame = _dibujar_guias(annotated_frame, mejores_figuras)

    return annotated_frame, mejores_figuras, detections


def _conectar_robot(robot_ip: str):
    if XArmAPI is None:
        raise RuntimeError("xArm API no disponible")

    arm = XArmAPI(robot_ip)
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)
    arm.move_gohome(wait=True)
    arm.set_position(*ROBOT_WORK, speed=20, wait=True)
    return arm


def _pose_desde_frame(frame: Any, shape: ShapeDetection) -> tuple[float, float, float, float, float, float]:
    height, width = frame.shape[:2]
    x0, y0, z0, roll0, pitch0, yaw0 = ROBOT_WORK

    offset_x = (shape.center_x / width - 0.5) * VISION_SPAN_MM[0]
    offset_y = (0.5 - shape.center_y / height) * VISION_SPAN_MM[1]

    return (x0 + offset_x, y0 + offset_y, z0, roll0, pitch0, yaw0)


def _mover_robot_a_figura(arm, frame: object, shape: ShapeDetection) -> None:
    x, y, z, roll, pitch, yaw = _pose_desde_frame(frame, shape)
    arm.set_position(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw, speed=20, wait=True)


def _dibujar_guias(frame: Any, mejores: dict[str, ShapeDetection]) -> Any:
    annotated = frame.copy()
    for indice, label in enumerate(SHAPE_SEQUENCE, start=1):
        shape = mejores.get(label)
        if shape is None:
            continue

        x1, y1, x2, y2 = [int(value) for value in shape.box]
        center = (int(shape.center_x), int(shape.center_y))
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(annotated, center, 5, (0, 255, 255), -1)
        cv2.putText(
            annotated,
            f"{indice}. {label}",
            (x1, max(0, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    return annotated


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Roboflow detection reading from a DroidCam stream (IP)."
    )
    parser.add_argument("ip", nargs="?", help="Phone IP address on the local network")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="DroidCam port")
    parser.add_argument(
        "--path",
        default=DEFAULT_PATH,
        help="DroidCam stream path (default: /video)",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Move the robot over the detected shapes in the order triangle, square, circle.",
    )
    parser.add_argument(
        "--robot-ip",
        default=None,
        help="xArm IP address used in auto mode.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show the OpenCV preview window when running this script directly.",
    )
    return parser.parse_args()


def ejecutar_deteccion_figuras(
    ip_camara: str = DEFAULT_PHONE_IP,
    robot_ip: str | None = None,
    puerto: int = DEFAULT_PORT,
    ruta: str = DEFAULT_PATH,
    modo_auto: bool = False,
    mostrar_ventana: bool = False,
) -> int:
    config = DroidCamConfig(ip=ip_camara, port=puerto, path=ruta)
    arm = None

    try:
        print("Cargando modelo...")
        model = cargar_modelo()

        cap = cv2.VideoCapture(config.url)
        if not cap.isOpened():
            print(
                f"Error: No se pudo abrir el stream en {config.url}. Revisa la IP y que DroidCam esté corriendo en el teléfono."
            )
            return 1

        box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()

        if modo_auto and robot_ip:
            arm = _conectar_robot(robot_ip)
            print(f"Robot conectado para modo automático: {robot_ip}")
        elif modo_auto:
            print("Modo automático activo sin IP de robot; se mostrará solo la detección.")

        print(f"Conectado con éxito al modelo: {MODEL_ID}")
        print(f"Conectado al stream: {config.url}")
        print("Iniciando bucle de video... Presiona 'q' para salir.")

        secuencia_ejecutada = False

        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("Error al leer el frame del stream.")
                break

            annotated_frame, mejores_figuras, detections = procesar_frame(
                frame,
                model,
                box_annotator,
                label_annotator,
            )

            if mejores_figuras:
                orden = " -> ".join(
                    label for label in SHAPE_SEQUENCE if label in mejores_figuras
                )
                if orden:
                    print(f"Figuras detectadas en secuencia objetivo: {orden}")

            if modo_auto and not secuencia_ejecutada and all(
                label in mejores_figuras for label in SHAPE_SEQUENCE
            ):
                print("Ejecutando secuencia: triangulo -> cuadrado -> circulo")
                for label in SHAPE_SEQUENCE:
                    figura = mejores_figuras[label]
                    print(f"Moviendo robot sobre {label}...")
                    if arm is not None:
                        _mover_robot_a_figura(arm, frame, figura)
                secuencia_ejecutada = True
                print("Secuencia completada.")

            if mostrar_ventana:
                cv2.imshow("Deteccion Roboflow", annotated_frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            if modo_auto and secuencia_ejecutada:
                break

        cap.release()
        if mostrar_ventana:
            cv2.destroyAllWindows()
        if arm is not None:
            try:
                arm.move_gohome(wait=True)
                arm.disconnect()
            except Exception:
                pass

        for _ in range(1, 5):
            cv2.waitKey(1)

    except Exception as e:
        print(f"Error detectado: {e}")
        return 1

    return 0


def main() -> int:
    args = parse_args()
    ip = args.ip or DEFAULT_PHONE_IP
    return ejecutar_deteccion_figuras(
        ip_camara=ip,
        robot_ip=args.robot_ip,
        puerto=args.port,
        ruta=args.path,
        modo_auto=args.auto,
        mostrar_ventana=args.preview,
    )


if __name__ == "__main__":
    raise SystemExit(main())