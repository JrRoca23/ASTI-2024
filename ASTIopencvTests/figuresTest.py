import cv2

print('Librerias leidas')

# Iniciar captura de video
cap = cv2.VideoCapture(0)

# Reducir la resolución de la imagen
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Crear ventana de visualización
cv2.namedWindow("Video en vivo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video en vivo", 640, 480)  # Ajustar tamaño de la ventana

def getContours(img):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 400:
            cv2.drawContours(frame, [cnt], -1, (255, 0, 0), 3)
            perimetro = cv2.arcLength(cnt, True)
            aprox = cv2.approxPolyDP(cnt, 0.02 * perimetro, True)
            objCorner = len(aprox)
            x, y, w, h = cv2.boundingRect(aprox)

            if objCorner == 3:
                objectType = 'Triangulo'
            elif objCorner == 4:
                aspecto = w / float(h)
                if aspecto > 0.95 and aspecto < 1.05:
                    objectType = 'Cuadrado'
                else:
                    objectType = 'Rectangulo'
            elif objCorner == 10:
                objectType = 'Estrella'
            elif objCorner > 4:
                objectType = 'Cilindro'
            elif objCorner > 4:
                objectType = 'Arco'
            else:
                objectType = '???'

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

    # Llamar a la función getContours para detectar contornos
    getContours(imgCanny)

    # Mostrar el video en vivo
    cv2.imshow("Video en vivo", frame)

    # Salir del bucle al presionar la tecla 'Esc'
    if cv2.waitKey(1) == 27:
        break

# Liberar los recursos y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
