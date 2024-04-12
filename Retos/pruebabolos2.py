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
s = Servo(board)
l = IrControllerV2(board)
# Variables globales
disLimiteParedFrontal = 30
disLimiteParedLateral = 16

def abrir():
    s.changeAngle(180)
def cerrar():
    s.changeAngle(0)
def disparo():
    print("DISPARO ")
    abrir()
    
def radar():
    global disIzq
    disIzq = u.measureLeft()
    time.sleep(0.2)
    global disDer
    disDer = u.measureRight()
    time.sleep(0.2)
    global disCen
    disCen = u.measureCenter()
    time.sleep(0.2)
    global disBizq
    disBizq = u.measureBastonLeft()
    time.sleep(0.2)
    global disBder
    disBder = u.measureBaston()
    time.sleep(0.2)
    print("disIzq: ",disIzq," disDer: ",disDer," disCen:", disCen , " disBizq: " , disBizq , " disBder" , disBder)

def correccion():
   radar()
   m.changeSpeedInd(116, 116, 100, 100)
   if abs (disBder < disLimiteParedLateral) and ((disDer - disBder) < 10):  # Si detecta un obstáculo a la izquierda
        print("Obstáculo detectado a la derecha en angulo.")
        
        m.turnLeft()
        time.sleep(0.1)
        m.stopcar()
        time.sleep(0.1)
        
        print("Distancia a la derecha:", disDer)
        print("Distancia a la baston:", disBder)
        
   elif abs (disBizq < disLimiteParedLateral) and ((disIzq - disBizq) < 10):  # Si detecta un obstáculo a la izquierda
        print("Obstáculo detectado a la izquierda en angulo.")
        m.changeSpeedInd(116, 116, 100, 100)
        m.turnRight()
        time.sleep(0.1)
        m.stopcar()
        time.sleep(0.1)
            
        print("Distancia a la izquierda:", disIzq)
        print("Distancia a la baston:", disBizq)

def determinarDireccionGiro():
    radar()
    if disIzq > disDer and disIzq > disCen:
        return "izquierda"
    elif disDer > disIzq and disDer > disCen:
        return "derecha"
           
def inicio():
    m.changeSpeedInd(80, 80, 60, 60)
    radar()
    if disCen < disLimiteParedFrontal:  # Si detecta un obstáculo al frente
            print("Obstáculo detectado al frente.")
            m.stopcar()  # Detener el avance
            time.sleep(0.2)
            # Determinar hacia dónde girar
            direccionGiro = determinarDireccionGiro()
            #print(direccionGiro)
            m.backward()
            time.sleep(0.3)
            
            if direccionGiro == "izquierda":
                print("Girando a la izquierda...")
                m.turnLeft()  # Girar a la izquierda
                time.sleep(1.3)
                m.stopcar()
                print("Giro completado")
                return "break"
            
            
    elif disIzq < disLimiteParedLateral:  # Si detecta un obstáculo a la izquierda
            print("Obstáculo detectado a la izquierda.")
            m.stopcar()
            time.sleep(0.2)
            m.right()
            time.sleep(0.1)
            m.stopcar()
            print("Correccíón hecha")
            #break
            
    elif disDer < disLimiteParedLateral:  # Si detecta un obstáculo a la derecha
            print("Obstáculo detectado a la derecha.")
            m.stopcar()
            time.sleep(0.2)
            m.left()
            time.sleep(0.1)
            m.stopcar()
            print("Correccíón hecha")
        
    elif abs (disBder < disLimiteParedLateral) and ((disDer - disBder) < 20):  # Si detecta un obstáculo a la izquierda
            print("Obstáculo detectado a la derecha en angulo.")
            m.changeSpeedInd(116, 116, 100, 100)
            m.turnLeft()
            time.sleep(0.1)
            m.stopcar()
            
            print("Distancia a la derecha:", disDer)
            print("Distancia a la baston:", disBder)
            
    elif abs (disBizq < disLimiteParedLateral) and ((disIzq - disBizq) < 20):  # Si detecta un obstáculo a la izquierda
            print("Obstáculo detectado a la izquierda en angulo.")
            m.changeSpeedInd(116, 116, 100, 100)
            m.turnRight()
            time.sleep(0.1)
            m.stopcar()
            
            print("Distancia a la izquierda:", disIzq)
            print("Distancia a la baston:", disBizq)
    print("----")
    m.forward()
def centrar():
    margen = 2
    elem = "1"
    while True:
        radar()
        varSen = str(l.sensorval())
        if varSen.find(elem) != -1 and abs(disIzq-disDer) <= margen:
          m.backward()
          time.sleep(0.2)
          m.stopcar()
          return "hecho"
          break
        elif abs(disIzq-disDer) <= margen:
          m.backward()
          time.sleep(0.2)
          m.stopcar()
       
        else:
            varSen = str(l.sensorval())
            if varSen.find(elem) != -1:
            #=======RETROC PEQUENO=======
              m.backward()
              time.sleep(0.2)
              m.stopcar()
            else:
              if disIzq > disDer:
                m.left() #The black line left
                time.sleep(0.2)
                
                correccion()
              elif disIzq < disDer:
                m.right() #The black line right
                time.sleep(0.2)
                
                correccion()

val = int(input("ESTA PUESTA LA BARRA SI(1) NO(0)"))
if (val == '1'):
    time.sleep(1)
else:
    print("abro garra,2 segundos para cierre....")
    abrir()
    time.sleep(2)
    cerrar()
    time.sleep(1)
m.forward()
time.sleep(0.3)
while True:
    print("Haloo")
    giroHecho = str (inicio())
    if giroHecho == "break" :
        print("termino parte 1")
        m.forward()
        time.sleep(0.2)
        m.stopcar()
        break
while True:
    m.forward()
    time.sleep(0.2)
    posicionado = str (centrar())
    if posicionado == "hecho":
        disparo()
        break
        
    