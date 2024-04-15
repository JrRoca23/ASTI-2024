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
#==========================CONFIGURATION===============================
board = pymata4.Pymata4()
m = MotorControllerV2(board)
u = Ultrasonido(board)
l = IrControllerV2(board)
s = Servo(board)
#==========================APP SEMIFINAL===============================
disIzqIni=20
disDerIni=20
avanzarTerminado = 0
short_delay=0.1
long_delay=0.15
disSeguimientoPared = 18
disLimiteParedFrontal = 25
time_correccion=0.025
pared="pRight"
disIzq=20
disDer=20
disCen=100
disAnterior=0
disActual=0

def detectarLinea_thread():
    while True:
        varSen = str(l.sensorval())
        elem = "1"
        if varSen.find(elem) != -1:
            print("se encontro ", varSen)
            global avanzarTerminado
            avanzarTerminado = 1
            break

def avanzaDetectaLinea():
    time.sleep(2.5)

def alinear(disAprox):
    eva=0
    if disAprox==0:
        print("Alineacion 0")
        while eva==0:
            disBaston=int(u.measureBaston())
            time.sleep(0.1)
            disDerecha=int(u.measureRight())
            time.sleep(0.1)
            print(disBaston, "--", disDerecha)
            if disBaston>disDerecha:
                m.turnRight()
                time.sleep(0.03)
                m.stopcar()
                time.sleep(1)
            if disBaston<disDerecha:
                m.turnLeft()
                time.sleep(0.03)
                m.stopcar()
                time.sleep(1)
            disBaston=int(u.measureBaston())
            time.sleep(0.1)
            disDerecha=int(u.measureRight())
            time.sleep(0.1)
            if abs(disBaston-disDerecha)<2:
                eva=1
                break

    if disAprox>0:
        print("alineacion ",disAprox)
        while eva==0:
            disBaston=int(u.measureBaston())
            disDerecha=int(u.measureRight())
            print(disBaston, "--", disDerecha)
            if abs(disBaston-disDerecha)<2 and abs(disDerecha-disAprox)<=2:
                eva=1
                break
            if disAprox>disDerecha:
                m.left()
                time.sleep(0.1)
                m.stopcar()
                time.sleep(0.5)
            if disAprox+2<disDerecha:
                m.right()
                time.sleep(0.1)
                m.stopcar()
                time.sleep(0.5)
            if disBaston>disDerecha:
                m.turnRight()
                time.sleep(0.05)
                m.stopcar()
                time.sleep(0.5)
            if disBaston<disDerecha:
                m.turnLeft()
                time.sleep(0.05)
                m.stopcar()
                time.sleep(0.5)

def giro90(directionV):
    m.changeSpeedInd(116, 116, 110, 110)
    if directionV == 1:
        print("giro 90 right")
        m.giro90R()
    elif directionV == 0:
        print("giro 90 left")
        m.giro90L()

def centrar():
    margen=2
    while True:
        disIzq=u.measureLeft()
        disDer=u.measureRight()
        print(disIzq,"----",disDer)
        if abs(disIzq-disDer) <= margen:
          m.stopcar()
          break
        else:
            if disIzq > disDer:
                m.left() #The black line left
                time.sleep(0.2)
                m.stopcar()
                time.sleep(1)
                alinear(0)
            elif disIzq < disDer:
                m.right() #The black line right
                time.sleep(0.2)
                m.stopcar()
                time.sleep(1)
                alinear(0)

def disparo():
    print("DISPARO ")
    s.changeAngle(180)
        
try:
    s.changeAngle(180)
    ertert = int(input("Se abrió el gancho, coloque el proyectil. Ingrese algún número para cerrar el gancho y continuar..."))
    s.changeAngle(0)
    entradaPared = int(input("Proyectil cargado. Ingrese número de pared a seguir (0-izquierda 1-derecha): "))
    m.forward() #go forward
    time.sleep(1.2)
    m.stopcar()
    disIzqIni=u.measureLeft()
    print(disIzqIni)
    while True:
        disIzq=u.measureLeft()
        if entradaPared == 0:
                if disIzq > 2*disIzqIni:
                        m.stopcar()
                        break
        if entradaPared == 1:
                if disDer > 2*disDerIni:
                        m.stopcar()
                        break
        m.forward()
        time.sleep(0.2)
        m.stopcar()
        time.sleep(0.5)
        alinear(12)
        time.sleep(0.5)
    alinear(12)
    m.forward()
    time.sleep(0.8)
    m.stopcar()
    time.sleep(1)
    alinear(12)
    time.sleep(1)
    giro90(entradaPared)
    #=======AVANCE PEQUENO=======
    print("Avance Pequeno")
    m.forward()
    time.sleep(1)
    m.stopcar()
    #============================
    print("Avanza analizando linea")
    avanzaDetectaLinea()
    m.backward()
    time.sleep(0.7)
    m.stopcar()
    time.sleep(1)

    print("Inicia Centrar")
    centrar()
    print("Termina Centrar")

    #Avan a luego de centrado
    #print("Avanza analizando linea")
    #avanzaDetectaLinea()
    #m.backward()
    #time.sleep(0.2)
    #m.stopcar()
    #time.sleep(1)

    alinear(0)
    time.sleep(1)
    disparo()    
    m.stopcar()

except KeyboardInterrupt:
    m.stopcar()
    exit(0)
