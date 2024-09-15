import numpy as np
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

class AttentionCalculator:
    def __init__(self) -> None:
        self.__distanceWeight = 0.75
        self.__motionWeight = 0.25

    def calculate(self, rawResults):
        distances = []
        motions = []
        detections = []
        for result in rawResults:
            motions.append(result["motion_value"])
            detections.append(result["face_detected"])

            if(result["face_detected"] == 1):
                distances.append(result["normalized_distance"])

        distances = np.array(distances)
        motions = np.array(motions)

        if(len(distances) == 0):
            medianDistance = 0
        else:
            medianDistance = np.median(distances)
        medianMotion = np.median(motions)
        meanDetection = sum(detections)

            # If no face is detected, return 0 as the attention score
        if meanDetection < 0:
            return 0  # No face detected, so no attention

        # Weights for each factor
        w_d = 0.4  # Weight for distance
        w_m = 0.4  # Weight for motion
        w_f = 0.2  # Weight for face detection

        # Calculate the distance score (penalize if too far or too close)
        D_score = 1 - abs(0.5 - medianDistance)  # Ideal is around 0.5

        # Calculate the motion score (low motion means paying attention)
        M_score = 1 - medianMotion  # Less motion is better

        # Face detection score
        F_score = 1 if meanDetection > 0 else 0

        # Calculate the final attention score as a weighted sum
        P_attention = (w_d * D_score) + (w_m * M_score) + (w_f * F_score)

        # Ensure the score is between 0 and 1
        P_attention = max(0, min(P_attention, 1))

        return P_attention

        #print(str(medianDistance) + " " + str(medianMotion) + " " + str(meanDetection) + " " + str(lackOfAttention))