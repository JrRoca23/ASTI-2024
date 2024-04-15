import time

from pymata4 import pymata4
from Controller.MotorControllerV2 import MotorControllerV2
from Controller.IrControllerV2 import IrControllerV2 
#==========================CONFIGURATION===============================
# Configuración
board = pymata4.Pymata4()
m = MotorControllerV2(board)
i = IrControllerV2(board)
#==========================APP Pruebas=================================

def follow_line():
    
    while True:
      m.changeSpeedInd(120, 120, 70, 70)
      m.forward()
        
    
        
follow_line()

