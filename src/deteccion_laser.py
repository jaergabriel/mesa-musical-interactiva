import cv2
import numpy as np

def detectar_laser(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 1. Máscara de rojo (tolerante)
    rojo_bajo1 = np.array([0, 60, 60])
    rojo_alto1 = np.array([10, 255, 255])
    rojo_bajo2 = np.array([170, 60, 60])
    rojo_alto2 = np.array([180, 255, 255])
    mask_rojo = cv2.bitwise_or(cv2.inRange(hsv, rojo_bajo1, rojo_alto1),
                               cv2.inRange(hsv, rojo_bajo2, rojo_alto2))
    
    # Limpiar ruido
    kernel = np.ones((3, 3), np.uint8)
    mask_rojo = cv2.morphologyEx(mask_rojo, cv2.MORPH_OPEN, kernel)
    
    contornos, _ = cv2.findContours(mask_rojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    mejor_punto = None
    mejor_brillo = 0
    
    for c in contornos:
        area = cv2.contourArea(c)
        if area < 5 or area > 1500:
            continue
        
        # Recortar la región del contorno
        x, y, w, h = cv2.boundingRect(c)
        if w == 0 or h == 0:
            continue
        
        roi_hsv = hsv[y:y+h, x:x+w]
        
        # Buscar el píxel más brillante dentro de la región roja
        # Usamos el canal V (brillo)
        _, max_val, _, max_loc = cv2.minMaxLoc(roi_hsv[:, :, 2])
        
        # Si el brillo máximo es alto, es candidato
        if max_val > 150 and max_val > mejor_brillo:
            mejor_brillo = max_val
            # Convertir coordenadas locales a globales
            px = x + max_loc[0]
            py = y + max_loc[1]
            mejor_punto = (px, py)
    
    if mejor_punto is not None:
        return mejor_punto
    
    return None