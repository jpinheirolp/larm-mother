import cv2
import numpy as np
import matplotlib.pyplot as plt
from tools import histo, myplot


im1=cv2.imread("image1.jpg",0)
im1 = cv2.resize(im1, (600,800)) 

cv2.imshow("image1",im1)
cv2.waitKey()

kernel = np.ones((3,3),np.float32)/9
im_conv_moy = cv2.filter2D(im1,-1,kernel)
cv2.imshow("image1 moyenneur",im_conv_moy)
cv2.imwrite("conv_moy.jpg",im_conv_moy)
cv2.waitKey()

kernel = -np.ones((3,3),np.float32)
kernel[1,1]=8
im_conv_contours = cv2.filter2D(im1,-1,kernel)
cv2.imshow("image1 contours",im_conv_contours)
cv2.imwrite("conv_cont.jpg",im_conv_contours)
cv2.waitKey()

kernel = -np.ones((3,3),np.float32)
kernel[1,1]=5
kernel[2,2]=kernel[0,0]=kernel[0,2]=kernel[2,0]=0
im_conv_net = cv2.filter2D(im1,-1,kernel)
cv2.imshow("image1 nettete",im_conv_net)
cv2.imwrite("conv_nettete.jpg",im_conv_net)
cv2.waitKey()

f = np.fft.fft2(im1)
fshift = np.fft.fftshift(f)

magnitude_spectrum = np.uint8(20*np.log(np.abs(fshift)))
mask = np.zeros((magnitude_spectrum.shape))
cv2.circle(mask, (np.int(magnitude_spectrum.shape[1]/2),np.int(magnitude_spectrum.shape[0]/2)), 50, 1, thickness=-1)
cv2.imshow("mask",mask*255)

fshift=fshift*mask
f = np.fft.ifftshift(fshift)
im_filtree = np.fft.ifft2(f)

cv2.imshow("image_filtre",np.uint8(np.abs(im_filtree)))
cv2.imwrite("filtrage_fft.jpg",np.uint8(np.abs(im_filtree)))
cv2.imwrite("mask_fft.jpg",np.uint8(mask*255))
cv2.imwrite("fft_maskee.jpg",np.uint8(magnitude_spectrum*mask))
cv2.imwrite("fft2D.jpg",np.uint8(magnitude_spectrum))


fftIm=im1
fftIm=np.concatenate((im1,magnitude_spectrum),axis=1)
cv2.imshow("image1 FFT2D",fftIm)
cv2.imwrite("fft2d.jpg",fftIm)
cv2.waitKey()

