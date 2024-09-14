import cv2
import numpy as np
import distance_estimator
import motionDetector
import detect_face

# Constants for distance estimation
Known_width = 14.3  # centimeters (average face width)
Focal_length = 615  # Assumed focal length
min_distance = 20  # Closest distance to the camera (e.g., 20 cm)
max_distance = 200  # Farthest distance from the camera (e.g., 200 cm)

# Initialize the distance finder and motion detection classes
distance_finder = distance_estimator.FindDistance(known_width=Known_width, focal_length=Focal_length, min_dist=min_distance, max_dist=max_distance)
motion_detector = motionDetector.MotionDetectionWithPyramid(levels=3)
face_detector = detect_face.FaceDetector(min_detection_confidence=0.75)

# Initialize camera
cap = cv2.VideoCapture(0)

def process_frame(frame):
    """
    Process the current frame for both distance estimation and motion detection.
    Return a dictionary of the results.
    """
    results = {}

    # Estimate normalized distance
    normalized_distance = distance_finder.estimate_distance_from_frame(frame)
    if normalized_distance is not None:
        results['normalized_distance'] = normalized_distance

    # Detect motion
    motion_value = motion_detector.detect_motion(frame)
    results['motion_value'] = motion_value

    face_detected = face_detector.detect_face(frame)
    results['face_detected'] = face_detected

    return results

def show_results_on_frame(frame, results):
    """
    Display the results on the current frame.
    """
    # Display normalized distance on the frame
    if 'normalized_distance' in results:
        cv2.line(frame, (30, 30), (230, 30), (0, 0, 255), 32)
        cv2.line(frame, (30, 30), (230, 30), (0, 0, 0), 28)
        cv2.putText(frame, f"Distance: {round(results['normalized_distance'], 2)}", (30, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display motion detection level on the frame
    cv2.line(frame, (30, 60), (230, 60), (0, 0, 255), 32)
    cv2.line(frame, (30, 60), (230, 60), (0, 0, 0), 28)
    cv2.putText(frame, f"Motion: {round(results['motion_value'], 2)}", (30, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

if __name__ == "__main__":
    while True:
        # Read frame from camera
        ret, frame = cap.read()
        if not ret:
            break

        # Process the current frame for distance and motion detection
        results = process_frame(frame)
        print(results)

        # Display results on the frame
        show_results_on_frame(frame, results)

        # Show the frame with annotations
        cv2.imshow("Distance and Motion Detection", frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()
