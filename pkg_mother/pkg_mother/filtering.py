#import the libraries
import cv2 as cv
import numpy as np

#'''
img = cv.imread("/home/bot/Vidéos/image_780.jpg")
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

lower_orange_bottle = np.array([5,180, 170]) # 5, 180 , ?
upper_orange_bottle = np.array([15,255,255])
mask = cv.inRange(hsv, lower_orange_bottle, upper_orange_bottle)
res = cv.bitwise_and(img, img, mask=mask)
# '''

#create resizable windows for displaying the images
cv.imwrite('./filtered_images/res.jpg',res)
cv.imwrite('./filtered_images/hsv.jpg',hsv)
cv.imwrite('./filtered_images/mask.jpg',mask)


#'''
# img = cv.imread("/home/bot/Images/image_2361.jpg")
# hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# lower_orange_bottle = np.array([110,30, 100]) # 5, 180 , ?
# upper_orange_bottle = np.array([255,255,255])
# mask = cv.inRange(hsv, lower_orange_bottle, upper_orange_bottle)
# res = cv.bitwise_and(img, img, mask=mask)
# # '''

# #create resizable windows for displaying the images
# cv.imwrite('./filtered_images/res.jpg',res)
# cv.imwrite('./filtered_images/hsv.jpg',hsv)
# cv.imwrite('./filtered_images/mask.jpg',mask)