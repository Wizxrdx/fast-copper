import cv2
import numpy as np


class extract:
    def __init__(self, path):
        # Load the image
        self.path = path
        image = cv2.imread(path)

        # Threshold the image to create a mask where non-white pixels are detected
        _, mask = cv2.threshold(image, 240, 255, cv2.THRESH_BINARY)

        # Find the coordinates of non-white pixels
        non_white_pixels = np.column_stack(np.where(mask != 255))

        # Find the uppermost, lowermost, leftmost, and rightmost non-white pixels
        if len(non_white_pixels) > 0:
            uppermost_pixel = non_white_pixels[np.argmin(non_white_pixels[:, 0])]
            lowermost_pixel = non_white_pixels[np.argmax(non_white_pixels[:, 0])]
            leftmost_pixel = non_white_pixels[np.argmin(non_white_pixels[:, 1])]
            rightmost_pixel = non_white_pixels[np.argmax(non_white_pixels[:, 1])]

            # Crop the region inside the bounding box (before drawing the green box)
            cropped_image = image[uppermost_pixel[0]:lowermost_pixel[0], leftmost_pixel[1]:rightmost_pixel[1]]

            # Save the cropped image as a JPEG file
            cropped_image = self.add_white_border(self.resize_to_square_with_padding(cropped_image, (22, 22)))
            cv2.imwrite(path, cropped_image)

    def getPath(self):
        return self.path

    def resize_to_square_with_padding(self, image, target_size):
        # Get the dimensions of the input image
        height, width, _ = image.shape

        # Determine the side length of the square
        side_length = max(height, width)

        # Create a white canvas of the desired target size
        canvas = np.ones((side_length, side_length, 3), dtype=np.uint8) * 255

        # Calculate the coordinates to place the input image in the center of the canvas
        y_offset = (side_length - height) // 2
        x_offset = (side_length - width) // 2

        # Place the input image onto the canvas
        canvas[y_offset:y_offset + height, x_offset:x_offset + width] = image

        # Resize the canvas to the target size
        resized_image = cv2.resize(canvas, target_size)

        return resized_image

    def add_white_border(self, image, border_size=3):
        # Get the dimensions of the input image
        height, width, _ = image.shape

        # Calculate the new dimensions for the bordered image
        new_height = height + 2 * border_size
        new_width = width + 2 * border_size

        # Create a white canvas of the new dimensions
        bordered_image = np.ones((new_height, new_width, 3), dtype=np.uint8) * 255

        # Calculate the coordinates to place the input image in the center of the canvas
        y_offset = border_size
        x_offset = border_size

        # Place the input image onto the canvas
        bordered_image[y_offset:y_offset + height, x_offset:x_offset + width] = image

        return bordered_image