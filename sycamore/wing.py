import cv2
import numpy as np 
from matplotlib import pyplot as plt

# read image
img = cv2.imread('1cm.jpg',0)
ret,thresh = cv2.threshold(img,0,230, cv2.THRESH_BINARY)
height, width = img.shape
print "height and width : ",height, width
size = img.size
print "size of the image in number of pixels", size 
img3 = cv2.Canny(img, 10, 100, 3)
nzCount = cv2.countNonZero(img3);
# plot the binary image
imgplot = plt.imshow(img3, 'gray')
plt.show()
