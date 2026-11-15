import cv2
import json
import os
import sys
from deteccion_laser import detectar_laser
from sonidos import cargar_sonido, reproducir

# Variables globales para el mouse
mouse_x, mouse_y = 0, 0

def mover_mouse(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y

# 1. Verificar si existe zonas.json
if not os.path.exists("zonas.json"):
    os.system("python src/calibracion.py")

with open("zonas.json", "r") as f:
    zonas = json.load(f)
with open("config.json", "r") as f:
    config = json.load(f)

print(f"Cargadas {len(zonas)} zonas.")
print("Cargando sonidos...")
sonidos_bancoA = [cargar_sonido(ruta) for ruta in config["bancoA"]]
sonidos_bancoB = [cargar_sonido(ruta) for ruta in config["bancoB"]]
sonidos_controles = [cargar_sonido(ruta) for ruta in config["controles"]]
sonidos_plato = [cargar_sonido(ruta) for ruta in config["plato"]]
print("¡Sonidos cargados!")

# Variables de estado
banco_actual = "A" 
sonidos_actuales = sonidos_bancoA

cap = cv2.VideoCapture(1) # Cámara nueva
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cap.set(cv2.CAP_PROP_EXPOSURE, -6) 

print("Mesa Musical (MODO MOUSE) iniciada. Mueve el mouse sobre las cajas. Presiona 'q' para salir.")
zona_anterior = -1

while True:
    ret, frame = cap.read()
    if not ret: break

    # --- SIMULACIÓN DE LÁSER CON MOUSE ---
    pos = (mouse_x, mouse_y)
    
    if pos:
        cx, cy = pos
        # Dibujamos un circulito donde está el mouse
        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1) 
        zona_actual = -1
        margen = 20 
        
        for i, (x, y, w, h) in enumerate(zonas):
            if (x - margen) < cx < (x + w + margen) and (y - margen) < cy < (y + h + margen):
                zona_actual = i
                break

        # Si entra a una zona nueva
        if zona_actual != -1 and zona_actual != zona_anterior:
            
            # Lógica del Mapeo
            if zona_actual < 10: # Cuerdas (0-4) y Pads (5-9)
                reproducir(sonidos_actuales[zona_actual])
                
            elif zona_actual == 10: # Botón A
                banco_actual = "A"
                sonidos_actuales = sonidos_bancoA
                print("Cambiado a Banco A")
                reproducir(sonidos_controles[0]) # REC como sonido de confirmación
                
            elif zona_actual == 11: # Botón B
                banco_actual = "B"
                sonidos_actuales = sonidos_bancoB
                print("Cambiado a Banco B")
                reproducir(sonidos_controles[0]) 
                
            # Controles (El orden en la mesa es: REC, PLAY, STOP, DEL)
            elif zona_actual == 12: # REC
                print("Grabando...")
                reproducir(sonidos_controles[0])
            elif zona_actual == 13: # PLAY
                print("Reproduciendo...")
                reproducir(sonidos_controles[3]) 
            elif zona_actual == 14: # STOP
                print("Detenido...")
                reproducir(sonidos_controles[1]) 
            elif zona_actual == 15: # DEL
                print("Borrando...")
                reproducir(sonidos_controles[2]) 
                
            elif zona_actual == 16: # Plato DJ
                reproducir(sonidos_plato[0]) # Scratch

        zona_anterior = zona_actual
    else:
        zona_anterior = -1

    # --- DIBUJO DE LAS ZONAS CON COLORES ---
    for i, (x, y, w, h) in enumerate(zonas):
        # Colores BGR
        if i < 5: 
            color = (255, 255, 0)    # CYAN (Cuerdas)
        elif i < 10:
            color = (255, 0, 255)    # MAGENTA (Pads)
        elif i < 12:
            color = (0, 255, 0)      # VERDE (Botones A/B)
        elif i < 16:
            color = (0, 255, 255)    # AMARILLO (Controles REC/PLAY/STOP/DEL)
        else:
            color = (255, 0, 0)      # AZUL (Plato DJ)

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        # Número de la zona para identificarlas
        cv2.putText(frame, str(i), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Mesa Musical", frame)
    
    # Conectar el mouse a la ventana
    cv2.setMouseCallback("Mesa Musical", mover_mouse)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or cv2.getWindowProperty("Mesa Musical", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()