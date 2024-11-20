import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/dia/ros2_ws/src/install/urdf_tutorial_r2d2'
