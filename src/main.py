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

# 3. Precargar sonidos (temporal: un solo sonido para todas las zonas)
# Cuando tengan los sonidos, cambiaremos esto por un mapeo real.
sonido_prueba = cargar_sonido("resources/sounds/C4.mp3")
sonidos = [sonido_prueba] * len(zonas)  # Lista con un sonido por zona

# 4. Configurar cámara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

print("Mesa Musical iniciada. Presiona 'q' para salir.")

# 5. Bucle principal
zona_anterior = -1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    pos = detectar_laser(frame)
    if pos:
        cx, cy = pos
        cv2.circle(frame, (cx, cy), 15, (0, 255, 0), 2)
        zona_actual = -1
        margen = 20  # Tolerancia para que el láser no tenga que entrar completo
        for i, (x, y, w, h) in enumerate(zonas):
            if (x - margen) < cx < (x + w + margen) and (y - margen) < cy < (y + h + margen):
                zona_actual = i
                cv2.putText(frame, f"Zona {i}", (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), -1)
                break

        if zona_actual != -1 and zona_actual != zona_anterior:
            reproducir(sonidos[zona_actual])

        zona_anterior = zona_actual
    else:
        zona_anterior = -1

    for (x, y, w, h) in zonas:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

        cv2.imshow("Mesa Musical", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or cv2.getWindowProperty("Mesa Musical", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()