from robot.RobotController import RobotController
import time

if __name__ == '__main__':
    print("Hello HoyaHacks 2024")

    robot = RobotController()


    while True:
        robot.moveBackward(50)