import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String
import numpy as np

class ControlNode(Node):
    def __init__(self):
        super().__init__('control_node')

        # Subscriber for detection information
        self.subscription = self.create_subscription(
            String,
            'yolo/detection',
            self.detection_info_callback,
            10
        )

        # Publisher for servo commands
        self.servo_pub = self.create_publisher(Float32MultiArray, '/servo_commands', 10)

    def detection_info_callback(self, msg):
        # Print the received detection information
        self.get_logger().info(f"Received detection information:\n{msg.data}")

        # Logic for calculating servo angles based on detection data
        servo_angles = self.calculate_servo_angles(msg.data)

        # Publish the angles to servo node
        self.servo_pub.publish(Float32MultiArray(data=servo_angles))

    def calculate_servo_angles(self, detection):
        # Convert object detection to arm movement, dummy values here
        # For simplicity, assume the detection data contains bounding box coordinates
        # In a real implementation, you would parse this data as needed.
        
        # Here we use dummy values, replace with your logic
        self.get_logger().info("Calculating servo angles based on detection...")
        
        # Return a list of 13 dummy servo angles (e.g., all at 90 degrees)
        return [90.0] * 13  # Example servo angles

def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
