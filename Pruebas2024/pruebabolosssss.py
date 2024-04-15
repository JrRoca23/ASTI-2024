import sys
import time
from pymata4 import pymata4
import numpy as np

from Controller.MotorControllerV2 import MotorControllerV2 
from Controller.UltrasoundControllerV2 import Ultrasonido 
from Controller.IrControllerV2 import IrControllerV2 
from Controller.ServoControllerV2 import Servo

board = pymata4.Pymata4()
m = MotorControllerV2(board)
u = Ultrasonido(board)
l = IrControllerV2(board)
s = Servo(board)

def disparo():
    print("DISPARO ")
    s.changeAngle(180)
def abrir():
    s.changeAngle(180)
    s.changeAngle(0)
try:
    disparo()
    abrir()
except KeyboardInterrupt:
    m.stopcar()
    exit(0)