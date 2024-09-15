import cv2
from distance_estimator import FindDistance  # Your distance estimation class
from motionDetector import MotionDetectionWithPyramid  # Your motion detection class
from detect_face import FaceDetector  # Your face detection class

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

    # Detect face
    face_detected = face_detector.detect_face(frame)
    results['face_detected'] = face_detected

    if face_detected == 1:
        # Estimate normalized distance only if face is detected
        normalized_distance = distance_finder.estimate_distance_from_frame(frame)
        if normalized_distance is not None:
            results['normalized_distance'] = normalized_distance
    else:
        results['normalized_distance'] = None  # No face detected, set distance to None

    # Detect motion
    motion_value = motion_detector.detect_motion(frame)
    results['motion_value'] = motion_value

    return results

def calculate_attention_score(normalized_distance, motion_value, face_detected):
    """
    Calculate the likelihood that the user is paying attention based on normalized distance,
    motion intensity, and face detection.
    :param normalized_distance: Normalized distance value (0-1).
    :param motion_value: Motion intensity value (0-1).
    :param face_detected: 1 if a face is detected, -1 if not.
    :return: A score between 0 and 1 indicating how likely the user is paying attention.
    """
    # If no face is detected, return 0 as the attention score
    if face_detected == -1:
        return 0  # No face detected, so no attention

    # Weights for each factor
    w_d = 0.4  # Weight for distance
    w_m = 0.4  # Weight for motion
    w_f = 0.2  # Weight for face detection

    # Calculate the distance score (penalize if too far or too close)
    D_score = 1 - abs(0.5 - normalized_distance) if normalized_distance is not None else 0

    # Calculate the motion score (low motion means paying attention)
    M_score = 1 - motion_value  # Less motion is better

    # Face detection score
    F_score = 1 if face_detected == 1 else 0

    # Calculate the final attention score as a weighted sum
    P_attention = (w_d * D_score) + (w_m * M_score) + (w_f * F_score)

    # Ensure the score is between 0 and 1
    P_attention = max(0, min(P_attention, 1))

    return P_attention

def show_results_on_frame(frame, results):
    """
    Display the results on the frame.
    """
    # Display distance
    if 'normalized_distance' in results and results['normalized_distance'] is not None:
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
        attention_score = calculate_attention_score(
            results.get('normalized_distance'), results['motion_value'], results['face_detected']
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
