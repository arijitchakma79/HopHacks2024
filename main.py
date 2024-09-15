from robot.RobotController import RobotController
from audio.AudioManager import AudioManager
from actions.ActionManager import ActionManager 
import time

import cv2
from inputManager import InputManager

inputManager = InputManager()

robot = RobotController()
robot.turnOnPowerLED()

audioManager = AudioManager()
actionManager = ActionManager(robot, audioManager)

cap = cv2.VideoCapture(0)

def waitForButton():
    while not robot.isButton1Pressed():
            time.sleep(0.1)

def runProgram():
    #actionManager.performAction("LookAround")

    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    for step in range(200):
        ret, frame = cap.read()
        if not ret:
            continue

        rawResults = inputManager.processFrame(frame)
        print(rawResults)

        #debugFrame = inputManager.showResults(frame, rawResults)
        #out.write(debugFrame)

        # Decision

        # Action

    #out.release()

while True:
    waitForButton()

    robot.turnOnProgramLED()
    runProgram()
    robot.turnOffProgramLED()
    
robot.turnOffPowerLED()
cap.release()