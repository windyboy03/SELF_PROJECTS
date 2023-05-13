import sys
import cv2 as cv
import numpy as np

def main(default_file):
    default_file = 'circle1.jpg'


    # Loads image
    src = cv.imread(cv.samples.findFile(default_file), cv.IMREAD_COLOR)

    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1


    # Convert to gray
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # DEnoise
    gray = cv.medianBlur(gray, 1)
    cv.imshow('red', gray)
    cv.waitKey(0)
    #Houghcircles parameter
    rows = gray.shape[0]
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                               param1=20, param2=15,
                               minRadius=8, maxRadius=12)
    cir = []

    # Draw circle
    if circles is not None:
        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            center = (i[0], i[1])
            print(center)

            # circle center
            cv.circle(src, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(src, center, radius, (255, 0, 255), 1)
    print(cir)
    #Save
    cv.imwrite("detected_coins.jpg", src)
    cv.waitKey(0)

    return 0

main('circle1.jpg')


# Suppose you have the circle centers in the `circles` list
# circles = [(x1, y1), (x2, y2), ...]

# 1. Sort the circles by their y-coordinate
circles_sorted = sorted(cir, key=lambda c: c[1])

# 2. Define a threshold distance between the centers to consider them as part of the same row
d = 20

# 3. For each row, find the center that is closest to the top of the row
rows = []
for c in circles_sorted:
    found_row = False
    for row in rows:
        if abs(c[1] - row[0][1]) <= d:
            row.append(c)
            found_row = True
            break
    if not found_row:
        rows.append([c])

# 4. Find the center that is closest to the bottom of the row
for row in rows:
    row.sort(key=lambda c: c[1])
    top_center = row[0]
    bottom_center = row[-1]
    # 5. Count the number of points that lie between the starting and ending points of the row
    n_points = sum(1 for c in circles_sorted if top_center[1] <= c[1] <= bottom_center[1] and abs(c[0] - top_center[0]) <= d)
    print(f"Row {row[0][1]}-{row[-1][1]}: {n_points} points")
