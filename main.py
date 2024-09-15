from robot.RobotController import RobotController
from audio.AudioManager import AudioManager
from actions.ActionManager import ActionManager 
import time
import random

import cv2
from inputManager import InputManager
from attentionCalculator import AttentionCalculator

from create_pdf import create_pdf

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
    out = cv2.VideoWriter('output.avi', fourcc, 10.0, (640, 480))

    total_attention_score = 0
    total_motion_intensity = 0
    face_detected_frames = 0
    total_movements = 0

    frame_count = 0

    #while True:
    for t in range(5):
        rawResults = []
        for step in range(35):
            ret, frame = cap.read()
            if not ret:
                continue

            r = inputManager.processFrame(frame)

             # Count face detected frames
            if r['face_detected'] == 1:
                face_detected_frames += 1

            # Count movements when motion intensity exceeds a threshold (e.g., 0.3)
            if r['motion_value'] > 0.3:
                total_movements += 1

            total_motion_intensity += r['motion_value']

            rawResults.append(r)

            debugFrame = inputManager.showResults(frame, r)
            out.write(debugFrame)

        frame_count += 1
        attention = attentionCalculator.calculate(rawResults)
        total_attention_score += attention
        
        print("Attention: " + str(attention))

        # Decision

        possibleActions = ["Meow", "Bark", "Ring", "Horn", "Hello", "Welcome", "Lost", "Attention", "TailMotion", "LookAround", "CrazyRotate"] 
        randomAction = random.choice(possibleActions)

            # Action

        actionManager.performAction(randomAction)


    if frame_count > 0:
        avg_attention_score = total_attention_score / frame_count
        frame_count *= 35
        print(f"Average Attention Score: {avg_attention_score * 100:.2f}%")
        
        # Prepare data for the PDF report
        report_data = {
            'avg_attention_score': avg_attention_score,
            'total_frames': frame_count,
            'face_detected_frames': face_detected_frames,
            'total_movements': total_movements,
            'total_motion_intensity': total_motion_intensity
        }

        # Generate PDF report and save locally
        create_pdf(report_data, filename="user_attention_summary_report.pdf")
    else:
        print("No frames processed.")

    out.release()

while True:
    waitForButton()

    robot.turnOnProgramLED()
    #actionManager.performAction("LookAround")
    runProgram()
    robot.turnOffProgramLED()
    
robot.turnOffPowerLED()
cap.release()