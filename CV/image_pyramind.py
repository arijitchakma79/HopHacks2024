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

            # Ensure the upsampled image matches the size of the previous Gaussian level
            gaussian_expanded = cv2.pyrUp(next_gaussian, dstsize=(self.gaussian_pyramid[i].shape[1], self.gaussian_pyramid[i].shape[0]))

            # Subtract the expanded image from the current level
            laplacian = cv2.subtract(self.gaussian_pyramid[i], gaussian_expanded)
            self.laplacian_pyramid.append(laplacian)

        # The last level of the Laplacian pyramid is the same as the last level of the Gaussian pyramid
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

# Usage example:
image = cv2.imread('new_zealand_lake.jpg')
image_pyramid = ImagePyramid(image, levels=6)
image_pyramid.build_gaussian_pyramid()
image_pyramid.build_laplacian_pyramid()

print(image_pyramid.get_gaussian_pyramid())
print(image_pyramid.get_laplacian_pyramid())
image_pyramid.show_pyramids()
