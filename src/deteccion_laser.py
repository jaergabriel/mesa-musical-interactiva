import cv2
import numpy as np

# Historial para suavizado
historial = []
max_historial = 5

def detectar_laser(frame):
    global historial
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Rangos para láser VERDE (ajustar según calibración)
    verde_bajo = np.array([35, 100, 100])   # <-- CAMBIA ESTOS VALORES
    verde_alto = np.array([85, 255, 255])   # <-- CAMBIA ESTOS VALORES
    
    mask_verde = cv2.inRange(hsv, verde_bajo, verde_alto)
    
    # Limpiar ruido
    kernel = np.ones((3, 3), np.uint8)
    mask_verde = cv2.morphologyEx(mask_verde, cv2.MORPH_OPEN, kernel)
    
    contornos, _ = cv2.findContours(mask_verde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    mejor_punto = None
    mejor_area = 0
    
    for c in contornos:
        area = cv2.contourArea(c)
        if area < 5 or area > 2000:  # Ajusta según el tamaño del punto
            continue
        
        x, y, w, h = cv2.boundingRect(c)
        if w == 0 or h == 0:
            continue
        
        # Recortar la región del contorno
        roi_hsv = hsv[y:y+h, x:x+w]
        roi_gris = roi_hsv[:, :, 2]  # Canal V (brillo)
        
        # Umbral de brillo dentro del contorno (solo lo más brillante)
        _, umbral = cv2.threshold(roi_gris, 200, 255, cv2.THRESH_BINARY)
        # Si el umbral no encuentra nada, bajar el valor
        if cv2.countNonZero(umbral) == 0:
            _, umbral = cv2.threshold(roi_gris, 150, 255, cv2.THRESH_BINARY)
        
        # Encontrar el centroide de la región brillante
        momentos = cv2.moments(umbral)
        if momentos["m00"] > 0:
            cx_local = int(momentos["m10"] / momentos["m00"])
            cy_local = int(momentos["m01"] / momentos["m00"])
            px = x + cx_local
            py = y + cy_local
            # Elegir el contorno con mayor área (el láser suele ser el más grande)
            if area > mejor_area:
                mejor_area = area
                mejor_punto = (px, py)
    
    # Suavizado con promedio móvil
    if mejor_punto is not None:
        historial.append(mejor_punto)
        if len(historial) > max_historial:
            historial.pop(0)
        # Promediar
        xs = [p[0] for p in historial]
        ys = [p[1] for p in historial]
        return (int(np.mean(xs)), int(np.mean(ys)))
    else:
        # Si no se detecta, devolver la última posición conocida (si hay)
        if historial:
            return historial[-1]
        return None