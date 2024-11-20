from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    turtle_node = Node(
            package='turtlesim',
            executable='turtlesim_node',
                )
    launch_description = LaunchDescription([turtle_node])
    return launch_description
