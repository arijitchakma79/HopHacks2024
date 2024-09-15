from robot.RobotController import RobotController
from audio.AudioManager import AudioManager
from actions.ActionManager import ActionManager 
import time
import random

import cv2
from inputManager import InputManager
from attentionCalculator import AttentionCalculator

inputManager = InputManager()
attentionCalculator = AttentionCalculator()

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

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    #while True:
    for t in range(1000):
        rawResults = []
        for step in range(35):
            ret, frame = cap.read()
            if not ret:
                continue

            r = inputManager.processFrame(frame)
            rawResults.append(r)

            debugFrame = inputManager.showResults(frame, r)
            out.write(debugFrame)


        attention = attentionCalculator.calculate(rawResults)
        print(attention)

        # Decision

        possibleActions = ["Meow", "Bark", "Ring", "Horn", "Hello", "Welcome", "Lost", "Attention", "TailMotion", "LookAround", "CrazyRotate"] 
        randomAction = random.choice(possibleActions)

            # Action

        actionManager.performAction(randomAction)

    out.release()

while True:
    waitForButton()

    robot.turnOnProgramLED()
    #actionManager.performAction("LookAround")
    runProgram()
    robot.turnOffProgramLED()
    
robot.turnOffPowerLED()
cap.release()