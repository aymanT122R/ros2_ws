# my_robot_control/robot_control.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RobotControlNode(Node):
    def __init__(self):
        super().__init__('robot_control_node')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        # Set robot's velocity
        msg.linear.x = 0.5  # Move forward at a constant speed
        msg.angular.z = 0.0  # No rotation
        self.publisher.publish(msg)
        self.get_logger().info('Publishing velocity: linear.x = 0.5')

def main(args=None):
    rclpy.init(args=args)
    node = RobotControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

