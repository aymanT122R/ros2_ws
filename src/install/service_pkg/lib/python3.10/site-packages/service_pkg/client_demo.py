#Import the relevant libraries
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class Service_Client(Node):
    def __init__(self,name):
        super().__init__(name)
        #To create a client, you use create_client function, and the parameters passed in are the data type of the service data and the topic name of the service
        self.client = self.create_client(AddTwoInts,'/add_two_ints')
        #Cycle through and wait for the server side to start successfully
        while not self.client.wait_for_service(timeout_sec=1.0):
            print("service not available, waiting again...")
        #Create a data object for the service request
        self.request = AddTwoInts.Request()
        
    def send_request(self): 
        self.request.a = 10
        self.request.b = 90
        #Send a service request
        self.future = self.client.call_async(self.request)
        
def main():
    rclpy.init() #Node initialization
    service_client = Service_Client("client_node") #Create an object
    service_client.send_request() #Send a service request
    while rclpy.ok():
        rclpy.spin_once(service_client)
        #Determine whether the data processing is complete
        if service_client.future.done():
            try:
                #Get service feedback information and print it
                response = service_client.future.result()
                print("Result = ",response.sum)
            except Exception as e:
                service_client.get_logger().info('Service call failed %r' % (e,))
            
        break
