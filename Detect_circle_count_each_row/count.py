import cv2
import numpy as np
import mark

# Load the image
image = cv2.imread('circle.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect circles in the image
rows = gray.shape[0]
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                          param1=20, param2=15,
                          minRadius=7, maxRadius=12)

# Define the lower and upper bounds for each color
lower_red = np.array([0, 0, 200])
upper_red = np.array([50, 50, 255])
lower_blue = np.array([200, 0, 0])
upper_blue = np.array([255, 50, 50])
lower_green = np.array([0, 200, 0])
upper_green = np.array([50, 255, 50])

# Create binary masks for each color
red_mask = mark.full_mask
blue_mask = cv2.inRange(image, lower_blue, upper_blue)
green_mask = cv2.inRange(image, lower_green, upper_green)


# Define the size of each block
block_size = (22, 324)

# Loop over each block of the image
for i in range(0, image.shape[0], block_size[0]):
    for j in range(0, image.shape[1], block_size[1]):
        # Get the current block
        block = image[i:i+block_size[0], j:j+block_size[1], :]

        # Apply the color masks to the block
        red_pixels = np.sum(red_mask[i:i+block_size[0], j:j+block_size[1]])
        blue_pixels = np.sum(blue_mask[i:i+block_size[0], j:j+block_size[1]])
        green_pixels = np.sum(green_mask[i:i+block_size[0], j:j+block_size[1]])

        # Initialize counters for each color
        red_count = 0
        blue_count = 0
        green_count = 0

        # Loop over the circles
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                # Check if the circle is in the current block
                if circle[1] >= i and circle[1] < i+block_size[0] and circle[0] >= j and circle[0] < j+block_size[1]:
                    center = (circle[0], circle[1])
                    radius = circle[2]

                    # Check the color of the circle
                    color = 'unknown'
                    if np.sum(red_mask[circle[1], circle[0]]) > 0:
                        color = 'red'
                    elif np.sum(blue_mask[circle[1], circle[0]]) > 0:
                        color = 'blue'
                    elif np.sum(green_mask[circle[1], circle[0]]) > 0:
                        color = 'green'

                    # Increment the counter for the color
                    if color == 'red':
                        red_count += 1
                    elif color == 'blue':
                        blue_count += 1
                    elif color == 'green':
                        green_count += 1

                    # Draw the circle on the image
                    cv2.circle(image, center, radius, (0, 255, 0), 2)

        # Print the results for the block
        print(f"Block ({i},{j}) - Red: {red_count}, Blue: {blue_count}, Green: {green_count}")



# Show the image with circles drawn on it
cv2.imshow('Circles', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
