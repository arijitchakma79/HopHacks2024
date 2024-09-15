import cv2
from distance_estimator import FindDistance  #  distance estimation class
from motionDetector import MotionDetectionWithPyramid  # motion detection class
from detect_face import FaceDetector  #  face detection class
from create_pdf import create_pdf
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
    total_motion_intensity = 0
    face_detected_frames = 0
    total_movements = 0

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

        # Accumulate the attention score and other metrics
        total_attention_score += attention_score
        total_motion_intensity += results['motion_value']

        # Count face detected frames
        if results['face_detected'] == 1:
            face_detected_frames += 1

        # Count movements when motion intensity exceeds a threshold (e.g., 0.3)
        if results['motion_value'] > 0.3:
            total_movements += 1

        frame_count += 1

        # Show the frame with annotations
        show_results_on_frame(frame, results)

        # Display frame
        cv2.imshow("Distance, Motion, and Attention Detection", frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()

    # Output the final report when the program closes
    if frame_count > 0:
        avg_attention_score = total_attention_score / frame_count
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