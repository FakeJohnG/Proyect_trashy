"""Prueba el modelo en vivo con la cámara: dibuja una caja alrededor de lo que reconoce.

Uso, desde la raíz del repo:
    python scripts/probar_camara.py                 # prueba la cámara con el modelo genérico yolo11n.pt
    python scripts/probar_camara.py ruta/best.pt    # prueba TU modelo entrenado

Pulsa la tecla "q" con la ventana de la cámara seleccionada para salir.
"""
import sys

import cv2
from ultralytics import YOLO

RUTA_MODELO = "best.pt"
CONFIANZA = 0.4   # solo se dibujan detecciones con al menos 40 % de seguridad
TAMANO = 416      # más pequeño = más rápido en una laptop sin GPU (prueba 320, 416 o 640)

modelo = YOLO(RUTA_MODELO)

camara = cv2.VideoCapture(0)   # 0 = la cámara principal; si no abre, prueba con 1
if not camara.isOpened():
    raise SystemExit("No se pudo abrir la cámara. Prueba cambiando VideoCapture(0) por VideoCapture(1).")

while True:
    ok, frame = camara.read()
    if not ok:
        break

    # El modelo analiza el fotograma y devuelve cajas, clases y confianza.
    resultado = modelo.predict(frame, conf=CONFIANZA, imgsz=TAMANO, verbose=False)[0]

    # plot() dibuja las cajas y las etiquetas sobre la imagen.
    cv2.imshow("Residuos (q para salir)", resultado.plot())

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camara.release()
cv2.destroyAllWindows()
