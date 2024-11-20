import rospy
from std_msgs.msg import Float32MultiArray
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)  # Initialize PCA9685 driver

def servo_callback(data):
    # Data contains angles for each of the 13 servos
    for i in range(13):
        angle = data.data[i]
        kit.servo[i].angle = angle

def servo_control_node():
    rospy.init_node('servo_control_node', anonymous=True)
    rospy.Subscriber('/servo_commands', Float32MultiArray, servo_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        servo_control_node()
    except rospy.ROSInterruptException:
        pass
