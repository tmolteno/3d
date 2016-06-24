import cv2
import numpy as np 
from matplotlib import pyplot as plt
ihg = raw_input("Num of seed: ")
# read image
hlf = ihg + "Crop.jpg"
cm = cv2.imread('1cmCrop.jpg',0)
img = cv2.imread(hlf, 0)
ret,thresh = cv2.threshold(cm, 100, 255, cv2.THRESH_BINARY_INV)
ret,image = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)
height, width = img.shape

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)

cv2.imshow('img', image)
cv2.imshow('thresh', thresh)
cm = cv2.countNonZero(thresh)
bob = cv2.countNonZero(image)
bob = float(bob)
bob1 = bob / cm
print cm
print bob
print bob1

cv2.waitKey(500)

#print "height and width : ",height, width
#size = img.size
#print "size of the image in number of pixels", size 
#img3 = cv2.Canny(img, 10, 100, 3)
#nzCount = cv2.countNonZero(img3);
## plot the binary image
#imgplot = plt.imshow(img3, 'gray')
#plt.show()
