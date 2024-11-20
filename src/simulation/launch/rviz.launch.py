from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    # Define paths to the URDF and SRDF files
    urdf_file = os.path.join(get_package_share_directory('simulation'), 'urdf', 'structure.urdf')
    srdf_file = os.path.join(get_package_share_directory('simulation'), 'config', 'structure.srdf')  # Ensure you have this file

    # Load the URDF and SRDF as parameters
    robot_description_param = {'robot_description': open(urdf_file).read()}
    robot_description_semantic_param = {'robot_description_semantic': open(srdf_file).read()}

    # Manually define kinematics parameters
    # Manually define kinematics parameters
    kinematics_params = {
    'ros__parameters': {
        'planning_plugin': 'ompl_interface/OMPLPlanner',  # Specify the planning plugin
        'kinematics': {
            'manipulator': {
                'type': 'kdl_kinematics_plugin/KDLKinematicsPlugin',  # Specify the IK solver type
                'joint_names': [
                    'Joint_1',
                    'Joint_2',
                    'Joint_3',
                    'Joint_4',
                    'Joint_5',
                    'Joint_6'
                    ]
                }
            }
        }
    }


    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[robot_description_param, robot_description_semantic_param]
        ),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', os.path.join(get_package_share_directory('simulation'), 'rviz', 'your_robot.rviz')]
        ),
        Node(
    	    package='moveit_ros_move_group',
    	    executable='move_group',
     	    name='move_group',
    	    output='screen',
    	    parameters=[kinematics_params, robot_description_param, robot_description_semantic_param]
        )
    ])

