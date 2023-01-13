import cv2
import numpy as np
import matplotlib.pyplot as plt


imcolor=cv2.imread("fleur.jpg")
imgray=cv2.imread("fleur.jpg",0)

# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(imgray,(5,5),0)
ret,otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
otsufin=imgray
otsufin=np.concatenate((otsufin,otsu), axis=1)
cv2.imwrite("otsu.jpg",otsufin)
cv2.imshow('otsu',otsufin)
cv2.waitKey(0)

#K-MEANS segmentation
Z = imcolor.reshape((-1,3))
Z = np.float32(Z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 4
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center[label.flatten()]
print(center)
imSegKmeans = res.reshape((imcolor.shape))

kmeansim=imcolor
kmeansim=np.concatenate((kmeansim,imSegKmeans), axis=1)
cv2.imwrite("kmeansseg.jpg",kmeansim)
cv2.imshow('kmeansseg.jpg',kmeansim)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Watershed
#label 0 : we don't know
#label 1 : Foreground
#label 2 : Background
kernel = np.ones((3,3),np.uint8)

b,g,r = cv2.split(imcolor) 
mask_petals=np.uint8((r>230)&(g<70)&(b>130))
#mask_petals = cv2.dilate(mask_petals,kernel,iterations = 10)
cv2.imshow('mask_petals',mask_petals*255)
cv2.waitKey(0)

bigger_mask = cv2.dilate(mask_petals,kernel,iterations = 20)
background_mask=(1-bigger_mask)
mask_origin = background_mask*2 + mask_petals

cv2.imwrite("mask_petals.jpg",np.uint8(mask_origin*126))

mask_watershed = cv2.watershed(imcolor,np.int32(mask_origin))
mask_watershed_bin=np.zeros(mask_watershed.shape,np.uint8)
mask_watershed_bin[mask_watershed==1]=1
mask_watershed_bin=cv2.merge((mask_watershed_bin,mask_watershed_bin,mask_watershed_bin))
mask_watershed_RGB=cv2.merge((np.uint8(mask_watershed*64),np.uint8(mask_watershed*64),np.uint8(mask_watershed*64)))

seuillage_watershed = imcolor
seuillage_watershed=np.concatenate((seuillage_watershed,mask_watershed_RGB), axis=1)
seuillage_watershed=np.concatenate((seuillage_watershed,mask_watershed_bin*imcolor), axis=1)

cv2.imwrite("seuillage_watershed.jpg",np.uint8(seuillage_watershed))
cv2.imshow('seuillage_watershed.jpg',np.uint8(seuillage_watershed))
cv2.waitKey(0)

#GrabCut
mask_GC=np.zeros(mask_origin.shape, np.uint8)
mask_GC[mask_origin==2]=cv2.GC_BGD
mask_GC[mask_origin==1]=cv2.GC_FGD
mask_GC[mask_origin==0]=cv2.GC_PR_FGD

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
res_GC, bgdModel, fgdModel = cv2.grabCut(imcolor,mask_GC,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
mask_grabcut = np.where((res_GC==2)|(res_GC==0),0,1).astype('uint8')
mask_grabcut_RGB=cv2.merge((np.uint8(mask_grabcut),np.uint8(mask_grabcut),np.uint8(mask_grabcut)))

seuillage_grabcut = imcolor
seuillage_grabcut=np.concatenate((seuillage_grabcut,np.uint8(mask_grabcut_RGB*255)), axis=1)
seuillage_grabcut=np.concatenate((seuillage_grabcut,np.uint8(mask_grabcut_RGB*imcolor)), axis=1)
cv2.imwrite("seuillage_grabcut.jpg",np.uint8(seuillage_grabcut))
cv2.imshow('seuillage_grabcut.jpg',np.uint8(seuillage_grabcut))
cv2.waitKey(0)


