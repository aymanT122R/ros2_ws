import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class DisplayNode(Node):
    def __init__(self):
        super().__init__('display_node')
        
        # Create a subscription to the 'image/raw' topic
        self.subscription = self.create_subscription(
            Image,
            'yolo/detection',
            self.image_callback,
            1000
        )
        
        # Initialize the CvBridge class
        self.bridge = CvBridge()

    def image_callback(self, msg):
        # Convert the ROS Image message to an OpenCV image
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        # Display the image in an OpenCV window
        cv2.imshow("ESP32-CAM Stream", frame)

        # Handle OpenCV window events (required to render the image)
        cv2.waitKey(1)

    def destroy_node(self):
        # Destroy OpenCV windows before shutting down the node
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = DisplayNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
