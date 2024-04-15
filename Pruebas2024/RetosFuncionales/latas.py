from pymata4 import pymata4
import time
from Controller.MotorControllerV2 import MotorControllerV2 

board = pymata4.Pymata4()
m = MotorControllerV2(board)
pausa = 0.025

while True:
    m.changeSpeedInd(120, 120, 70, 70)
    m.forward()
    time.sleep(pausa)
    m.turnRight()
    time.sleep(0.4)
    
    pausa += 0.025
