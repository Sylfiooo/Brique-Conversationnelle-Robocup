from setuptools import setup

package_name = 'tts'
submodules = "tts/submodules"

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name, submodules],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lucas_coudrais',
    maintainer_email='lucas.coudrais@gmail.com',
    description='Ros package for TTS only',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tts = tts.tts:main',
            'test_client = tts.test_client:main',
        ],
    },
)
