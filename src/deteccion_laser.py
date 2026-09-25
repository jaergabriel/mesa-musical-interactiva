import cv2
import numpy as np

def detectar_laser(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Rangos estrictos: saturación y brillo altísimos (solo el láser)
    rojo_bajo1 = np.array([0, 200, 200])
    rojo_alto1 = np.array([10, 255, 255])
    rojo_bajo2 = np.array([170, 200, 200])
    rojo_alto2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, rojo_bajo1, rojo_alto1)
    mask2 = cv2.inRange(hsv, rojo_bajo2, rojo_alto2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    # Limpiar ruido pequeño
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contornos:
        contorno_mas_grande = max(contornos, key=cv2.contourArea)
        area = cv2.contourArea(contorno_mas_grande)
        # Solo aceptar si el punto no es ni muy pequeño ni muy grande (evita la cara)
        if 5 < area < 500: 
            M = cv2.moments(contorno_mas_grande)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return (cx, cy)
    return None