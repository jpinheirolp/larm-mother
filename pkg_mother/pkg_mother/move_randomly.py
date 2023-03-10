#!python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import*
from geometry_msgs.msg import Twist
from random import random, getrandbits
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
        self.rectangle_left_y_limit = -0.3
        self.rectangle_right_y_limit = 0.3
        self.rectangle_closer_x_limit = 0
        self.rectangle_further_away_x_limit = 0.6
        self.rectangle_low_z_limit = -0.18
        self.rectangle_high_z_limit = 0.4
        self.rectangle_center_y_direction = 0

        self.rectangle_linear_speed_far_limit = 1.1
        self.rectangle_linear_speed_close_limit = 0.6

        self.command = "no command"

        self.time_interval_rnd_turn = 300 # 0.1s * 300 == 30 seconds
        self.time_to_rnd_turn = 300


        self.robot_max_angular_speed = 1.5
        self.robot_min_angular_speed = 0.5
        self.robot_right_angular_speed = 0
        self.robot_left_angular_speed = 0

        self.robot_linear_speed = 0.1

        self.robot_close_linear_speed = 0.1
        self.robot_middle_linear_speed = 0.15
        self.robot_far_linear_speed = 0.2
        

        self.mutex_trn_rnd = 0
        self.rotation_counter = 0
        
    

    def interpret_obstacles(self,scanMsg):
        #print("interpreting ...")
        
        obstacles_points = scanMsg.points
        num_points_left = 0
        num_points_right = 0
        num_points_close = 0
        num_points_middle = 0
        num_points_far = 0

        tol_of_points_inside_rect = 25
        sum_for_robot_left_angular_speed = 0
        sum_for_robot_right_angular_speed = 0
        for point in obstacles_points:
            point_x_coordinate = point.x
            point_y_coordinate = point.y
            point_z_coordinate = point.z

            left_rect_center = (self.rectangle_left_y_limit - self.rectangle_center_y_direction)/2
            right_rect_center = (self.rectangle_right_y_limit - self.rectangle_center_y_direction)/2

            if self.rectangle_left_y_limit < point_y_coordinate and point_y_coordinate < self.rectangle_right_y_limit:
                if self.rectangle_closer_x_limit < point_x_coordinate and point_x_coordinate < self.rectangle_further_away_x_limit:
                    if self.rectangle_low_z_limit < point_z_coordinate and point_z_coordinate < self.rectangle_high_z_limit:
                        #point is inside rectangle
                        if point_y_coordinate < self.rectangle_center_y_direction:
                            num_points_left += 1
                            # uodating angular speed
                            sum_for_robot_left_angular_speed += ( (self.rectangle_left_y_limit - (point_y_coordinate - self.rectangle_center_y_direction) ) * (self.robot_max_angular_speed*0.7-self.robot_min_angular_speed)) / left_rect_center
                    
                        else: 
                            num_points_right += 1
                            sum_for_robot_right_angular_speed += ( (self.rectangle_right_y_limit - (point_y_coordinate - self.rectangle_center_y_direction)) * (self.robot_max_angular_speed*0.7-self.robot_min_angular_speed)) / right_rect_center

                        if point_x_coordinate < self.rectangle_linear_speed_close_limit:
                            num_points_close += 1
                        elif point_x_coordinate < self.rectangle_linear_speed_far_limit:
                            num_points_middle += 1
                        else:
                            num_points_far += 1


        #It`s not gonna work but the idea is good
        ##print("points in left",num_points_left)
        ##print("points in right", num_points_right)
        if self.time_to_rnd_turn <= 0:
            self.command = "turn_to_rnd_position"
            return 0
        if num_points_left + num_points_right <= tol_of_points_inside_rect:
            #there is no object in front of the robot
            print(num_points_close, num_points_middle, num_points_far) 
            if (max(num_points_close, num_points_middle, num_points_far) == num_points_close) and (num_points_close != 0):
                self.robot_linear_speed = self.robot_close_linear_speed
            elif num_points_middle > num_points_far:
                self.robot_linear_speed = self.robot_middle_linear_speed
            else:
                self.robot_linear_speed = self.robot_far_linear_speed

            self.command = "go_foward"

        else:
            if abs(num_points_left - num_points_right) < 20:
            
                self.command = "turn_to_rnd_position"
                
            elif num_points_left < num_points_right:
                #there is a object on the left
                self.command = "turn_left"
                self.robot_left_angular_speed = abs(sum_for_robot_right_angular_speed/(num_points_right + 1)) + self.robot_min_angular_speed
            else:
                #there is a object on the right
                self.command = "turn_right"
                self.robot_right_angular_speed = sum_for_robot_left_angular_speed/(num_points_left + 1) + self.robot_min_angular_speed
                

    def move_robot(self):
        print(self.robot_linear_speed)
        velo = Twist()
        ##print(self.command)
        self.time_to_rnd_turn -= 1
        ##print(self.time_to_rnd_turn,"time to turn")
        if self.command == "turn_to_rnd_position" and self.mutex_trn_rnd == 0:
            print("I should turn")
            angular_speed_sig = 1
            if bool(getrandbits(1)):
                angular_speed_sig = -1
            self.mutex_trn_rnd =  angular_speed_sig
            self.rotation_counter = round(random() * 2 * math.pi * 10) # determines a random angular position
            self.time_to_rnd_turn = self.time_interval_rnd_turn
        if self.mutex_trn_rnd != 0: #if the robot is turning the other movements stop
            print("Im turning")
            if self.rotation_counter <= 0:
                self.rotation_counter = 0
                self.mutex_trn_rnd = 0
                return 0

            self.rotation_counter -= 1
            angular_speed_sig = 1
            
            velo.angular.z = 0.7 * self.mutex_trn_rnd
            velo.angular.x = 0.0
        elif self.command == "go_foward": #would be more optmized with a switch :(
            velo.linear.x = self.robot_linear_speed
            velo.angular.z = 0.0
        elif self.command == "turn_right" and self.robot_linear_speed == self.robot_middle_linear_speed:
            velo.linear.x = self.robot_middle_linear_speed * 0.5
            velo.angular.z = min(self.robot_right_angular_speed,self.robot_max_angular_speed)
            #print("right turn", self.robot_right_angular_speed )

        elif self.command == "turn_left"and self.robot_linear_speed == self.robot_middle_linear_speed:
            velo.linear.x = self.robot_middle_linear_speed * 0.5
            #print("left turn", self.robot_left_angular_speed )
            velo.angular.z = -min(self.robot_left_angular_speed,self.robot_max_angular_speed)
        elif self.command == "turn_right":
            velo.linear.x = 0.0
            velo.angular.z = min(self.robot_right_angular_speed,self.robot_max_angular_speed)
            #print("right turn", self.robot_right_angular_speed )

        elif self.command == "turn_left":
            velo.linear.x = 0.0
            #print("left turn", self.robot_left_angular_speed )
            velo.angular.z = -min(self.robot_left_angular_speed,self.robot_max_angular_speed)
        else:
            return 0
        ##print(velo)
        print(velo.linear.x)
        self.velocity_publisher.publish(velo)

    #def turn_to_rnd_position(self):
   

        
      

    
                    
            
        

       
def main(args=None):
    #print('Its working now ')
    rclpy.init(args=args)
    safe_rnd_move_controller = Move_Randomly()  
    rclpy.spin(safe_rnd_move_controller)
    safe_rnd_move_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()

           
#'''
       
      


