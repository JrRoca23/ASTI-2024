import sys
import time
from pymata4 import pymata4
import threading
import _thread
import numpy as np

from Controller.MotorControllerV2 import MotorControllerV2 
from Controller.UltrasoundControllerV2 import Ultrasonido 
from Controller.IrControllerV2 import IrControllerV2 
from Controller.ServoControllerV2 import Servo

# Configuración
board = pymata4.Pymata4()
m = MotorControllerV2(board)
u = Ultrasonido(board)

# Variables globales
avanzarTerminado = 0
disLimiteParedFrontal = 25
disCen = 100

# Función para determinar dirección de giro
def determinarDireccionGiro():
    distanciaIzquierda = u.measureLeft()
    distanciaDerecha = u.measureRight()
    
    if distanciaIzquierda < distanciaDerecha:
        return "izquierda"
    else:
        return "derecha"

# Función para avanzar en línea recta
def avanzaLineaRecta():
    global avanzarTerminado
    
    while True:
        m.forward()  # Avanzar
        
        distanciaCen = u.measureCenter()  # Medir distancia al frente
        distanciaIzq = u.measureLeft()  # Medir distancia a la izquierda
        distanciaDer = u.measureRight()  # Medir distancia a la derecha
        
        if distanciaCen < disLimiteParedFrontal:  # Si detecta un obstáculo al frente
            m.stopcar()  # Detener el avance
            time.sleep(0.1)
            
            # Ajuste lateral
            if distanciaIzq < disCen:  # Si el obstáculo está más cerca a la izquierda
                m.right()  # Moverse un poco hacia la derecha
                time.sleep(0.1)
            elif distanciaDer < disCen:  # Si el obstáculo está más cerca a la derecha
                m.left()  # Moverse un poco hacia la izquierda
                time.sleep(0.1)
                
            direccionGiro = determinarDireccionGiro()  # Determinar hacia dónde girar
            if direccionGiro == "izquierda":
                m.turnLeft()  # Girar a la izquierda
            else:
                m.turnRight()  # Girar a la derecha
                
            time.sleep(0.5)  # Tiempo para completar el giro
            
            m.stopcar()  # Detenerse después del giro
            avanzarTerminado = 0  # Reiniciar la bandera de avance terminado
            break  # Salir del bucle de avance en línea recta

# Bucle principal
while True:
    m.forward()
    time.sleep(0.5)
    avanzaLineaRecta()  # Llamar a la función para avanzar en línea recta
