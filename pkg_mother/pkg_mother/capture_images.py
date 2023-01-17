#!python3
import rclpy
from rclpy.node import Node
import cv2
import numpy as np
import os
#from sklearn.svm import LinearSVC
#from scipy.cluster.vq import *
#from sklearn.preprocessing import StandardScaler
#from sklearn import preprocessing
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
image_path = '/home/bot/ros2_ws/larm-mother/pkg_mother/photos' 
os.chdir(image_path)
class CameraInterpret(Node):
    def __init__(self):
        super().__init__('scan_interpreter')
        self.create_subscription( Image, 'img', self.scan_callback, 10)
        self.image_counter = 0
        self.bridge = CvBridge()
       
        
    def scan_callback(self, scanMsg):
        #print("capturing image")
        self.image_counter += 1
        captured_image = scanMsg
        #print(captured_image) 
        cv_captured_image = self.bridge.imgmsg_to_cv2(captured_image, "bgr8")
        cv2.imwrite(f'image_{self.image_counter}.jpg', cv_captured_image)

def main(args=None):
    rclpy.init(args=args)
    cameraInterpret = CameraInterpret()
    rclpy.spin(cameraInterpret)
    cameraInterpret.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()


