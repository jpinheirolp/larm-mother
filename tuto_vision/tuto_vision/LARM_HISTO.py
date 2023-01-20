import cv2
import numpy as np
import matplotlib.pyplot as plt
from tools import *

im1=cv2.imread("image_501.jpg",0)
im2=cv2.imread("image_886.jpg",0)
im1 = cv2.resize(im1, (600,800)) 
im2 = cv2.resize(im2, (600,800))

fig1=cv2.imshow("image1",im1)
fig2=cv2.imshow("image2",im2)
cv2.waitKey()

histo_im1=histo(im1)
cv2.imshow("histogramme im",histo_im1)
cv2.waitKey()
cv2.destroyWindow("histogramme im")
cv2.imwrite("image1_histogramme.jpg",histo_im1)

seuillage_infirmiere=np.uint8((im1>200)*255)
histo_seuillage_infirmiere=histo(seuillage_infirmiere)
figSeuilInf=cv2.imshow("seuillage_infirmiere",histo_seuillage_infirmiere)
cv2.imwrite("seuillage_infirmiere.jpg",histo_seuillage_infirmiere)
cv2.waitKey()
cv2.destroyWindow("seuillage_infirmiere")

seuillage_marin=np.uint8((im1<75)*255)
histo_seuillage_marin=histo(seuillage_marin)
figSeuilMarin=cv2.imshow("seuillage_marin",histo_seuillage_marin)
cv2.imwrite("seuillage_marin.jpg",histo_seuillage_marin)
cv2.waitKey()
cv2.destroyWindow("seuillage_marin")

equ = cv2.equalizeHist(im1)
histo_equ=histo(equ)
fig_egalisation=cv2.imshow("Egalisation d'histogramme",histo_equ)
cv2.imwrite("image1_egalisation.jpg",histo_equ)
cv2.waitKey()
#cv2.destroyWindow(fig_egalisation)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(im1)
histo_clahe=histo(cl1)
cv2.imshow("CLAHE",histo_clahe)
cv2.imwrite("image1_CLAHE.jpg",histo_clahe)
cv2.waitKey()
cv2.destroyWindow("CLAHE")

imfleur=cv2.imread("fleur.jpg")
b,g,r = cv2.split(imfleur) 

mask=np.uint8((r>230)&(g<120)&(b>90))
r=r*mask
g=g*mask
b=b*mask
newRGBImage = cv2.merge((b,g,r))

mask_RGB=cv2.merge((mask,mask,mask))*255

seuillage_couleur = imfleur
seuillage_couleur=np.concatenate((seuillage_couleur,mask_RGB), axis=1)
seuillage_couleur=np.concatenate((seuillage_couleur,newRGBImage), axis=1)

cv2.imwrite("seuillage_couleur.jpg",seuillage_couleur)

cv2.imshow("seuillage_couleur",seuillage_couleur)
cv2.waitKey()

lut=np.log(range(256))
maxiLut=np.max(lut)
lut=np.uint8((lut/maxiLut)*255.0)

lutIm=myplot(lut)
cv2.imshow("lutIm",lutIm)
cv2.waitKey()

print(lut)
Image_LUT=cv2.LUT(im1, lut)
#c=255/np.log(255+1)
#Image_LUT=Image_LUT*c

cv2.imshow("image LUT",Image_LUT)
cv2.waitKey()









