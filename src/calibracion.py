import cv2
import json
import numpy as np

puntos = []
zonas = []
dibujando = False

def dibujar_rectangulo(event, x, y, flags, param):
    global puntos, dibujando
    if event == cv2.EVENT_LBUTTONDOWN:
        puntos = [(x, y)]
        dibujando = True
    elif event == cv2.EVENT_MOUSEMOVE and dibujando:
        puntos.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP:
        dibujando = False
        if len(puntos) > 1:
            x1, y1 = puntos[0]
            x2, y2 = puntos[-1]
            zonas.append((min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)))
            puntos = []

# 1. Encender cámara (OJO: AQUÍ PONEMOS LA CÁMARA 1)
cap = cv2.VideoCapture(1) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Presiona 'c' para capturar la imagen. Presiona 'q' o cierra la ventana para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo acceder a la cámara")
        break
    cv2.imshow("Camara - Presiona 'c' para capturar", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        imagen = frame.copy()
        break
    elif key == ord('q') or cv2.getWindowProperty("Camara - Presiona 'c' para capturar", cv2.WND_PROP_VISIBLE) < 1:
        cap.release()
        cv2.destroyAllWindows()
        exit()

cap.release()
cv2.destroyAllWindows()

# 2. Ventana de calibración
cv2.namedWindow("Calibracion")
cv2.setMouseCallback("Calibracion", dibujar_rectangulo)

while True:
    temp = imagen.copy()
    for (x, y, w, h) in zonas:
        cv2.rectangle(temp, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if len(puntos) > 1:
        cv2.rectangle(temp, puntos[0], puntos[-1], (0, 0, 255), 1)
    
    cv2.imshow("Calibracion", temp)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        with open("zonas.json", "w") as f:
            json.dump(zonas, f, indent=4)
        print(f"Guardadas {len(zonas)} zonas en zonas.json")
        break
    elif key == ord('r'):
        zonas = []
        puntos = []
        print("Zonas reiniciadas")
    elif key == ord('q') or cv2.getWindowProperty("Calibracion", cv2.WND_PROP_VISIBLE) < 1:
        print("Saliendo sin guardar...")
        break

cv2.destroyAllWindows()