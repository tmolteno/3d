import cv2
import numpy as np 
from matplotlib import pyplot as plt

# read image
img = cv2.imread('1cm.jpg',0)
ret,thresh = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)
height, width = img.shape

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)

cv2.imshow('img', img)
cv2.imshow('thresh', thresh)

cv2.waitKey(0)

#print "height and width : ",height, width
#size = img.size
#print "size of the image in number of pixels", size 
#img3 = cv2.Canny(img, 10, 100, 3)
#nzCount = cv2.countNonZero(img3);
## plot the binary image
#imgplot = plt.imshow(img3, 'gray')
#plt.show()
