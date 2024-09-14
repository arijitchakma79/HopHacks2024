from robot.RobotController import RobotController
from audio.AudioManager import AudioManager
from actions.ActionManager import ActionManager 
import time

if __name__ == '__main__':
    print("Hello HoyaHacks 2024")

    robot = RobotController()
    robot.turnOnPowerLED()
    
    audioManager = AudioManager()

    actionManager = ActionManager(robot, audioManager)

    while True:
        while not robot.isButton1Pressed():
            time.sleep(0.1)

        robot.turnOnProgramLED()
        actionManager.performAction("Meow")

        robot.turnOffProgramLED()
        
    robot.turnOffPowerLED()