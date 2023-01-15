#!/usr/bin/env python3

import os

import os
from ament_index_python.packages import get_package_share_directory
import launch
from launch_ros.actions import Node

def generate_launch_description():
    my_package_dir = get_package_share_directory('pkg_mother')
    return launch.LaunchDescription([
        Node(package='rviz2',
             executable='rviz2',
             arguments=['-d', os.path.join('/home/bot/ros2_ws/larm-mother/pkg_mother', 'rviz2_config_challenge-1.rviz')])
    ])
