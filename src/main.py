import cv2
import json
import os
import sys
from deteccion_laser import detectar_laser
from sonidos import cargar_sonido, reproducir

# 1. Verificar si existe zonas.json
if not os.path.exists("zonas.json"):
    print("Mesa no calibrada. Ejecutando calibración...")
    os.system("python src/calibracion.py")  # Ejecuta la calibración automáticamente
    if not os.path.exists("zonas.json"):
        print("No se pudo calibrar. Saliendo.")
        sys.exit()
    print("Calibración completada. Iniciando mesa musical...")

# 2. Cargar zonas
with open("zonas.json", "r") as f:
    zonas = json.load(f)

print(f"Cargadas {len(zonas)} zonas.")

# 3. Cargar sonido de prueba (cámbialo por el tuyo)
sonido = cargar_sonido("resources/sounds/C4.mp3")

# 4. Bucle principal
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Mesa Musical iniciada. Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    pos = detectar_laser(frame)
    if pos:
        cx, cy = pos
        cv2.circle(frame, (cx, cy), 15, (0, 255, 0), 2)
        for i, (x, y, w, h) in enumerate(zonas):
            if x < cx < x + w and y < cy < y + h:
                reproducir(sonido)
                cv2.putText(frame, f"Zona {i}", (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                break

    for (x, y, w, h) in zonas:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

    cv2.imshow("Mesa Musical", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()