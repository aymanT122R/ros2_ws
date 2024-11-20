#Import the relevant libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Topic_Sub(Node):
    def __init__(self,name):
        super().__init__(name)  
        #The create_subscription used to create the subscriber is: topic data type, topic name, callback function name, queue length
        self.sub = self.create_subscription(String,"/topic_demo",self.sub_callback,1) 
    #Callback function executor: prints the received information
    def sub_callback(self,msg):
        print(msg.data)
def main():
    rclpy.init() #ROS2 Python interface initialization
    sub_demo = Topic_Sub("subscriber_node") #Create an object and initialize it
    rclpy.spin(sub_demo)
