import cv2
import numpy as np

class MotionDetection:
    def __init__(self, threshold):
        self.previous_frame = None
        self.threshold = threshold

    def detect_motion(self, current_frame):

        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.previous_frame is None:
            self.previous_frame = gray
            return 0

        frame_diff = cv2.absdiff(gray, self.previous_frame)

        self.previous_frame = gray

        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

        motion_pixels = np.sum(thresh > 0)

        motion_intensity = (motion_pixels / float(gray.size)) * 10  

        if motion_intensity < self.threshold:
            motion_intensity = 0
        
        elif motion_intensity > 1:
            motion_intensity = 1

        return motion_intensity

    def show_image(self, image):

        cv2.imshow('Motion Detection', image)
        cv2.waitKey(1)


