import cv2
import numpy as np

# 1. Encender la cámara y optimizarla para la Celeron
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Resolución baja para que no laguee
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Presiona la tecla 'q' para salir.")

while True:
    # 2. Leer el fotograma de la cámara
    ret, frame = cap.read()
    if not ret:
        print("No se pudo acceder a la cámara")
        break

    # 3. Convertir la imagen de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 4. Definir el rango de color rojo (el láser)
    # El rojo en HSV está en los extremos, por eso usamos dos rangos
    rojo_bajo1 = np.array([0, 120, 70])
    rojo_alto1 = np.array([10, 255, 255])
    
    rojo_bajo2 = np.array([170, 120, 70])
    rojo_alto2 = np.array([180, 255, 255])

    # 5. Crear las máscaras para ambos rangos de rojo
    mask1 = cv2.inRange(hsv, rojo_bajo1, rojo_alto1)
    mask2 = cv2.inRange(hsv, rojo_bajo2, rojo_alto2)
    
    # 6. Unir las dos máscaras en una sola
    mask = cv2.bitwise_or(mask1, mask2)

    # 7. Buscar contornos (el punto blanco en la máscara)
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contornos:
        # Encontrar el contorno más grande (el punto láser)
        contorno_mas_grande = max(contornos, key=cv2.contourArea)
        
        # Verificar que el área sea lo suficientemente grande (que no sea ruido)
        if cv2.contourArea(contorno_mas_grande) > 5:
            # Obtener el centro del contorno
            M = cv2.moments(contorno_mas_grande)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Dibujar un círculo verde en el centro del láser
                cv2.circle(frame, (cx, cy), 15, (0, 255, 0), 2)
                cv2.putText(frame, "Laser!", (cx + 20, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # 8. Mostrar el resultado en pantalla
    cv2.imshow("Laser Tracker", frame)
    # Mostrar la máscara (opcional, para depurar)
    cv2.imshow("Mascara", mask)

    # 9. Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 10. Apagar todo al salir
cap.release()
cv2.destroyAllWindows()