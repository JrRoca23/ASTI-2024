import sys
import time
from pymata4 import pymata4
import numpy as np



from Controller.MotorControllerV2 import MotorControllerV2 
from Controller.UltrasoundControllerV2 import Ultrasonido 



# Configuración
board = pymata4.Pymata4()
m = MotorControllerV2(board)
u = Ultrasonido(board)

# Variables globales
disLimiteParedFrontal = 20
disLimiteParedLateral = 12
delante = False

# Función para avanzar en línea recta
def avanzaLineaRecta():
    print("Avanzando en línea recta...")
    m.backward()
    time.sleep(0.3)
    while True:
        m.changeSpeed(65)
        m.turnRight()  # Avanzar
        #time.sleep(0.2)
        distanciaCen = u.measureCenter()  # Medir distancia al frente
        distanciaIzq = u.measureLeft()  # Medir distancia a la izquierda
        distanciaDer = u.measureRight()  # Medir distancia a la derecha
        #distanciaBastonR = u.measureBaston()
        #distanciaBastonL = u.measureBastonLeft()
        
        #print("-----Distancia al frente:", distanciaCen)
        #print("Distancia a la izquierda:", distanciaIzq)
        #print("Distancia a la derecha:", distanciaDer)
        
        if distanciaCen < disLimiteParedFrontal:  # Si detecta un obstáculo al frente
            print("Obstáculo detectado al frente.")
            if not delante:
                m.stopcar()
                time.sleep(0.1)
                delante = True
            m.changeSpeedInd(255,255, 128, 128)
            m.forward()  # Detener el avance
        else:
            delante = False
            
# Avanzar durante 1 segundo antes de iniciar el bucle principal
print("Iniciando movimiento hacia adelante...")

# Bucle principal
#while True:
input()
avanzaLineaRecta()  # Llamar a la función para avanzar en línea recta