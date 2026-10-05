import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

print("Apunta el láser a la cámara.")
print("Si el círculo verde sigue el láser, la cámara SÍ lo captura.")
print("Si el círculo no sigue el láser, la cámara NO lo captura.")
print("Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a escala de grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Encontrar el píxel más brillante
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gris)
    
    # Dibujar un círculo en el píxel más brillante
    x, y = max_loc
    cv2.circle(frame, (x, y), 20, (0, 255, 0), 2)
    cv2.putText(frame, f"Brillo max: {max_val}", (x + 25, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    cv2.imshow("Brillo", frame)
    cv2.imshow("Grises", gris)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
