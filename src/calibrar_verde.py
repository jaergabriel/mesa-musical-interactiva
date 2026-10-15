import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# Intenta desactivar la autoexposición (si la cámara lo permite)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cap.set(cv2.CAP_PROP_EXPOSURE, -6)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("H min", "Trackbars", 35, 180, nothing)
cv2.createTrackbar("H max", "Trackbars", 85, 180, nothing)
cv2.createTrackbar("S min", "Trackbars", 100, 255, nothing)
cv2.createTrackbar("S max", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("V min", "Trackbars", 100, 255, nothing)
cv2.createTrackbar("V max", "Trackbars", 255, 255, nothing)

print("Ajusta los sliders hasta que el láser se vea BLANCO y el fondo NEGRO en la ventana 'Mascara'.")
print("Anota los valores que funcionen y presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    h_min = cv2.getTrackbarPos("H min", "Trackbars")
    h_max = cv2.getTrackbarPos("H max", "Trackbars")
    s_min = cv2.getTrackbarPos("S min", "Trackbars")
    s_max = cv2.getTrackbarPos("S max", "Trackbars")
    v_min = cv2.getTrackbarPos("V min", "Trackbars")
    v_max = cv2.getTrackbarPos("V max", "Trackbars")
    
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv, lower, upper)
    
    cv2.imshow("Camara", frame)
    cv2.imshow("Mascara", mask)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()