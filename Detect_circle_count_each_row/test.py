import cv2
import sys
import os
import testmark
import count_circle


if not os.path.exists('patches'):
    os.makedirs('patches')



nRows = int(1)
# Number of columns
mCols = 15

# Reading image
img = cv2.imread('circle1.jpg')
#print img

cv2.imshow('image',img)

# Dimensions of the image
sizeX = img.shape[1]
sizeY = img.shape[0]

print(img.shape)


for i in range(0, nRows):
    for j in range(0, mCols):
        roi = img[i*sizeY//nRows:i*sizeY//nRows + sizeY//nRows, j*sizeX//mCols:j*sizeX//mCols + sizeX//mCols]


        if testmark.get_red_blue_pixels(roi) == 'mostly red':
            print('Red:= ',count_circle.count_circles(roi))
        elif testmark.get_red_blue_pixels(roi) == 'mostly blue':
            print('Blue:= ',count_circle.count_circles(roi))
        elif testmark.get_red_blue_pixels(roi) == 'equal':
            print('None circle detect !')
        cv2.imwrite('patches/patch_'+str(i)+str(j)+".jpg", roi)




cv2.waitKey(0)
cv2.destroyAllWindows()