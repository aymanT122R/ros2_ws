#Import the relevant library files
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class Service_Server(Node):
    def __init__(self,name):
        super().__init__(name)
        #To create a server, use create_service function, and the parameters passed in are:
        #The data type of the service data, the name of the service, and the service callback function (that is, the content of the service)
        self.srv = self.create_service(AddTwoInts, '/add_two_ints', self.Add2Ints_callback)
    #The content of the service callback function here is to add two integer numbers and return the result of the addition
    def Add2Ints_callback(self,request,response):
        response.sum = request.a + request.b
        print("response.sum = ",response.sum)
        return response
def main():
    rclpy.init()
    server_demo = Service_Server("publisher_node")
    rclpy.spin(server_demo)
