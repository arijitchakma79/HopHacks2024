import cv2
from distance_estimator import FindDistance  # Your distance estimation class
from motionDetector import MotionDetectionWithPyramid  # Your motion detection class
from detect_face import FaceDetector  # Your face detection class
from get_attention_score import calculate_attention_score
# Constants for distance estimation
Known_width = 14.3  # Average face width in cm
Focal_length = 615  # Assumed focal length
min_distance = 20  # Closest distance (cm)
max_distance = 200  # Farthest distance (cm)

# Initialize the classes
distance_finder = FindDistance(known_width=Known_width, focal_length=Focal_length, min_dist=min_distance, max_dist=max_distance)
motion_detector = MotionDetectionWithPyramid(levels=3)
face_detector = FaceDetector(min_detection_confidence=0.75)

# Initialize the camera
cap = cv2.VideoCapture(0)

# List to store attention scores
attention_scores = []

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

    # Detect face
    face_detected = face_detector.detect_face(frame)
    results['face_detected'] = face_detected

    return results



def show_results_on_frame(frame, results):
    """
    Display the results on the frame.
    """
    # Display distance
    if 'normalized_distance' in results:
        cv2.putText(frame, f"Distance: {round(results['normalized_distance'], 2)}", (30, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display motion detection level
    cv2.putText(frame, f"Motion: {round(results['motion_value'], 2)}", (30, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display face detection status
    face_status = "Face Detected" if results.get('face_detected', -1) == 1 else "No Face Detected"
    cv2.putText(frame, face_status, (30, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

if __name__ == "__main__":
    total_attention_score = 0
    frame_count = 0

    while True:
        # Capture frame from camera
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame for distance and motion
        results = process_frame(frame)

        # Calculate attention score for the current frame
        if 'normalized_distance' in results and 'motion_value' in results and 'face_detected' in results:
            attention_score = calculate_attention_score(
                results['normalized_distance'], results['motion_value'], results['face_detected']
            )
            attention_scores.append(attention_score)

            total_attention_score += attention_score
            frame_count += 1

        # Display results on the frame
        show_results_on_frame(frame, results)

        # Show the frame with annotations
        cv2.imshow("Distance, Motion, and Attention Detection", frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()

    # Output the final average attention score when the program closes
    if frame_count > 0:
        avg_attention_score = total_attention_score / frame_count
        print(f"Average Attention Score: {avg_attention_score:.2f}")
    else:
        print("No frames processed.")
