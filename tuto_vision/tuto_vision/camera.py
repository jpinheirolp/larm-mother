import cv2
import numpy as np
import pyrealsense2 as rs
import time, numpy as np
import sys, cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import*
from cv_bridge import CvBridge
import signal


class camera(Node):

    def __init__(self):
        super().__init__('camera_vision')
        self.bridge=CvBridge()
        self.image_publisher = self.create_publisher(Image, '/sensor_mesgs/image', 10)
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)
        

    def fonctionvision(self):
        def souris(event, x, y, flags, param):
            global lo, hi, color, hsv_px

            if event == cv2.EVENT_MOUSEMOVE:
                # Conversion des trois couleurs RGB sous la souris en HSV
                px = frame[y,x]
                px_array = np.uint8([[px]])
                hsv_px = cv2.cvtColor(px_array,cv2.COLOR_BGR2HSV)

            if event==cv2.EVENT_MBUTTONDBLCLK:
                color=image[y, x][0]

            if event==cv2.EVENT_LBUTTONDOWN:
                if color>5:
                    color-=1

            if event==cv2.EVENT_RBUTTONDOWN:
                if color<250:
                    color+=1

            lo[0]=color-10
            hi[0]=color+10

        color=100

        lo=np.array([color-5, 100, 50])
        hi=np.array([color+5, 255,255])

        color_info=(0, 0, 255)

        cap=cv2.VideoCapture(0)
        cv2.namedWindow('Camera')
        cv2.setMouseCallback('Camera', souris)
        hsv_px = [0,0,0]

        # Creating morphological kernel
        kernel = np.ones((3, 3), np.uint8)

        while True:
            ret, frame=cap.read()
            image=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            image_publiée= self.bridge.cv2_to_imgmsg(frame,"bgr8")
            self.image_publisher.publish(image_publiée)
            mask=cv2.inRange(image, lo, hi)
            mask=cv2.erode(mask, kernel, iterations=1)
            mask=cv2.dilate(mask, kernel, iterations=1)
            image2=cv2.bitwise_and(frame, frame, mask= mask)
            cv2.putText(frame, "Couleur: {:d}".format(color), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, color_info, 1, cv2.LINE_AA)

            # Affichage des composantes HSV sous la souris sur l'image
            pixel_hsv = " ".join(str(values) for values in hsv_px)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, "px HSV: "+pixel_hsv, (10, 260),
                    font, 1, (255, 255, 255), 1, cv2.LINE_AA)

            #cv2.imshow('Camera', frame)
            #cv2.imshow('image2', image2)
            #cv2.imshow('Mask', mask)

            if cv2.waitKey(1)&0xFF==ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

def main(args=None):
    rclpy.init(args=args)

    Camera =camera()

    Camera.fonctionvision()
    
    # Start the ros infinit loop with the Camera node.
    rclpy.spin_once(Camera)

    # At the end, destroy the node explicitly.
    Camera.destroy_node()

    # and shut the light down.
    rclpy.shutdown()

if __name__ == '__main__':
    main()