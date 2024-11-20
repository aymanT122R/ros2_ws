import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class DetectionInfoSubscriber(Node):
    def __init__(self):
        super().__init__('publisher_node')

        # Subscriber for detection information
        self.subscription = self.create_subscription(
            String,
            'yolo/detection',
            self.detection_info_callback,
            10
        )

    def detection_info_callback(self, msg):
        # Print the received detection information
        self.get_logger().info(f"Received detection information:\n{msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = DetectionInfoSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
