import numpy as np
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

class AttentionCalculator:
    def __init__(self) -> None:
        self.__distanceWeight = 0.75
        self.__motionWeight = 0.25
        self.__detectionWeight = 1

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

        lackOfAttention = medianDistance * self.__distanceWeight + medianMotion * self.__motionWeight + meanDetection * self.__detectionWeight
        lackOfAttention =  (sigmoid(lackOfAttention) + 1) / 2

        print(str(medianDistance) + " " + str(medianMotion) + " " + str(meanDetection) + " " + str(lackOfAttention))