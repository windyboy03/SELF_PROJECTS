import cv2
import numpy as np

def count_circles(image_path):
    # Load the image
    image = image_path

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect circles in the image
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                          param1=20, param2=15,
                          minRadius=8, maxRadius=12)

    count = 0

    # Loop over the circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            count = count + 1

    return count
