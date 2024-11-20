from setuptools import find_packages, setup

package_name = 'esp32_motor_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dia',
    maintainer_email='dia@todo.todo',
    description='ROS 2 package to control motors on an ESP32 robot over Wi-Fi',
    license='TODO: License declaration',  # Replace with your actual license
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Add entry point for your motor control node here
            'motor_control_node = esp32_motor_control.motor_control_node:main',  # Ensure this points to your main function
        ],
    },
)

