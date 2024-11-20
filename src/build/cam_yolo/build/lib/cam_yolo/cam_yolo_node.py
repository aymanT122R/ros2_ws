import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
import cv2
from cv_bridge import CvBridge
from ultralytics import YOLO

class YoloESP32CamNode(Node):
    def __init__(self):
        super().__init__('cam_yolo_node')

        # Publisher for the detected objects information
        self.detection_info_publisher_ = self.create_publisher(String, 'yolo/detection', 10)

        # Publisher for the image with bounding boxes
        self.image_publisher_ = self.create_publisher(Image, 'yolo/image', 1)

        # Create OpenCV VideoCapture object for ESP32-CAM
        self.camera_url = "http://192.168.1.71:81/stream"
        self.cap = cv2.VideoCapture(self.camera_url)

        if not self.cap.isOpened():
            self.get_logger().error("Error: Could not open video stream.")
            exit()

        self.bridge = CvBridge()

        # Timer to capture and process images at a set frequency
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 FPS

        # Load the YOLO model (replace 'yolov8s.pt' with your own model path)
        self.model = YOLO('yolov8s.pt')  # Replace with the actual path to your model

    def timer_callback(self):
        ret, frame = self.cap.read()
        
        if not ret:
            self.get_logger().error("Error: Failed to capture image.")
            return

        # Run YOLO model inference on the captured frame
        results = self.model(frame)

        # Initialize a list to store detection information
        detections_info = []

        # Extract bounding boxes and class names, and draw them on the image
        for result in results:
            boxes = result.boxes.xyxy  # Bounding box coordinates
            confidences = result.boxes.conf  # Confidence scores
            class_ids = result.boxes.cls  # Class IDs

            for box, conf, cls in zip(boxes, confidences, class_ids):
                if conf > 0.6:  # Set a confidence threshold
                    x1, y1, x2, y2 = map(int, box)  # Convert to integer pixel coordinates

                    # Get class name from class ID
                    class_name = self.model.names[int(cls)] if int(cls) < len(self.model.names) else "Unknown"

                    # Draw the bounding box on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Put class name text on the frame
                    label = f"{class_name} {conf:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Format the detection information
                    detection_info = f"xmin: {x1}, xmax: {x2}, ymin: {y1}, ymax: {y2}, class: {class_name}"
                    detections_info.append(detection_info)

        # Publish the detection information as a single string
        if detections_info:
            detections_string = "\n".join(detections_info)  # Join all detections into a single string
            self.detection_info_publisher_.publish(String(data=detections_string))
            self.get_logger().info(f"Published detection information:\n{detections_string}")

        # Convert the modified frame (with bounding boxes) to a ROS Image message and publish it
        img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        self.image_publisher_.publish(img_msg)
        self.get_logger().info("Published image with bounding boxes")

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = YoloESP32CamNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
