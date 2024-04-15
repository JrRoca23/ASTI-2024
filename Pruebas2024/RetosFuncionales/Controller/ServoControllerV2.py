from pymata4 import pymata4
import time
import RPi.GPIO as GPIO
class Servo:
    def __init__(self, boardE):
        self.board = boardE
        self.board.set_pin_mode_servo(35)
        self.board.set_pin_mode_digital_output(33)
        self.board.servo_write(35, 180)
        self.board.digital_write(33,1)
        
    def changeAngle(self, angle):
        angle = int(angle)
        self.board.servo_write(35, angle)
board = pymata4.Pymata4()
servo_instance = Servo(board)
board.shutdown()