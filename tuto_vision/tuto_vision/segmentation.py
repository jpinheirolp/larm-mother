import cv2
import pyrealsense2 as rs
import time, numpy as np
import sys, cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import*
from cv_bridge import CvBridge
import signal
import numpy as np

class cameraselection(Node):


    def __init__(self):
         super().__init__('camera_vision')
         self.bridge=CvBridge()
         #self.image_subscription = self.create_subscription( Image, '/sensor_mesgs/image', self.fonctionselection, 10)
         #self.timer = self.create_timer(0.1, self.interpret_obstacles) # 0.1 seconds to target a frequency of 10 hertz
        # Configure depth and color streams
         self.pipeline = rs.pipeline()
         self.config = rs.config()

    def fonctionselection(self):

        cap=cv2.VideoCapture(0)

        # capture an image
        #image=scanMsg.data

        # Select ROI
        r = cv2.selectROI(cap)

        ret, frame=cap.read()

        # Crop image
        imCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

        average_h = np.mean(imCrop[:,:,0])
        average_s = np.mean(imCrop[:,:,1])
        average_v = np.mean(imCrop[:,:,2])

        print(average_h,average_s,average_v)

        # Display cropped image
        cv2.imshow("Image", imCrop)
        cv2.imwrite('template.png', imCrop)
        cv2.waitKey(0)

       
def main(args=None):
    print('Its working now ')
    rclpy.init(args=args)
    imageSelection=cameraselection()  
    rclpy.spin_once(imageSelection)
    imageSelection.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()
