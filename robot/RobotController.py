from robot.MotorController import MotorController, MotorDirection

class RobotController:
    def __init__(self) -> None:
        self.__leftMotor = MotorController(19, 13)
        self.__rightMotor = MotorController(12, 18)

    def moveForward(self, speed):
        self.__leftMotor.setDirection(MotorDirection.Forward)
        self.__rightMotor.setDirection(MotorDirection.Forward)

        self.__leftMotor.setSpeed(speed)
        self.__rightMotor.setSpeed(speed * 0.95)

    def moveBackward(self, speed):
        self.__leftMotor.setDirection(MotorDirection.Backward)
        self.__rightMotor.setDirection(MotorDirection.Backward)

        self.__leftMotor.setSpeed(speed)
        self.__rightMotor.setSpeed(speed * 0.95)