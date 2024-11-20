from setuptools import setup

package_name = 'my_robot_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='Package for controlling robot via Wi-Fi',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'robot_control = my_robot_control.robot_control:main',
    ],
},
)

