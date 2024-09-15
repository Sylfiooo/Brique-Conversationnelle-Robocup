from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'stt'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'lib' ), glob('lib/*')),
        (os.path.join('share', package_name, 'modele' ), glob('modele/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vincent.buniazet',
    maintainer_email='vincent.buniazet@cpe.fr',
    description='Package de reconnaissance vocale',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'stt = stt.STT_Whisper_cpp:main'
        ],
    },
)
