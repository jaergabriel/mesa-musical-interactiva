import cv2
import numpy as np

def detectar_laser(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Rangos para láser VERDE (532 nm)
    verde_bajo = np.array([35, 100, 100])
    verde_alto = np.array([85, 255, 255])
    
    mask_verde = cv2.inRange(hsv, verde_bajo, verde_alto)
    
    kernel = np.ones((3, 3), np.uint8)
    mask_verde = cv2.morphologyEx(mask_verde, cv2.MORPH_OPEN, kernel)
    
    contornos, _ = cv2.findContours(mask_verde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    mejor_punto = None
    mejor_brillo = 0
    
    for c in contornos:
        area = cv2.contourArea(c)
        if area < 3 or area > 1500:
            continue
        
        x, y, w, h = cv2.boundingRect(c)
        if w == 0 or h == 0:
            continue
        
        roi_hsv = hsv[y:y+h, x:x+w]
        
        _, max_val, _, max_loc = cv2.minMaxLoc(roi_hsv[:, :, 2])
        
        if max_val > 100 and max_val > mejor_brillo:
            mejor_brillo = max_val
            px = x + max_loc[0]
            py = y + max_loc[1]
            mejor_punto = (px, py)
    
    return mejor_punto