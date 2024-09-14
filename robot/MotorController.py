from gpiozero import PWMLED
from time import sleep

from enum import Enum

class MotorDirection(Enum):
    Forward = 0
    Backward = 1

class MotorController:
    def __init__(self, forwardPin, backwardPin, correctionFactor = 1) -> None:
        self.__forwardPin = forwardPin
        self.__backwardPin = backwardPin
        self.__correctionFactor = correctionFactor

        self.__forwardPWM = PWMLED(self. __forwardPin)
        self.__backwardPWM = PWMLED(self.__backwardPin)

        self.__motorDirection = MotorDirection.Forward
        self.__currentSpeed = 0

    def setDirection(self, direction):
        self.__motorDirection = direction

    def stop(self):
        self.__forwardPWM.value = 0
        self.__backwardPWM.value = 0

    def setSpeed(self, percent):
        self.__currentSpeed = percent
        value = percent / 100

        value = max(0, value)
        value = min(1, value)

        if self.__motorDirection == MotorDirection.Forward:
            if self.__backwardPWM.value > 0.1:
                self.stop()
                sleep(0.05)

            self.__forwardPWM.value = value * self.__correctionFactor
            self.__backwardPWM.value = 0
        else:
            if self.__forwardPWM.value > 0.1:
                self. stop()
                sleep(0.05)

            self.__forwardPWM.value = 0
            self.__backwardPWM.value = value * self.__correctionFactor