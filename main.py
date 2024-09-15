from robot.RobotController import RobotController
from audio.AudioManager import AudioManager
from actions.ActionManager import ActionManager 
import time
import random

import cv2
from inputManager import InputManager
from attentionCalculator import AttentionCalculator

import numpy as np
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

class QLearning:
    def __init__(self, n_actions, learning_rate=0.1, discount_factor=0.95, exploration_rate=0.3):
        self.n_actions = n_actions
        self.q_table = np.zeros(n_actions)
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.action_counts = np.zeros(n_actions)

    def choose_action(self):
        if np.random.random() < self.epsilon:
            # Exploration: choose randomly, but favor less-chosen actions
            probabilities = 1 / (self.action_counts + 1)
            probabilities /= probabilities.sum()
            return np.random.choice(self.n_actions, p=probabilities)
        else:
            # Exploitation: add small random noise to break ties randomly
            noisy_q_values = self.q_table + np.random.normal(0, 0.01, self.n_actions)
            return np.argmax(noisy_q_values)

    def update(self, action, reward):
        self.action_counts[action] += 1
        best_next_q = np.max(self.q_table)
        td_target = reward + self.gamma * best_next_q
        td_error = td_target - self.q_table[action]
        self.q_table[action] += self.lr * td_error

    def decay_epsilon(self, decay_rate=0.9995):
        self.epsilon = max(0.05, self.epsilon * decay_rate)  # Maintain a minimum exploration rate


n_actions = 11  # Number of discrete choices
agent = QLearning(n_actions)

def runProgram():
    #actionManager.performAction("LookAround")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 10.0, (640, 480))

    total_attention_score = 0
    total_motion_intensity = 0
    face_detected_frames = 0
    total_movements = 0

    frame_count = 0

    
    possibleActions = ["Meow", "Bark", "Ring", "Horn", "Hello", "Welcome", "Lost", "Attention", "TailMotion", "LookAround", "CrazyRotate"] 
    random.shuffle(possibleActions)
    

    #while True:
    for t in range(10):
        action = agent.choose_action()

        #randomAction = random.choice(possibleActions)
        actionStr = possibleActions[action]

            # Action

        actionManager.performAction(actionStr)

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

        agent.update(action, attention)
   


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