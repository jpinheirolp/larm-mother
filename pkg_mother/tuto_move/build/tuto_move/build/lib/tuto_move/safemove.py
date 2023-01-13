#python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import*
from geometry_msgs.msg import Twist

import math
from geometry_msgs.msg import Point32


class MoveSafe(Node):

    def __init__(self):
          
        super().__init__('movesafe')
        self.obstacles = self.create_subscription( PointCloud, '/nuagepoint', self.interpret_obstacles, 10)
        self.velocity_publisher= self.create_publisher(Twist, '/multi/cmd_nav', 10)
        self.timer = self.create_timer(0.1, self.interpret_obstacles) # 0.1 seconds to target a frequency of 10 hertz
        self.rectangle_closer_y_limit = 1
        self.rectangle_further_away_y_limit = 5
        self.rectangle_left_x_limit = -3
        self.rectangle_right_y_limit = 3
        self.rectangle_center_x_direction = 0

    def move_robot(self,command):
        velo = Twist()
        print(command)
        if command == "go_foward": #would be more optmized with a switch :(
            velo.linear.y = 0.2
            velo.angular.x = 0
        elif command == "turn_right":
            velo.linear.y = 0
            velo.angular.x = 1
        elif command == "turn_left":
            velo.linear.y = 0
            velo.angular.x = -1
        else:
            return 0

        self.velocity_publisher.publish(velo)

    def interpret_obstacles(self,scanMsg):
        print(self.obstacles)
        obstacles_points = scanMsg.points
        num_points_left = 0
        num_points_right = 0
        tol_of_points_inside_rect = 2
        for point in obstacles_points:
            point_x_coordinate = point.x
            point_y_coordinate = point.y
            if self.rectangle_closer_y_limit < point_y_coordinate and point_y_coordinate < self.rectangle_further_away_y_limit:
                if self.rectangle_left_x_limit < point_x_coordinate and point_x_coordinate < self.rectangle_right_y_limit:
                    #point is inside rectangle
                    if point_x_coordinate < self.rectangle_center_x_direction:
                        num_points_left += 1
                    else: 
                        num_points_right += 1
        if num_points_left + num_points_right <= tol_of_points_inside_rect:
            #there is no object in front of the robot
            self.move_robot("go_foward")
        else:
            if num_points_left < num_points_right:
                #there is a object on the right
                self.move_robot("turn_left")
            else:
                #there is a object on the left
                self.move_robot("turn_right")

                    
            
        

       
def main(args=None):
    print('Its running')
    rclpy.init(args=args)
    safe_move_controller = MoveSafe()  
    rclpy.spin(safe_move_controller)
    safe_move_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()

           
       
      



        