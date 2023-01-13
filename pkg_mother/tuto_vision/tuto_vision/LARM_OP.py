import cv2
import numpy as np

im1=cv2.imread("image1.jpg",0)
im2=cv2.imread("image2.jpg",0)
im1 = cv2.resize(im1, (600,800)) 
im2 = cv2.resize(im2, (600,800))

height, width = im1.shape[:2] 

T = np.float32([[1, 0, 5], [0, 1, 0]]) 
im1_translation = cv2.warpAffine(im1, T, (width, height)) 

cv2.imshow("image1",im1)
cv2.imshow("image2",im2)
cv2.imshow("image1 translatee",im1_translation)
cv2.imwrite("image1_translatee.jpg",im1_translation)
cv2.waitKey()

add = np.int16(im1)+np.int16(im2)

sup = np.int16(im1)-np.int16(im1_translation)

div = (im1+1)/((np.float16(im2)/50)+1)
div=np.int16(div)

cv2.normalize(add,  add, 0, 255, cv2.NORM_MINMAX)
cv2.normalize(sup,  sup, 0, 255, cv2.NORM_MINMAX)
cv2.normalize(div,  div, 0, 255, cv2.NORM_MINMAX)

add=np.uint8(add)
sup=np.uint8(sup)
div=np.uint8(div)

figAdd=cv2.imshow("image1 + image2",add)
cv2.imwrite("addition.jpg",add)
figSous=cv2.imshow("image1 - image1_translatee",sup)
cv2.imwrite("soustraction.jpg",sup)
figDiv=cv2.imshow("image1 / image2",div)
cv2.waitKey()

grad_x=np.zeros(im1.shape,np.int)
grad_y=np.zeros(im2.shape,np.int)
rows,cols = im1.shape

print(im1.shape)
print("rows "+str(rows)+" cols "+str(cols))

for i in range(rows-1):
	for j in range(cols-1):
		grad_x[i,j]=np.int(im1[i,j+1])-np.int(im1[i,j])
		grad_y[i,j]=np.int(im1[i+1,j])-np.int(im1[i,j])

print(" i : "+str(i)+" j : "+str(j))
cv2.imshow("grad_x",np.uint8(((grad_x+255)/2)))
cv2.imshow("grad_y",np.uint8(((grad_y+255)/2)))
cv2.imwrite("grad_x.jpg",grad_x)
cv2.imwrite("grad_y.jpg",grad_y)
cv2.waitKey()
