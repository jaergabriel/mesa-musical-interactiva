import cv2
import json
import os
import sys
from deteccion_laser import detectar_laser
from sonidos import cargar_sonido, reproducir

# 1. Verificar si existe zonas.json
if not os.path.exists("zonas.json"):
    print("Mesa no calibrada. Ejecutando calibración...")
    os.system("python src/calibracion.py")
    if not os.path.exists("zonas.json"):
        print("No se pudo calibrar. Saliendo.")
        sys.exit()
    print("Calibración completada. Iniciando mesa musical...")

# 2. Cargar zonas
with open("zonas.json", "r") as f:
    zonas = json.load(f)

print(f"Cargadas {len(zonas)} zonas.")

# 3. Cargar sonido (CAMBIA ESTO por el archivo que tengas)
sonido = cargar_sonido("resources/sounds/C4.mp3")

# 4. Configurar cámara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

print("Mesa Musical iniciada. Presiona 'q' para salir.")

# 5. Bucle principal
zona_anterior = -1
contador = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    pos = detectar_laser(frame)
    if pos:
        cx, cy = pos
        cv2.circle(frame, (cx, cy), 15, (0, 255, 0), 2)
        zona_actual = -1
        for i, (x, y, w, h) in enumerate(zonas):
            if x < cx < x + w and y < cy < y + h:
                zona_actual = i
                cv2.putText(frame, f"Zona {i}", (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), -1)
                break

        # Solo reproducir si la zona cambió (entrada a nueva zona)
        if zona_actual != -1 and zona_actual != zona_anterior:
            reproducir(sonido)

        zona_anterior = zona_actual
    else:
        zona_anterior = -1

    for (x, y, w, h) in zonas:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

    cv2.imshow("Mesa Musical", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()