import cv2
import numpy as np

# Iniciar captura de video
cap = cv2.VideoCapture(0)

# Reducir la resolución de la imagen
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Crear ventana de visualización
cv2.namedWindow("Video en vivo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video en vivo", 640, 480)  # Ajustar tamaño de la ventana

def detectarCirculos(img, frame):
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                               param1=50, param2=30, minRadius=10, maxRadius=100)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)

def detectarArcos(img, frame):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 400:
            perimetro = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimetro, True)
            objCorner = len(approx)
            if objCorner > 4:
                cv2.drawContours(frame, [approx], -1, (0, 255, 255), 3)
                objectType = 'Arco'
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, objectType, (x + (w // 2) - 10, y + (h // 2) - 10), 
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)

# Bucle principal
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir la imagen a escala de grises
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar desenfoque gaussiano
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)

    # Detectar bordes con Canny
    imgCanny = cv2.Canny(imgBlur, 50, 50)

    # Llamar a las funciones para detectar círculos y "arcos"
    detectarCirculos(imgCanny, frame)
    detectarArcos(imgCanny, frame)

    # Mostrar el video en vivo
    cv2.imshow("Video en vivo", frame)

    # Salir del bucle al presionar la tecla 'Esc'
    if cv2.waitKey(1) == 27:
        break

# Liberar los recursos y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
