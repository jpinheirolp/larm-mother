#!python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import*
from centroid_lib import *

import math
from geometry_msgs.msg import Point32

class CameraInterpret(Node):

    def __init__(self):
        super().__init__('scan_interpreter')
        self.create_subscription( Image, '/sensor_mesgs/image', self.camera_callback, 10)
        self.scan_publisher = self.create_publisher(str, '/detection', 10) # change to text msg
        self.orange_centroid = np.loadtxt("./centroids/centroid_orange.txt")
        self.ground_centroid = np.loadtxt("./centroids/centroid_red.txt")
        self.black_centroid = np.loadtxt("./centroids/centroid_black.txt")


    def camera_callback(self, scanMsg):
        sample = []
        obstacles= []
        captured_image = np.array(scanMsg.data)
        black_bottle_found = find_closest_piece_image(captured_image,self.black_centroid,self.ground_centroid, 3 ,3,save_images=False)


        if len(black_bottle_found) == 0:
            msg = "Pas de Bouteille Noir ici\n"
        else:
            msg = "Voila, une Bouteille Noir !!!!!!!!!\n"

        orange_bottle_found = find_closest_piece_image(captured_image,self.orange_centroid,self.ground_centroid, 3 ,3,save_images=False)

        
        if len(orange_bottle_found) == 0:
            msg += "Pas de Bouteille Orange ici"
        else:
            msg += "Voila, une Bouteille Orange !!!!!!!!!"


        self.scan_publisher.publish(msg)
        
       

        
def main(args=None):
    rclpy.init(args=args)
    camera_interpret = CameraInterpret()
    rclpy.spin(CameraInterpret)
    camera_interpret.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()
