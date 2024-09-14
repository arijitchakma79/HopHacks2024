from robot.MotorController import MotorController, MotorDirection
from gpiozero import LED, Button, DistanceSensor
import time

class RobotController:
    def __init__(self) -> None:
        self.__leftMotor = MotorController(19, 13)
        self.__rightMotor = MotorController(12, 18, 0.95)

        self.__powerLED = LED(27)
        self.__programLED = LED(17)

        self.__button1 = Button(2)
        self.__button2 = Button(3)

        self.__obstacleSensor = DistanceSensor(22, 4)
        self.__floorSensor = DistanceSensor(26, 5)

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

    def getObstacleDistance(self):
        return self.__obstacleSensor.distance
    
    def getFloorDistance(self):
        return self.__floorSensor.distance

    def safeWait(self, milliseconds):
        warningCount = 0
        for t in range(milliseconds):
            time.sleep(0.001)
            
            print(self.getObstacleDistance())
            if(self.__leftMotor.getDirection() == MotorDirection.Forward and self.__rightMotor.getDirection() == MotorDirection.Forward): 
                if(self.getObstacleDistance() < 0.35):
                    warningCount+=1

                #if(self.getFloorDistance() > 0.3):
                #    warningCount+=1
            
            if(warningCount > 25):
                    self.stop()
                    break

           