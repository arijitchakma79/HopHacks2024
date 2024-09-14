from robot.RobotController import RobotController
from actions.ActionManager import ActionManager 
import time

if __name__ == '__main__':
    print("Hello HoyaHacks 2024")

    robot = RobotController()
    robot.turnOnPowerLED()
    
    actionManager = ActionManager(robot)

    while True:
        while not robot.isButton1Pressed():
            time.sleep(0.1)

        robot.turnOnProgramLED()
        actionManager.performAction("TailMotion")

        robot.turnOffProgramLED()
        
    robot.turnOffPowerLED()