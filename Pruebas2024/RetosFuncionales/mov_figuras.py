import cv2
import time

from pymata4 import pymata4
from Controller.MotorControllerV2 import MotorControllerV2

print('Librerias leidas')

board = pymata4.Pymata4()
m = MotorControllerV2(board)

# Iniciar captura de video
cap = cv2.VideoCapture(0)

# Reducir la resolución de la imagen
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Crear ventana de visualización
cv2.namedWindow("Video en vivo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video en vivo", 640, 480)  # Ajustar tamaño de la ventana

def getContours(img):
    yes = "y"
    
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
                r = input("la figura es un Triangulo: (y/n)")
                if yes in r:
                    cap.release()
                    objectType = 'Triangulo'
                    m.changeSpeedInd(75, 75, 67, 67)
                    m.forward()
                    time.sleep(dis_recto (1200))
                    m.stopcar()
                    time.sleep(1)
                    m.changeSpeedInd(95, 95, 62, 62)
                    m.right()
                    time.sleep(dis_derecha (248))
                    m.stopcar()
            elif objCorner == 4:
                r = input("la figura es un Rectangulo: (y/n)")
                if yes in r:
                    cap.release()
                    objectType = 'Rectangulo'
                    m.changeSpeedInd(75, 75, 67, 67)
                    m.forward()
                    time.sleep(dis_recto (1733))
                    m.stopcar()
                    time.sleep(1)
                    m.changeSpeedInd(95, 95, 62, 62)
                    m.right()
                    time.sleep(dis_derecha (361) + 0.5)
                    m.stopcar()
            elif objCorner == 10:
                r = input("la figura es un Estrella: (y/n)")
                if yes in r:
                    cap.release()
                    objectType = 'Estrella'
                    m.changeSpeedInd(75, 75, 67, 67)
                    m.forward()
                    time.sleep(dis_recto (1687))
                    m.stopcar()
                    time.sleep(1)
                    m.changeSpeedInd(95, 95, 62, 62)
                    m.left()
                    time.sleep(dis_derecha (17))
                    m.stopcar()
            elif objCorner > 5:
                r = input("la figura es un Cilindro: (y/n)")
                if yes in r:
                    cap.release()
                    objectType = 'Cilindro'
                    m.changeSpeedInd(128, 128, 128, 128)
                    m.forward()
                    time.sleep(dis_recto (649))
                    m.stopcar()
                    time.sleep(1)
                    m.changeSpeedInd(95, 95, 62, 62)
                    m.right()
                    time.sleep(dis_derecha (213))
                    m.stopcar()
            else:
                r = input("la figura es un Arco: (y/n)")
                print(type(y))
                print(type(r))
                if yes in r:
                    cap.release()
                    objectType = 'Arco'
                    m.changeSpeedInd(75, 75, 67, 67)
                    m.forward()
                    time.sleep(dis_recto (35))
                    m.stopcar()
                    time.sleep(1)
                    m.changeSpeedInd(95, 95, 62, 62)
                    m.right()
                    time.sleep(dis_derecha (586))
                    m.stopcar()
            '''
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, objectType, (x + (w // 2) - 10, y + (h // 2) - 10), 
                        cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)
            '''
def dis_recto(mm):
    
    cm = mm/10
    a =  cm*1.23016
    a = a/18.8396492
    return a

def dis_derecha(mm):

    cm = mm/10
    a = cm*3/25
    return a


# Bucle principal detección de figura:
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