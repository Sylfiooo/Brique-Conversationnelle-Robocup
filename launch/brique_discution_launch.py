from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tts',
            executable='tts',
        ),
        Node(
            package='nlp',
            executable='nlp',
        ),
        Node(
            package='stt',
            executable='stt',
        ),
        Node(
            package='main',
            executable='main',
           
        )
    ])
