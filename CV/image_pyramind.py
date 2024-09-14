import cv2

class ImagePyramid:
    def __init__(self, image, levels=6):
        self.image = image
        self.levels = levels
        self.gaussian_pyramid = []

    def build_gaussian_pyramid(self):
 
        img = self.image.copy()
        self.gaussian_pyramid.append(img)

        for i in range(self.levels - 1):
            img = cv2.pyrDown(img)
            self.gaussian_pyramid.append(img)

        return self.gaussian_pyramid
