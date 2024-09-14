import cv2
import numpy as np

class ImagePyramid:
    def __init__(self, image, levels=6):
        self.image = image
        self.levels = levels
        self.gaussian_pyramid = []
        self.laplacian_pyramid = []

    def build_gaussian_pyramid(self):

        img = self.image.copy()
        self.gaussian_pyramid.append(img)

        for i in range(self.levels - 1):
            img = cv2.pyrDown(img)
            self.gaussian_pyramid.append(img)

    def build_laplacian_pyramid(self):
        """
        Builds a Laplacian pyramid by subtracting the upsampled version of each Gaussian level.
        """
        self.build_gaussian_pyramid()
        for i in range(self.levels - 1):
            next_gaussian = self.gaussian_pyramid[i + 1]

            
            gaussian_expanded = cv2.pyrUp(next_gaussian, dstsize=(self.gaussian_pyramid[i].shape[1], self.gaussian_pyramid[i].shape[0]))

           
            laplacian = cv2.subtract(self.gaussian_pyramid[i], gaussian_expanded)
            self.laplacian_pyramid.append(laplacian)

        self.laplacian_pyramid.append(self.gaussian_pyramid[-1])


    def get_gaussian_pyramid(self):
        return self.gaussian_pyramid

    def get_laplacian_pyramid(self):
        return self.laplacian_pyramid

    def show_pyramids(self):
        """
        Displays the Gaussian and Laplacian pyramids.
        """
        # Display Gaussian Pyramid
        print("Gaussian Pyramid:")
        for i, img in enumerate(self.gaussian_pyramid):
            cv2.imshow(f'Gaussian Level {i}', img)

        # Display Laplacian Pyramid
        print("Laplacian Pyramid:")
        for i, img in enumerate(self.laplacian_pyramid):
            cv2.imshow(f'Laplacian Level {i}', img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

