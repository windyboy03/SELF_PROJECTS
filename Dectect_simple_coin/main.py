import sys
import cv2 as cv
import numpy as np


def main(argv):
    default_file = 'coin.jpg'
    filename = argv[0] if len(argv) > 0 else default_file

    # Loads image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_COLOR)

    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1



    # Convert to gray
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # DEnoise
    gray = cv.medianBlur(gray, 9)
    cv.imshow(gray)
    cv.waitKey(0)
    #Houghcircles parameter
    rows = gray.shape[0]
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                               param1=300, param2=14,
                               minRadius=120, maxRadius=270)

    # Draw circle
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(src, center, 1, (0, 100, 100), 7)
            # circle outline
            radius = i[2]
            cv.circle(src, center, radius, (255, 0, 255), 7)

    #Save
    cv.imwrite("detected_coins.jpg", src)
    cv.waitKey(0)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])