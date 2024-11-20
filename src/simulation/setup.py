from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'simulation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include your launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        # Include any configuration or other resource files you might have (like URDF, YAML, etc.)
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'config'), glob('config/*.srdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dia',
    maintainer_email='dia@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Add any Python scripts you need to run
        ],
    },
)
