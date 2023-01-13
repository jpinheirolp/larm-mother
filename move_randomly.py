#!python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import*
from geometry_msgs.msg import Twist
from random import random
#from nav_msgs.msg import Odometry

import math
from geometry_msgs.msg import Point32


class Move_Randomly(Node):

    def __init__(self):
          
        super().__init__('move_safe')
        self.create_subscription( PointCloud, '/nuagepoint', self.interpret_obstacles, 10)
        #self.create_subscription( Odometry, 'odometry/filtered', self.interpret_obstacles, 10)

        self.velocity_publisher= self.create_publisher(Twist, '/multi/cmd_nav', 10)
        self.timer = self.create_timer(0.1, self.move_robot) # 0.1 seconds to target a frequency of 10 hertz
        self.rectangle_closer_y_limit = -0.3
        self.rectangle_further_away_y_limit = 0.3
        self.rectangle_left_x_limit = 0
        self.rectangle_right_x_limit = 0.23
        self.rectangle_low_z_limit = -0.18
        self.rectangle_high_z_limit = 0.4
        self.rectangle_center_x_direction = 0
        self.command = "no commmand"
        self.time_to_rnd_turn = 0
        self.time_interval_rnd_turn = 300 # 0.1s * 300 == 30 seconds
        self.robot_angle = 0
        self.robot_position_x = 0
        self.robot_position_y = 0
        self.robot_position_z = 0
        self.mutex_trn_rnd = False
        self.rotation_counter = 0
        
   

    def interpret_obstacles(self,scanMsg):
        print("interpreting ...")
        self.time_to_rnd_turn = (self.time_interval_rnd_turn + 1) % self.time_interval_rnd_turn
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
                        if point_y_coordinate < self.rectangle_center_x_direction:
                            num_points_left += 1
                        else: 
                            num_points_right += 1
        #It`s not gonna work but the idea is good
        if self.time_interval_rnd_turn == 0:
            self.command = "turn_to_rnd_position"
            return 0
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
        if self.command == "turn_to_rnd_position" and not self.mutex_trn_rnd:
            self.mutex_trn_rnd = True
            self.rotation_counter = round(random() * 2 * math.pi * 10) # determines a random angular position
        if self.mutex_trn_rnd: #if the robot is turning the other movements stop
            if self.rotation_counter == 0:
                self.mutex_trn_rnd = False
                return 0
            velo.angular.z = 0.1
        elif self.command == "go_foward": #would be more optmized with a switch :(
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

    def turn_to_rnd_position(self):
        if self.rotation_counter == 0:
            self.mutex_trn_rnd = False
            return 0
        return 

        
        pass

    
                    
            
        

       
def main(args=None):
    print('Its working now ')
    rclpy.init(args=args)
    safe_rnd_move_controller = Move_Randomly()  
    rclpy.spin(safe_rnd_move_controller)
    safe_rnd_move_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()

           
#'''
       
      



        