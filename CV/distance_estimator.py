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

# Color and Font settings
GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
fonts = cv2.FONT_HERSHEY_COMPLEX

class FindDistance:
    def __init__(self, known_width=14.3, focal_length=615):
        self.known_width = known_width
        self.focal_length = focal_length
        self.face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.75)

    def distance_finder(self, real_face_width, face_width_in_frame):
        """
        Estimate the distance between the camera and the face using the face width in the frame.
        """
        if face_width_in_frame == 0:
            return None  # No face detected
        distance = (real_face_width * self.focal_length) / face_width_in_frame
        return distance
    
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
        Returns the distance if a face is detected, otherwise returns None.
        """
        # Detect face width in the current frame
        face_width_in_frame = self.face_data(frame)

        # If a face is detected, calculate the distance
        if face_width_in_frame != 0:
            distance = self.distance_finder(self.known_width, face_width_in_frame)
            return distance
        return None

if __name__ == "__main__":
    # Create an instance of the FindDistance class
    distance_finder = FindDistance(known_width=Known_width, focal_length=Focal_length)

    # Initialize camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read frame from camera
        ret, frame = cap.read()
        if not ret:
            break

        # Estimate distance for the current frame
        distance = distance_finder.estimate_distance_from_frame(frame)

        # If distance is detected, display it on the frame
        if distance is not None:
            # Draw background for the text
            cv2.line(frame, (30, 30), (230, 30), RED, 32)
            cv2.line(frame, (30, 30), (230, 30), BLACK, 28)

            # Display the estimated distance on the frame
            cv2.putText(frame, f"Distance: {round(distance, 2)} CM", (30, 35), fonts, 0.6, GREEN, 2)

        # Show the frame
        cv2.imshow("Distance Estimation", frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()
