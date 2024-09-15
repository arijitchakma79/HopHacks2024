import cv2
import numpy as np
from CV import distance_estimator
from CV import motionDetector
from CV import detect_face

class InputManager():
    def __init__(self) -> None:
        self.__knownWidth = 14.3  # centimeters (average face width)
        self.__focalLength = 615  # Assumed focal length
        self.__minDistance = 20  # Closest distance to the camera (e.g., 20 cm)
        self.__maxDistance = 200  # Farthest distance from the camera (e.g., 200 cm)

        self.__distanceFinder = distance_estimator.FindDistance(known_width=self.__knownWidth, focal_length=self.__focalLength, min_dist=self.__minDistance, max_dist=self.__maxDistance)
        self.__motionDetector = motionDetector.MotionDetectionWithPyramid(levels=3)
        self.__faceDetector = detect_face.FaceDetector(min_detection_confidence=0.75)

    def processFrame(self, frame):
        """
        Process the current frame for both distance estimation and motion detection.
        Return a dictionary of the results.
        """
        results = {}

        # Estimate normalized distance
        normalized_distance = self.__distanceFinder.estimate_distance_from_frame(frame)
        if normalized_distance is not None:
            results['normalized_distance'] = normalized_distance

        # Detect motion
        motion_value = self.__motionDetector.detect_motion(frame)
        results['motion_value'] = motion_value

        face_detected = self.__faceDetector.detect_face(frame)
        results['face_detected'] = face_detected

        return results
    
    def showResults(self, frame, results):
        """
        Display the results on the current frame.
        """

        debugFrame = frame.copy()

        # Display normalized distance on the frame
        if 'normalized_distance' in results:
            cv2.line(debugFrame, (30, 30), (230, 30), (0, 0, 255), 32)
            cv2.line(debugFrame, (30, 30), (230, 30), (0, 0, 0), 28)
            cv2.putText(debugFrame, f"Distance: {round(results['normalized_distance'], 2)}", (30, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Display motion detection level on the frame
        cv2.line(debugFrame, (30, 60), (230, 60), (0, 0, 255), 32)
        cv2.line(debugFrame, (30, 60), (230, 60), (0, 0, 0), 28)
        cv2.putText(debugFrame, f"Motion: {round(results['motion_value'], 2)}", (30, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        return debugFrame