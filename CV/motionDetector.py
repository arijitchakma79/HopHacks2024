import cv2
import numpy as np
from CV import image_pyramind

class MotionDetectionWithPyramid:
    def __init__(self, levels=4):
        self.previous_frame_pyramid = None
        self.levels = levels

    def detect_motion(self, current_frame):

        current_pyramid = image_pyramind.ImagePyramid(current_frame, self.levels).build_gaussian_pyramid()
  
        if self.previous_frame_pyramid is None:
            self.previous_frame_pyramid = current_pyramid
            return 0

        total_motion = 0

        for i in range(self.levels):
            current_level = current_pyramid[i]
            previous_level = self.previous_frame_pyramid[i]

            current_gray = cv2.cvtColor(current_level, cv2.COLOR_BGR2GRAY)
            previous_gray = cv2.cvtColor(previous_level, cv2.COLOR_BGR2GRAY)

            frame_diff = cv2.absdiff(current_gray, previous_gray)

            _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

            motion_pixels = np.sum(thresh > 0)

            motion_intensity = (motion_pixels / float(current_gray.size)) * 10

            total_motion += motion_intensity

        total_motion = min(total_motion / self.levels, 1)

        self.previous_frame_pyramid = current_pyramid

        return total_motion

    def show_image(self, image):

        cv2.imshow('Motion Detection', image)
        cv2.waitKey(1)


