from glob import glob

from setuptools import find_packages, setup

package_name = 'emotion_aware_assistant'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mazen Ben Abid',
    maintainer_email='mazen.benabid@enstab.ucar.tn',
    description='Emotion-aware conversational assistant built on ROS 2 and Transformers.',
    license='MIT',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'emotion_classifier = emotion_aware_assistant.emotion_classifier:main',
            'response_synthesis = emotion_aware_assistant.response_synthesis:main',
            'user_interface = emotion_aware_assistant.user_interface:main',
        ],
    },
)
