import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class ESP32CamNode(Node):
    def __init__(self):
        super().__init__('esp32_cam_node')
        
        # Publisher for the image stream
        self.publisher_ = self.create_publisher(Image, 'esp32_cam/image_raw', 10)

        # Create OpenCV VideoCapture object
        self.camera_url = "http://192.168.1.192:81/stream"
        self.cap = cv2.VideoCapture(self.camera_url)

        if not self.cap.isOpened():
            self.get_logger().error("Error: Could not open video stream.")
            exit()

        self.bridge = CvBridge()

        # Timer to publish images at a set frequency
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 FPS

    def timer_callback(self):
        ret, frame = self.cap.read()
        
        if not ret:
            self.get_logger().error("Error: Failed to capture image.")
            return

        # Convert OpenCV image to ROS2 Image message and publish
        image_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        self.publisher_.publish(image_msg)
        self.get_logger().info("Published image frame")

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ESP32CamNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
