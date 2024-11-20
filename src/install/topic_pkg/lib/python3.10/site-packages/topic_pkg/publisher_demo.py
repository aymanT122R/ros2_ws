import rclpy
from rclpy.node import Node
from std_msgs.msg import String
class Topic_Pub(Node):
    def __init__(self,name):
        super().__init__(name)
        self.pub = self.create_publisher(String,"/topic_demo",1)
        self.timer = self.create_timer(1,self.pub_msg)
        
    def pub_msg(self):
        msg = String()
        msg.data = "Hi,I send a message."
        self.pub.publish(msg)
    
def main():
    rclpy.init()
    pub_demo = Topic_Pub("publisher_node")
    rclpy.spin(pub_demo)
