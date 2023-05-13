import cv2
import numpy as np

def count_circles(image_path):
    # Load the image
    image = cv2.imread(image_path)

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
        for i in circles[0, :]:


            center = (i[0], i[1])
            radius = i[2]
            new_img = np.zeros_like(image)
            cv2.circle(new_img, center, radius, (255, 255, 255), -1)

            # Save new image
            cv2.imshow('circle_area.jpg', new_img)
            cv2.waitKey(0)
    return count
count_circles('circle.jpg')