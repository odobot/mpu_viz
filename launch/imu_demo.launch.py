#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory  # Import ROS 2 function

def generate_launch_description():
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    # get_package_share_directory('mpu_6050_driver')
    turtlebot3_cartographer_prefix = get_package_share_directory('mpu_viz')
    cartographer_config_dir = LaunchConfiguration('cartographer_config_dir', default=os.path.join(
                                                  turtlebot3_cartographer_prefix, 'config'))
    configuration_basename = LaunchConfiguration('configuration_basename',
                                                 default='turtlebot3_lds_2d.lua')

    resolution = LaunchConfiguration('resolution', default='0.05')
    publish_period_sec = LaunchConfiguration('publish_period_sec', default='1.0')

    rviz_config_dir = os.path.join(get_package_share_directory('mpu_viz'),
                                   'rviz', 'tb3_cartographer.rviz')
    
    urdf_file = os.path.join(
        get_package_share_directory('mpu_viz'), 'urdf', 'plane.urdf')

    return LaunchDescription([
        DeclareLaunchArgument(
            'urdf_file',
            default_value=os.path.join(get_package_share_directory('mpu_viz'), 'urdf', 'plane.urdf'),
            description='Full path to the URDF file to be loaded'
        ),
        
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('urdf_file')])}],
        ),

        Node(
            package='mpu_viz', 
            executable='imu_node.py', 
            name="imu_node",
            output='screen'),
            
        Node(
            package='mpu_viz', 
            executable='tf_broadcaster_imu.py',
            name="tf_broadcaster_imu", 
            output='screen'),
        
    ])

