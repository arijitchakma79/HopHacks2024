import cv2
import mediapipe as mp

class FaceDetector:
    def __init__(self, min_detection_confidence=0.5):
        """
        Initialize the FaceDetector class.
        :param min_detection_confidence: Minimum confidence value for face detection.
        """
        self.face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=min_detection_confidence)

    def detect_face(self, frame):
        """
        Detect a face in the frame.
        :param frame: The frame in which to detect the face.
        :return: 1 if a face is detected, -1 if no face is found.
        """
        # Convert the frame from BGR to RGB as MediaPipe requires RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Perform face detection
        results = self.face_detection.process(rgb_frame)

        # Check if faces are detected
        if results.detections:
            return 1  # Face detected
        else:
            return -1  # No face detected

    def release(self):
        """
        Release any resources used by the class.
        """
        self.face_detection = None

if __name__ == "__main__":
    # Initialize the face detector
    face_detector = FaceDetector(min_detection_confidence=0.75)

    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Detect face in the frame
        result = face_detector.detect_face(frame)
        print(result)
        # Display the result on the frame
        if result == 1:
            cv2.putText(frame, 'Face Detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'No Face Detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Show the frame
        cv2.imshow('Face Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()
    face_detector.release()
