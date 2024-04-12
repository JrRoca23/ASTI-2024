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
disLimiteParedFrontal = 10
disLimiteParedLateral = 12

def abrir():
    s.changeAngle(180)
def cerrar():
    s.changeAngle(0)
def disparo():
    print("DISPARO ")
    abrir()
    
m.turnLeft()
time.sleep(0.6)
m.stopcar()
    

        