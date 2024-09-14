import cv2
import mediapipe as mp

# Initialize MediaPipe Face Mesh solution
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Initialize FaceMesh model
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5, refine_landmarks=True)

def getLandmarks(image, face_mesh):
    # Convert the BGR image to RGB before processing.
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgb.flags.writeable = False
    results = face_mesh.process(image_rgb)
    return results

def isLookingAtCenter(eye_left_corner, eye_right_corner, iris_center, threshold=0.2):
    # Calculate the width of the eye (distance between the corners)
    eye_width = eye_right_corner[0] - eye_left_corner[0]
    
    # Calculate the center of the eye
    eye_center_x = (eye_left_corner[0] + eye_right_corner[0]) / 2
    
    # Calculate normalized position of the iris relative to the eye width
    iris_offset = (iris_center[0] - eye_center_x) / eye_width
    
    # If the iris offset is within the threshold range, it's centered
    if abs(iris_offset) < threshold:
        return 'Center'
    else:
        return 'Not Center'

def getEyeCorners(landmarks, left_indices, right_indices):
    # Get the coordinates of the left and right corners of the eye
    eye_left = [landmarks[left_indices].x, landmarks[left_indices].y]
    eye_right = [landmarks[right_indices].x, landmarks[right_indices].y]
    return eye_left, eye_right

def getIrisCenter(landmarks, iris_indices):
    # Get the center of the iris by averaging the iris landmarks
    iris_x = [landmarks[idx].x for idx in iris_indices]
    iris_y = [landmarks[idx].y for idx in iris_indices]
    iris_center = [sum(iris_x) / len(iris_x), sum(iris_y) / len(iris_y)]
    return iris_center

def drawMarkers(frame, eye_left_corner, eye_right_corner, iris_center):
    # Convert the normalized landmark positions to pixel coordinates
    h, w, _ = frame.shape
    eye_left_px = (int(eye_left_corner[0] * w), int(eye_left_corner[1] * h))
    eye_right_px = (int(eye_right_corner[0] * w), int(eye_right_corner[1] * h))
    iris_center_px = (int(iris_center[0] * w), int(iris_center[1] * h))

    # Draw markers for the eye corners and iris
    cv2.circle(frame, eye_left_px, 3, (255, 0, 0), -1)  # Blue for left corner
    cv2.circle(frame, eye_right_px, 3, (255, 0, 0), -1)  # Blue for right corner
    cv2.circle(frame, iris_center_px, 3, (0, 255, 0), -1)  # Green for iris center

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 420)  # height
cap.set(10, 100)  # brightness

while True:
    success, frame = cap.read()
    if not success:
        print('Ignoring empty camera frame.')
        continue
    
    # Flip the video horizontally for natural interaction
    frame = cv2.flip(frame, 1)

    # Get the landmarks and results from the face mesh
    results = getLandmarks(frame, face_mesh)
    
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        # Define eye corner landmarks (SWAP them after flipping the frame)
        left_eye_corners = (362, 263)  # Swapped after flip
        right_eye_corners = (33, 133)  # Swapped after flip

        # Define iris landmarks (SWAP them after flipping the frame)
        left_iris_indices = [469, 470, 471, 472]  # Swapped after flip
        right_iris_indices = [474, 475, 476, 477]  # Swapped after flip

        # Get eye corners and iris center for left eye
        left_eye_left_corner, left_eye_right_corner = getEyeCorners(landmarks, left_eye_corners[0], left_eye_corners[1])
        left_iris_center = getIrisCenter(landmarks, left_iris_indices)

        # Get eye corners and iris center for right eye
        right_eye_left_corner, right_eye_right_corner = getEyeCorners(landmarks, right_eye_corners[0], right_eye_corners[1])
        right_iris_center = getIrisCenter(landmarks, right_iris_indices)

        # Check if user is looking at the center for both eyes
        left_eye_status = isLookingAtCenter(left_eye_left_corner, left_eye_right_corner, left_iris_center)
        right_eye_status = isLookingAtCenter(right_eye_left_corner, right_eye_right_corner, right_iris_center)

        # Draw markers on the left and right eyes
        drawMarkers(frame, left_eye_left_corner, left_eye_right_corner, left_iris_center)
        drawMarkers(frame, right_eye_left_corner, right_eye_right_corner, right_iris_center)

        # Display the status on the frame (for both eyes)
        cv2.putText(frame, f'Left Eye: {left_eye_status}', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Right Eye: {right_eye_status}', (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show the webcam frame
        cv2.imshow('Iris Center Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera resources and close windows
cap.release()
cv2.destroyAllWindows()
face_mesh.close()
