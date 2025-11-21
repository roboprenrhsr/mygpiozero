from mygpiozero import Motor, Robot
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

robot = Robot(Motor(23, 24, 12, pin_factory=factory), Motor(5, 6, 13, pin_factory=factory))

try:
    robot.value = (1, 1)

finally:
    robot.close()