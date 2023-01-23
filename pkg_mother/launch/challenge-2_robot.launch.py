#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    tbot_sim_path = get_package_share_directory('tbot_sim')
    tbot_slam_path = get_package_share_directory('slam_toolbox')
    launch_file_dir = os.path.join(tbot_sim_path, 'launch')
    launch_slam_dir = os.path.join(tbot_slam_path, 'launch')
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/challenge-1.launch.py']),
            PythonLaunchDescriptionSource([ launch_slam_dir, '/online_sync_launch.py' ]),
            launch_arguments={
                'use_sim_time:=False',
               
            }.items()),
        Node(
            package='tuto_move',
            executable='scan_echo',
            name="scan_echo"),
        Node(
            package='pkg_mother',
            executable='mv_rand',
            name="mv_rand",
           ),
        
        Node(
            package='tuto_vision',
            executable='camera',
            name="camera"),
        
        Node( 
            package='pkg_mother',
            executable='centroid',
            name="centroid"),
        
        # Node(
        #     package='pkg_mother',
        #     executable='',
        #     name="centroid")
        ])
        


    
            ])
         