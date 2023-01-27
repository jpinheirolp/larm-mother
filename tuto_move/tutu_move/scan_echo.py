#!python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import*

import math
from geometry_msgs.msg import Point32

class ScanInterpret(Node):

    def __init__(self):
        super().__init__('scan_interpreter')
        self.create_subscription( LaserScan, 'scan', self.scan_callback, 10)
        self.scan_publisher = self.create_publisher(PointCloud, '/nuagepoint', 10)

    def scan_callback(self, scanMsg):
        sample = []
        obstacles= []
        angle= scanMsg.angle_min
      
        for aDistance in scanMsg.ranges :
            if 0.1 < aDistance and aDistance < 5.0 and abs(angle) < 1.5:

            
                samplePoint= [
                    math.cos(angle) * aDistance,
                    math.sin( angle ) * aDistance
                ]
                sample.append( samplePoint )
    
            


                aPoint= Point32()
                aPoint.x= (float)(math.cos(angle) * aDistance)
                aPoint.y= (float)(math.sin( angle ) * aDistance)
                aPoint.z= (float)(0)
                obstacles.append( aPoint )
              
            angle+= scanMsg.angle_increment
        
            sample= [ [ round(p[0], 2), round(p[1], 2) ] for p in  sample[10:20] ]
            nuage=PointCloud()
            nuage.header.frame_id='laser'
            nuage.points=obstacles
     
        
        self.scan_publisher.publish(nuage)
        
       
        
  
                
           
           
       
      



        
def main(args=None):
    rclpy.init(args=args)
    scanInterpret = ScanInterpret()
    rclpy.spin(scanInterpret)
    scanInterpret.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()
