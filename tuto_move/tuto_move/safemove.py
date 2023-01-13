'''
#!python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import*

import math
from geometry_msgs.msg import Point32

class ScanInterpret(Node):

    def __init__(self):
        super().__init__('scan_interpreter')
        self.create_subscription( PointCloud, '/nuagepoint', self.interpret_obstacles, 10)
        self.scan_publisher = self.create_publisher(PointCloud, '/nuagepoint', 10)

    def interpret_obstacles(self, scanMsg):
        sample = []
        obstacles= []
        angle= scanMsg.angle_min
        for aDistance in scanMsg.ranges :
            if 0.1 < aDistance and aDistance < 5.0 :

            
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
            self.get_logger().info( f" obs({len(obstacles)}) ...{sample}..." ) 
            nuage=PointCloud()
            nuage.header.frame_id='laser'
            nuage.points=obstacles
     
        
        self.scan_publisher.publish(nuage)
        
       
        
  


        
def main(args=None):
    print('Its running 3')
    rclpy.init(args=args)
    scanInterpret = ScanInterpret()
    rclpy.spin(scanInterpret)
    scanInterpret.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()


'''
#!python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import*
from geometry_msgs.msg import Twist

import math
from geometry_msgs.msg import Point32


class MoveSafe(Node):

    def __init__(self):
          
        super().__init__('move_safe')
        self.create_subscription( PointCloud, '/nuagepoint', self.interpret_obstacles, 10)
        #self.create_subscription( LaserScan, 'scan', self.interpret_obstacles, 10)

        self.velocity_publisher= self.create_publisher(Twist, '/multi/cmd_nav', 10)
        self.timer = self.create_timer(0.1, self.move_robot) # 0.1 seconds to target a frequency of 10 hertz
        self.rectangle_closer_y_limit = 0.1
        self.rectangle_further_away_y_limit = 0.5
        self.rectangle_left_x_limit = -0.3
        self.rectangle_right_x_limit = 0.3
        self.rectangle_low_z_limit = -0.15
        self.rectangle_high_z_limit = 0.2
        self.rectangle_center_x_direction = 0
        self.command = "no commmand"

   

    def interpret_obstacles(self,scanMsg):
        print("interpreting ...")
        obstacles_points = scanMsg.points
        num_points_left = 0
        num_points_right = 0
        tol_of_points_inside_rect = 30
        for point in obstacles_points:
            point_x_coordinate = point.x
            point_y_coordinate = point.y
            point_z_coordinate = point.z
            if self.rectangle_closer_y_limit < point_y_coordinate and point_y_coordinate < self.rectangle_further_away_y_limit:
                if self.rectangle_left_x_limit < point_x_coordinate and point_x_coordinate < self.rectangle_right_x_limit:
                    if self.rectangle_low_z_limit < point_z_coordinate and point_z_coordinate < self.rectangle_high_z_limit:

                        #point is inside rectangle
                        if point_x_coordinate < self.rectangle_center_x_direction:
                            num_points_left += 1
                        else: 
                            num_points_right += 1
        if num_points_left + num_points_right <= tol_of_points_inside_rect:
            #there is no object in front of the robot
            self.command = "go_foward"
        else:
            if num_points_left < num_points_right:
                #there is a object on the right
                self.command = "turn_left"
            else:
                #there is a object on the left
                self.command = "turn_right"

    def move_robot(self):
        velo = Twist()
        print(self.command)
        if self.command == "go_foward": #would be more optmized with a switch :(
            velo.linear.x = 0.1
            velo.angular.z = 0.0
        elif self.command == "turn_right":
            velo.linear.x = 0.0
            velo.angular.z = 0.5
        elif self.command == "turn_left":
            velo.linear.x = 0.0
            velo.angular.z = -0.5
        else:
            return 0
        print(velo)
        self.velocity_publisher.publish(velo)

                    
            
        

       
def main(args=None):
    print('Its working now ')
    rclpy.init(args=args)
    safe_move_controller = MoveSafe()  
    rclpy.spin(safe_move_controller)
    safe_move_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()

           
#'''
       
      



        