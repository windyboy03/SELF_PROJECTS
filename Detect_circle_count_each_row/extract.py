import cv2
import numpy as np
import testmark

def extract_objects_from_circles(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # DEnoise
    gray = cv2.medianBlur(gray, 1)

    #Houghcircles parameter
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=20, param2=15,
                               minRadius=8, maxRadius=12)
    new_circle = []
    # Extract objects from each circle
    circles = np.uint16(np.around(circles))
    for circle in circles[0]:
        # Get circle coordinates and radius
        x, y, r = circle.astype(np.int64)

        # Create a circular mask
        mask = np.zeros_like(gray)
        cv2.circle(mask, (x, y), r, 255, -1)

        # Apply mask to the original image to extract the object
        object = cv2.bitwise_and(img, img, mask=mask)
        if testmark.get_red_blue_pixels(object) == 'mostly red':
            circle[2] = 0
            new_circle.append(circle)
        elif testmark.get_red_blue_pixels(object) == 'mostly blue':
            circle[2] = 1
            new_circle.append(circle)
        # Show the extracted object
        #cv2.imshow('Object.jpg', object)
        #cv2.waitKey(0)
    return new_circle

