import numpy as np
import cv2
import mediapipe as mp

# Initialize MediaPipe Face Detection and Drawing utilities
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Known real-world values for face dimensions and distance from the camera
Known_width = 14.3  # centimeters (average face width)

# Hardcoded focal length (you can adjust this based on experimentation or known camera specs)
Focal_length = 615  # This value is assumed, you can experiment with this based on your setup

# Define minimum and maximum distances for normalization (in centimeters)
min_distance = 20  # Closest distance to the camera (e.g., 20 cm)
max_distance = 200  # Farthest distance from the camera (e.g., 200 cm)

# Color and Font settings
GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
fonts = cv2.FONT_HERSHEY_COMPLEX

class FindDistance:
    def __init__(self, known_width=14.3, focal_length=615, min_dist=20, max_dist=200):
        self.known_width = known_width
        self.focal_length = focal_length
        self.min_dist = min_dist
        self.max_dist = max_dist
        self.face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.75)

    def distance_finder(self, real_face_width, face_width_in_frame):
        """
        Estimate the distance between the camera and the face using the face width in the frame.
        """
        if face_width_in_frame == 0:
            return None  # No face detected
        distance = (real_face_width * self.focal_length) / face_width_in_frame
        return distance
    
    def normalize_distance(self, distance):
        """
        Normalize the distance to a value between 0 and 1 based on the min and max distances.
        """
        normalized_dist = (distance - self.min_dist) / (self.max_dist - self.min_dist)
        # Clamp the value between 0 and 1
        return max(0, min(normalized_dist, 1))

    def face_data(self, image):
        """
        Detects the face in the image and returns its width (in pixels).
        """
        face_width = 0
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB for MediaPipe
        results = self.face_detection.process(img_rgb)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                bbox_width = int(bboxC.width * iw)

                # Draw the face bounding box and landmarks
                mp_drawing.draw_detection(image, detection)

                # Get face width in pixels
                face_width = bbox_width

        return face_width

    def estimate_distance_from_frame(self, frame):
        """
        Estimate the distance of the face in the given frame.
        Returns the normalized distance if a face is detected, otherwise returns None.
        """
        # Detect face width in the current frame
        face_width_in_frame = self.face_data(frame)

        # If a face is detected, calculate the distance
        if face_width_in_frame != 0:
            distance = self.distance_finder(self.known_width, face_width_in_frame)
            normalized_distance = self.normalize_distance(distance)
            return normalized_distance
        return None

