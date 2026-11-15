"""Start the processing nodes (classifier + response synthesis).

The interactive user_interface node reads from the keyboard, so it is run
separately in its own terminal with `ros2 run`.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

PACKAGE = 'emotion_aware_assistant'


def generate_launch_description():
    model_name = DeclareLaunchArgument(
        'model_name',
        default_value='SamLowe/roberta-base-go_emotions',
        description='Hugging Face model used by the emotion classifier',
    )

    return LaunchDescription([
        model_name,
        Node(
            package=PACKAGE,
            executable='emotion_classifier',
            name='emotion_classifier',
            output='screen',
            parameters=[{'model_name': LaunchConfiguration('model_name')}],
        ),
        Node(
            package=PACKAGE,
            executable='response_synthesis',
            name='response_synthesis',
            output='screen',
        ),
    ])
