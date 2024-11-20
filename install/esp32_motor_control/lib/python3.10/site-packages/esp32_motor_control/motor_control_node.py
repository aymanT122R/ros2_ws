import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket

class MotorControlNode(Node):
    def __init__(self):
        super().__init__('motor_control_node')

        # Create UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.esp32_ip = "192.168.1.100"  # IP address of the ESP32
        self.esp32_port = 4210  # The port ESP32 is listening to

        # Create a subscriber to listen for cmd_vel messages
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',  # Topic for robot velocity commands
            self.cmd_vel_callback,
            10)  # Queue size

    def cmd_vel_callback(self, msg):
        # Extract linear and angular velocities from the Twist message
        linear_x = msg.linear.x  # Forward/backward speed
        angular_z = msg.angular.z  # Turning speed (rotation)

        # Send motor commands via UDP based on velocity inputs
        if linear_x > 0:  # Forward
            self.udp_socket.sendto("FORWARD".encode(), (self.esp32_ip, self.esp32_port))
            self.get_logger().info(f"Moving Forward with speed {linear_x}")
        elif linear_x < 0:  # Backward
            self.udp_socket.sendto("BACKWARD".encode(), (self.esp32_ip, self.esp32_port))
            self.get_logger().info(f"Moving Backward with speed {linear_x}")
        else:  # Stop
            self.udp_socket.sendto("STOP".encode(), (self.esp32_ip, self.esp32_port))
            self.get_logger().info("Stopping motors")

        if angular_z > 0:  # Turn right
            self.udp_socket.sendto("RIGHT".encode(), (self.esp32_ip, self.esp32_port))
            self.get_logger().info(f"Turning Right with angular velocity {angular_z}")
        elif angular_z < 0:  # Turn left
            self.udp_socket.sendto("LEFT".encode(), (self.esp32_ip, self.esp32_port))
            self.get_logger().info(f"Turning Left with angular velocity {angular_z}")


def main(args=None):
    rclpy.init(args=args)
    
    motor_control_node = MotorControlNode()
    
    try:
        rclpy.spin(motor_control_node)
    except KeyboardInterrupt:
        pass
    
    motor_control_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

