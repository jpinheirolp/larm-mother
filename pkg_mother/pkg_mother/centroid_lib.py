import matplotlib.pyplot as plt
import matplotlib.colors as clr
from sklearn.cluster import KMeans
import numpy as np
import cv2


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
        image_hist_vector.extend(bins)

    '''for i in range(len(colors_hsv)):
        hist = colors_hsv[i].ravel()
        (n, bins, patches) = plt.hist(hist, bins=256, color = color_names[i],density=True)
        image_hist_vector.extend(bins) #'''
    
    return np.array(image_hist_vector)

def find_closest_piece_image(image,positive_centroid, false_positive_centroid,num_x_pieces, num_y_pieces,save_images = False):
    num_pixels_x_image = image.shape[1] 
    num_pixels_y_image = image.shape[0] 
    num_pixels_x_piece = num_pixels_x_image // num_x_pieces # a big chink of this func is in crop_images, desrespecting the DRY principle
    num_pixels_y_piece = num_pixels_y_image // num_y_pieces
    closest_distance = np.inf
    closest_piece = []

    for x in range(num_x_pieces ):
        for y in range(num_y_pieces ):
            image_piece = image[y*num_pixels_y_piece : (y+1)*num_pixels_y_piece, x*num_pixels_x_piece : (x+1)*num_pixels_x_piece]
            piece_vec_hist = create_image_vector_color_hist_space(image_piece) #this should ne a 2dimensional array
            piece_positive_distance = np.linalg.norm(positive_centroid - piece_vec_hist,ord=1)
            piece_negative_distance = np.linalg.norm(false_positive_centroid - piece_vec_hist,ord=1)
            piece_distance = piece_positive_distance - piece_negative_distance * 0.6

            if save_images:
                cv2.imwrite(f"./distance_images/{piece_positive_distance//100}_{piece_negative_distance//100}.jpg", image_piece)

            if closest_distance > piece_distance:
                closest_distance = piece_distance
                closest_piece = image_piece
   
    return closest_piece

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