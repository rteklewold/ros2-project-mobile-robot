import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    package_dir = get_package_share_directory('rover')
    urdf = os.path.join(package_dir, 'rover.urdf')

    return LaunchDescription([
        Node(
            package = 'robot_state_publisher',
            executable = 'robot_state_publisher',
            name = 'robot_state_publisher',
            output = 'screen',
            arguments = [urdf]),
        Node(
            package = 'joint_state_publisher',
            executable = 'joint_state_publisher',
            name = 'joint_state_publisher',
            arguments = [urdf]),
        # Node(
        #     package = 'rviz2',
        #     executable = 'rviz2',
        #     name = 'rviz2',
        #     output = 'screen'),
        ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'], 
                       output = 'screen'),
        Node (package='gazebo_ros',
              executable = 'spawn_entity.py',
              name = 'urdf_spawner',
              output = 'screen',
              arguments=["-topic", "/robot_description", "-entity", "rover"])

    ])