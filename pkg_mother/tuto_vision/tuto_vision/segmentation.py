import cv2
import numpy as np

# connect to a sensor (0: webcam)
cap=cv2.VideoCapture(0)

# capture an image
ret, frame=cap.read()

# Select ROI
r = cv2.selectROI(frame)

# Crop image
imCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

average_h = np.mean(imCrop[:,:,0])
average_s = np.mean(imCrop[:,:,1])
average_v = np.mean(imCrop[:,:,2])

print(average_h,average_s,average_v)

# Display cropped image
cv2.imshow("Image", imCrop)
cv2.waitKey(0)
