#!python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import*
#from centroid_lib import *

import math
from geometry_msgs.msg import Point32
from geometry_msgs.msg import Twist

import matplotlib.pyplot as plt
import matplotlib.colors as clr
from sklearn.cluster import KMeans
import numpy as np
import cv2
from cv_bridge import CvBridge
from std_msgs.msg import String

# On importe les fonctions de centroid_lib

color_info=(0, 0, 255)


def crop_image(image,num_x_pieces, num_y_pieces):
    num_pixels_x_image = image.shape[1] 
    num_pixels_y_image = image.shape[0] 
    num_pixels_x_piece = num_pixels_x_image // num_x_pieces # a big chink of this func is in find_closest_element(), desrespecting the DRY principle
    num_pixels_y_piece = num_pixels_y_image // num_y_pieces
    croped_images = []
    for x in range(num_x_pieces ):
        for y in range(num_y_pieces ):
            image_piece = image[y*num_pixels_y_piece : (y+1)*num_pixels_y_piece, x*num_pixels_x_piece : (x+1)*num_pixels_x_piece]
            croped_images.append(image_piece) #this should ne a 2dimensional array
    return croped_images 
#'''

def create_image_vector_color_hist_space(im):
    # Load the image as a NumPy array
    image = np.array(im)
    color_names = ['red','green','blue']
    hsv_names = ['h','s','v']
     

    # Split the image into its R, G, and B channels
    color_list = np.split(image, [1, 2], axis=2)
    image_hsv = clr.rgb_to_hsv(image) 
    colors_hsv = np.split(image_hsv, [1, 2], axis=2)
    
    image_hist_vector = []

    for i in range(len(color_list)):
        hist = color_list[i].ravel()
        (n, bins, patches) = plt.hist(hist, bins=256, color = color_names[i],density=True)
        if i == 0:
            bins = bins[5:15]
        elif i == 1:
            bins = bins[180:]
        elif i == 2:
            bins = bins[120:]

        image_hist_vector.extend(bins)

    '''for i in range(len(colors_hsv)):
        hist = colors_hsv[i].ravel()
        (n, bins, patches) = plt.hist(hist, bins=256, color = color_names[i],density=True)
        image_hist_vector.extend(bins) #'''
    return np.array(image_hist_vector)

def find_closest_piece_image(image,height,width,positive_centroid, false_positive_centroid,num_x_pieces,num_y_pieces, tol = 0.4,save_images = False):
    
    
    num_pixels_x_image = width
    num_pixels_y_image = height
    num_pixels_x_piece = num_pixels_x_image // num_x_pieces # a big chink of this func is in crop_images, desrespecting the DRY principle
    num_pixels_y_piece = num_pixels_y_image // num_y_pieces
    closest_distance = np.inf
    closest_piece = []
    tol_variable = 0
    closet_piece_x = 0
    closet_piece_y = 0

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_orange_bottle = np.array([3,150,100])# 5, 180 , ?
    upper_orange_bottle = np.array([17,255,255])
    mask = cv2.inRange(hsv, lower_orange_bottle, upper_orange_bottle)
    filtered_image = cv2.bitwise_and(image, image, mask=mask)
    

    for x in range(num_x_pieces ):
        for y in range(num_y_pieces ):
            image_piece = filtered_image[y*num_pixels_y_piece : (y+1)*num_pixels_y_piece, x*num_pixels_x_piece : (x+1)*num_pixels_x_piece]
            piece_vec_hist = create_image_vector_color_hist_space(image_piece) #this should ne a 2dimensional array
            print(len(positive_centroid), len(piece_vec_hist))
            piece_positive_distance = np.linalg.norm(positive_centroid - piece_vec_hist,ord=1)
            piece_negative_distance = np.linalg.norm(false_positive_centroid - piece_vec_hist,ord=1)
            piece_distance = piece_positive_distance #- piece_negative_distance * 0.6
            

            #if save_images:
                #cv2.imwrite(f"./distance_images/{piece_positive_distance//100}_{piece_negative_distance//100}.jpg", image_piece)
                #cv2.imwrite(f"/home/bot/ros2_ws/larm-mother/distance_images/{piece_positive_distance/piece_negative_distance}.jpg", image_piece)
                #print('saving img')

            if closest_distance > piece_distance:
                closest_distance = piece_distance
                closest_piece = image_piece
                tol_variable = piece_positive_distance/piece_negative_distance
                best_distance = piece_positive_distance
                closet_piece_x = x
                closet_piece_y = y

    #returned_image =  image
    returned_image = f"{tol_variable}_{best_distance}"

    if tol_variable < tol:
        #cv2.circle(returned_image,(int((closet_piece_x  +0.5 ) * num_pixels_x_piece ),int((closet_piece_y  +0.5 ) * num_pixels_y_piece )),num_pixels_x_image,(0,0,0),1)
        #cv2.putText(returned_image, "Bouteille orange!!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, color_info, 1, cv2.LINE_AA)
        #cv2.imshow('Camera', returned_image)
        ''' ----------------

        

        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (closet_piece_x*num_pixels_x_piece,closet_piece_y*num_pixels_y_piece)
        fontScale = 1
        color = (240,10,10)
        
        alpha = 0.5
        beta = (1.0 - alpha)
        returned_image = cv2.addWeighted(image, alpha, filtered_image, beta, 0.0)

        returned_image = cv2.putText(returned_image, text_image, org, font, fontScale, color)
        print("bouteille") '''
        returned_image = f"{tol_variable}_{best_distance}_bouteille"
    return returned_image

def create_centroids(img_file_list, img_folder_list, num_pcs_x, num_pcs_y,k):
    list_vectors = []
    for i in range(len(img_file_list)):
        im =cv2.imread(img_folder_list[i] + "/" + img_file_list[i] + ".jpg")
        croped_imgs =  crop_image(im,num_pcs_x,num_pcs_y)
        
        for j in range(num_pcs_x*num_pcs_y):
            vector_hist = create_image_vector_color_hist_space(croped_imgs[j])
            
            list_vectors.append(vector_hist)

    list_vectors = np.array(list_vectors)
    kmeans = KMeans(n_clusters=k, random_state=0, n_init="auto").fit(list_vectors)
    print(kmeans.labels_)

    centroids = kmeans.cluster_centers_
    
    return centroids

#rosification

class CameraInterpret(Node):

    def __init__(self):
        self.bridge=CvBridge()
        super().__init__('scan_interpreter')
        self.create_subscription( Image, '/sensor_mesgs/image', self.camera_callback, 10)
        #self.scan_publisher = self.create_publisher(Image, '/detection', 10) # change to text msg
        self.scan_publisher = self.create_publisher(String, '/detection', 10) # change to text msg
        self.orange_centroid = np.loadtxt("/home/bot/ros2_ws/larm-mother/pkg_mother/pkg_mother/centroids/centroid_orange.txt")
        self.ground_centroid = np.loadtxt("/home/bot/ros2_ws/larm-mother/pkg_mother/pkg_mother/centroids/centroid_red.txt")
        self.black_centroid = np.loadtxt("/home/bot/ros2_ws/larm-mother/pkg_mother/pkg_mother/centroids/centroid_black.txt")
       
    def camera_callback(self, scanMsg):
        sample = []
        obstacles= []
        (height,width)=(scanMsg.height,scanMsg.width)
       # captured_image = np.array(scanMsg.data)
        captured_image = scanMsg
        cv2_image = self.bridge.imgmsg_to_cv2(captured_image,"bgr8")
       # print(captured_image.shape)

        '''
        black_bottle_found = find_closest_piece_image(cv2_image,height,width,self.black_centroid,self.ground_centroid, 3 ,3,save_images=False)


        if len(black_bottle_found) == 0:
            msg = "Pas de Bouteille Noir ici\n"
        else:
            msg = "Voila, une Bouteille Noir !!!!!!!!!\n"
        #'''

        orange_bottle_found = find_closest_piece_image(cv2_image,height,width,self.orange_centroid,self.ground_centroid, 3 ,3,tol=0.7,save_images=True)
        
        #msg = Image()

        
        #msg= self.bridge.cv2_to_imgmsg(orange_bottle_found,"bgr8")
        msg = String()

        msg.data = orange_bottle_found

        self.scan_publisher.publish(msg)
        

        
       

        
def main(args=None):
    rclpy.init(args=args)
    camera_interpret = CameraInterpret()
    rclpy.spin(camera_interpret)
    camera_interpret.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()
