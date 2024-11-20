    
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # Spawn the robot in Gazebo
        ExecuteProcess(
            cmd=['ign', 'gazebo','empty.sdf'],
            output='screen'
        ),
        
        # Spawn the URDF model
        Node(
            package='simulation',
            executable='spawn_entity.py',
            arguments=['-file', 'urdf/structure.urdf', '-entity', 'structure'],
            output='screen'
        ),

        # Joint State Publisher
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen'
        ),

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': 'structure.urdf'}]
        ),

        # Controller Spawner
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        ),
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_trajectory_controller', '--controller-manager', '/controller_manager'],
        )
    ])
