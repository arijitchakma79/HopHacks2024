import cv2
import numpy as np
import image_pyramind


class MotionDetectionWithPyramid:
    def __init__(self, levels=4):
        self.previous_frame_pyramid = None
        self.levels = levels

    def detect_motion(self, current_frame):
        """
        Detect motion using a Gaussian pyramid.
        """
        # Build the current frame's pyramid
        current_pyramid = image_pyramind.ImagePyramid(current_frame, self.levels).build_gaussian_pyramid()
  

        # If it's the first frame, initialize the previous frame pyramid
        if self.previous_frame_pyramid is None:
            self.previous_frame_pyramid = current_pyramid
            return 0

        total_motion = 0

        # Iterate through each level of the pyramid to compute motion
        for i in range(self.levels):
            current_level = current_pyramid[i]
            previous_level = self.previous_frame_pyramid[i]

            # Convert the current and previous level images to grayscale
            current_gray = cv2.cvtColor(current_level, cv2.COLOR_BGR2GRAY)
            previous_gray = cv2.cvtColor(previous_level, cv2.COLOR_BGR2GRAY)

            # Compute the absolute difference between the current and previous levels
            frame_diff = cv2.absdiff(current_gray, previous_gray)

            # Apply threshold to focus on significant changes
            _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

            # Count the number of pixels where motion is detected
            motion_pixels = np.sum(thresh > 0)

            # Normalize the motion intensity for each level
            motion_intensity = (motion_pixels / float(current_gray.size)) * 10

            total_motion += motion_intensity

        # Normalize total motion across all levels
        total_motion = min(total_motion / self.levels, 1)

        # Update the previous frame pyramid for the next comparison
        self.previous_frame_pyramid = current_pyramid

        return total_motion

    def show_image(self, image):
        """
        Display the current frame.
        """
        cv2.imshow('Motion Detection', image)
        cv2.waitKey(1)

# Example of how to use this class with a webcam feed
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    motion_detector = MotionDetectionWithPyramid(levels=3)

    while True:
        # Read each frame from the webcam
        ret, frame = cap.read()

        if not ret:
            break

        # Detect motion in the current frame using a pyramid approach
        motion_value = motion_detector.detect_motion(frame)

        # Print the amount of motion (0 to 1)
        print(f"Motion level: {motion_value:.2f}")

        # Display the current frame
        motion_detector.show_image(frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
