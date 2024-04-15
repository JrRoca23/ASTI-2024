import sys
import time
from pymata4 import pymata4
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
disLimiteParedFrontal = 15
disLimiteParedLateral = 12

# Función para determinar dirección de giro
def determinarDireccionGiro():
    distanciaIzquierda = u.measureLeft()
    distanciaDerecha = u.measureRight()
    distanciaCentro = u.measureCenter()
    
    if distanciaIzquierda > distanciaDerecha and distanciaIzquierda > distanciaCentro:
        return "izquierda"
    elif distanciaDerecha > distanciaIzquierda and distanciaDerecha > distanciaCentro:
        return "derecha"
    #elif distanciaCentro > distanciaDerecha and  distanciaCentro > distanciaIzquierda:
        #return "avanzar"

# Función para avanzar en línea recta
def avanzaLineaRecta():
    print("Avanzando en línea recta...")
    m.forward()
    time.sleep(0.5)
    while True:
        m.changeSpeedInd(90, 90, 70, 70)
        m.forward()  # Avanzar
        #time.sleep(0.2)
        distanciaCen = u.measureCenter()  # Medir distancia al frente
        distanciaIzq = u.measureLeft()  # Medir distancia a la izquierda
        distanciaDer = u.measureRight()  # Medir distancia a la derecha
        distanciaBastonR = u.measureBaston()
        distanciaBastonL = u.measureBastonLeft()
        
        #print("-----Distancia al frente:", distanciaCen)
        #print("Distancia a la izquierda:", distanciaIzq)
        #print("Distancia a la derecha:", distanciaDer)
        
        if distanciaCen < disLimiteParedFrontal:  # Si detecta un obstáculo al frente
            print("Obstáculo detectado al frente.")
            m.stopcar()  # Detener el avance
            time.sleep(0.5)
            # Determinar hacia dónde girar
            direccionGiro = determinarDireccionGiro()
            #print(direccionGiro)
            m.backward()
            time.sleep(0.3)
            
            if direccionGiro == "izquierda":
                print("Girando a la izquierda...")
                m.turnLeft()  # Girar a la izquierda
                print("Giro completado")
                
            elif direccionGiro == "derecha":
                print("Girando a la derecha...")
                m.turnRight()  # Girar a la derecha
                print("Giro completado")
                
            time.sleep(1.5)
            m.stopcar()
            time.sleep(0.2)
            #elif direccionGiro == "avanzar": 
                #print("Avanzando")
                #m.forward()
                
                
            #time.sleep(0.2)  # Tiempo para completar el giro
            
            #m.stopcar()  # Detenerse después del giro
            #break  # Salir del bucle de avance en línea recta
            
        elif distanciaIzq < disLimiteParedLateral:  # Si detecta un obstáculo a la izquierda
            print("Obstáculo detectado a la izquierda.")
            m.stopcar()
            time.sleep(0.5)
            m.right()
            time.sleep(0.4)
            m.stopcar()
            print("Correccíón hecha")
            #break
            
        elif distanciaDer < disLimiteParedLateral:  # Si detecta un obstáculo a la derecha
            print("Obstáculo detectado a la derecha.")
            m.stopcar()
            time.sleep(0.5)
            m.left()
            time.sleep(0.4)
            m.stopcar()
            print("Correccíón hecha")
        
        elif abs (distanciaBastonR < disLimiteParedLateral) and ((distanciaDer - distanciaBastonR) < 10):  # Si detecta un obstáculo a la izquierda
            print("Obstáculo detectado a la derecha en angulo.")
            m.changeSpeedInd(116, 116, 100, 100)
            m.turnLeft()
            time.sleep(0.1)
            m.stopcar()
            time.sleep(0.1)
            
            print("Distancia a la derecha:", distanciaDer)
            print("Distancia a la baston:", distanciaBastonR)
            
        # elif distanciaDer == 136:  # Si detecta un obstáculo a la izquierda
            # print("Obstáculo detectado a la derecha en angulo.")
            # m.giro45L()
        elif abs (distanciaBastonL < disLimiteParedLateral) and ((distanciaIzq - distanciaBastonL) < 10):  # Si detecta un obstáculo a la izquierda
            print("Obstáculo detectado a la izquierda en angulo.")
            m.changeSpeedInd(116, 116, 100, 100)
            m.turnRight()
            time.sleep(0.1)
            m.stopcar()
            time.sleep(0.1)
            
            print("Distancia a la izquierda:", distanciaIzq)
            print("Distancia a la baston:", distanciaBastonL)
            

# Avanzar durante 1 segundo antes de iniciar el bucle principal
print("Iniciando movimiento hacia adelante...")

# Bucle principal
#while True:
avanzaLineaRecta()  # Llamar a la función para avanzar en línea recta

