from robot.MotorController import MotorController, MotorDirection
from gpiozero import LED
from gpiozero import Button

class RobotController:
    def __init__(self) -> None:
        self.__leftMotor = MotorController(19, 13)
        self.__rightMotor = MotorController(12, 18, 0.95)

        self.__powerLED = LED(27)
        self.__programLED = LED(17)

        self.__button1 = Button(2)
        self.__button2 = Button(3)

    def turnOnPowerLED(self):
        self.__powerLED.on()

    def turnOffPowerLED(self):
        self.__powerLED.off()

    def turnOnProgramLED(self):
        self.__programLED.on()

    def turnOffProgramLED(self):
        self.__programLED.off()

    def isButton1Pressed(self):
        return self.__button1.is_pressed
    
    def isButton2Pressed(self):
        return self.__button2.is_pressed

    def stop(self):
        self.__leftMotor.stop()
        self.__rightMotor.stop()

    def moveForward(self, speed):
        self.__leftMotor.setDirection(MotorDirection.Forward)
        self.__rightMotor.setDirection(MotorDirection.Forward)

        self.__leftMotor.setSpeed(speed)
        self.__rightMotor.setSpeed(speed)

    def moveBackward(self, speed):
        self.__leftMotor.setDirection(MotorDirection.Backward)
        self.__rightMotor.setDirection(MotorDirection.Backward)

        self.__leftMotor.setSpeed(speed)
        self.__rightMotor.setSpeed(speed)

    def rotateClockwise(self, speed):
        self.__leftMotor.setDirection(MotorDirection.Forward)
        self.__rightMotor.setDirection(MotorDirection.Backward)

        self.__leftMotor.setSpeed(speed)
        self.__rightMotor.setSpeed(speed)

    def rotateCounterClockwise(self, speed):
        self.__leftMotor.setDirection(MotorDirection.Backward)
        self.__rightMotor.setDirection(MotorDirection.Forward)

        self.__leftMotor.setSpeed(speed)
        self.__rightMotor.setSpeed(speed)

    def moveLeftMotor(self, speed, direction):
        self.__leftMotor.setDirection(direction)
        self.__leftMotor.setSpeed(speed)

    def moveRightMotor(self, speed, direction):
        self.__rightMotor.setDirection(direction)
        self.__rightMotor.setSpeed(speed)