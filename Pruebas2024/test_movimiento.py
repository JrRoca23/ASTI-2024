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

def draw():
    m.changeSpeedInd(90, 90, 62, 62)
    m.right()
    time.sleep(3)
    m.stopcar()
    
draw()
 

