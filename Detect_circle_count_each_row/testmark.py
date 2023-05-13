import cv2
import numpy as np


def get_red_blue_pixels(image_path):
    # Load the image
    image = image_path

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for red and blue colors
    lower_red = np.array([0, 70, 50])
    upper_red = np.array([10, 255, 255])
    lower_blue = np.array([100, 70, 50])
    upper_blue = np.array([130, 255, 255])

    # Create a mask for red and blue colors
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Count the number of red and blue pixels
    red_pixels = np.sum(red_mask == 255)
    blue_pixels = np.sum(blue_mask == 255)

    # Calculate the percentage of red and blue pixels
    total_pixels = image.shape[0] * image.shape[1]
    red_percent = red_pixels / total_pixels * 100
    blue_percent = blue_pixels / total_pixels * 100

    # Check if the image is mostly red or mostly blue
    if red_percent > blue_percent:
        color_result = "mostly red"
    elif blue_percent > red_percent:
        color_result = "mostly blue"
    else:
        color_result = "equal"

    # Return the percentage of red and blue pixels and the color result
    return color_result

