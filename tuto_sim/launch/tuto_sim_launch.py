import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription , ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    
    tbot_sim_path = get_package_share_directory('tbot_sim')
    tuto_sim_path = get_package_share_directory('tuto_sim')
    
    
    launch_tuto_file_dir = os.path.join(tbot_sim_path, 'launch')
    launch_rviz_file_dir = '/home/bot/ros2_ws/tuto_sim'

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_tuto_file_dir, '/challenge-1.launch.py']),
            ),
       

    ExecuteProcess(
        cmd=['rviz2','-d', launch_rviz_file_dir],output='screen'
    ),
    Node(
        package='teleop_twist_keyboard',
        executable= 'teleop_twist_keyboard',
        name='teleop',
        prefix="gnome-terminal -x" 
    ),
     ])
