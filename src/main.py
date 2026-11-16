import cv2
import json
import os
import sys
import pygame
from deteccion_laser import detectar_laser
from sonidos import cargar_sonido, reproducir

# Variables globales para el mouse
mouse_x, mouse_y = 0, 0

def eventos_mouse(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y

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

banco_actual = "A" 
sonidos_actuales = sonidos_bancoA
zona_anterior = -1
canal_actual = None 

cap = cv2.VideoCapture(1) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cap.set(cv2.CAP_PROP_EXPOSURE, -6) 

cv2.namedWindow("Mesa Musical")
cv2.setMouseCallback("Mesa Musical", eventos_mouse)

print("Mesa Musical iniciada. Cierra la ventana con la 'X' para salir.")

while True:
    ret, frame = cap.read()
    if not ret: break

    pos = (mouse_x, mouse_y)
    
    if pos:
        cx, cy = pos
        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1) 
        zona_actual = -1
        
        # --- CAMBIO 1: Margen a 0 para que las zonas sean exactas y no se pisen ---
        margen = 0 
        
        for i, (x, y, w, h) in enumerate(zonas):
            if (x - margen) < cx < (x + w + margen) and (y - margen) < cy < (y + h + margen):
                zona_actual = i
                break

        if zona_actual != -1 and zona_actual != zona_anterior:
            
            # Fadeout de seguridad para el Banco B
            if canal_actual is not None and zona_anterior < 5 and banco_actual == "B":
                canal_actual.fadeout(400)

            canal_fijo = pygame.mixer.Channel(zona_actual)
            
            # --- CAMBIO 2: Transición armónica entre cuerdas ---
            if zona_anterior >= 0 and zona_anterior < 5: 
                # Si venimos de tocar otra cuerda, hacemos un micro-fadeout para que se unan las notas
                canal_fijo.fadeout(150) 
            else:
                # Si venimos de un pad o botón, detenemos el sonido en seco
                canal_fijo.stop()

            if zona_actual < 10: 
                canal_fijo.play(sonidos_actuales[zona_actual])
                canal_actual = canal_fijo
            elif zona_actual == 10: 
                banco_actual = "A"
                sonidos_actuales = sonidos_bancoA
                print("Cambiado a Banco A")
                canal_fijo.play(sonidos_controles[0]) 
                canal_actual = canal_fijo
            elif zona_actual == 11: 
                banco_actual = "B"
                sonidos_actuales = sonidos_bancoB
                print("Cambiado a Banco B")
                canal_fijo.play(sonidos_controles[0]) 
                canal_actual = canal_fijo
            elif zona_actual == 12: 
                canal_fijo.play(sonidos_controles[0])
                canal_actual = canal_fijo
            elif zona_actual == 13: 
                canal_fijo.play(sonidos_controles[3]) 
                canal_actual = canal_fijo
            elif zona_actual == 14: 
                canal_fijo.play(sonidos_controles[1]) 
                canal_actual = canal_fijo
            elif zona_actual == 15: 
                canal_fijo.play(sonidos_controles[2]) 
                canal_actual = canal_fijo
            elif zona_actual == 16: 
                canal_fijo.play(sonidos_plato[0]) 
                canal_actual = canal_fijo

        elif zona_actual == -1 and zona_anterior != -1:
            if canal_actual is not None and zona_anterior < 5 and banco_actual == "B":
                canal_actual.fadeout(400) 
                canal_actual = None

        zona_anterior = zona_actual

    # --- DIBUJO DE LAS ZONAS ---
    for i, (x, y, w, h) in enumerate(zonas):
        if i < 5: color = (255, 255, 0)    # CYAN
        elif i < 10: color = (255, 0, 255)  # MAGENTA
        elif i < 12: color = (0, 255, 0)    # VERDE
        elif i < 16: color = (0, 255, 255)  # AMARILLO
        else: color = (255, 0, 0)           # AZUL

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, str(i), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Mesa Musical", frame)
    
    cv2.waitKey(1) 
    if cv2.getWindowProperty("Mesa Musical", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()