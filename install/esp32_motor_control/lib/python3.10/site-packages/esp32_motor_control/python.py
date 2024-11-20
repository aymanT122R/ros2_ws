import rclpy
from rclpy.node import Node
import socket
from std_msgs.msg import String

class MotorControlNode(Node):
    def __init__(self):
        super().__init__('motor_control_node')
        
        # Create UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.esp32_ip = "192.168.1.100"  # IP address of the ESP32
        self.esp32_port = 4210  # The port ESP32 is listening to
        
        # Create a subscriber to listen for motor commands
        self.subscription = self.create_subscription(
            String,
            'motor_commands',
            self.command_callback,
            10)
    
    def command_callback(self, msg):
        # Send the motor command via UDP to the ESP32
        command = msg.data
        self.get_logger().info(f'Sending command: {command}')
        self.udp_socket.sendto(command.encode(), (self.esp32_ip, self.esp32_port))


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

