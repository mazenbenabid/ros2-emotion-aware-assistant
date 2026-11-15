"""ROS 2 node that turns a detected emotion into an empathetic reply.

Subscribes : /emotion_output   (std_msgs/String)  basic emotion
Publishes  : /response_output  (std_msgs/String)  reply shown to the user
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String

from emotion_aware_assistant.emotions import pick_response


class ResponseSynthesisNode(Node):
    """Selects a reply adapted to the user's emotion."""

    def __init__(self):
        super().__init__('response_synthesis')
        self.subscription = self.create_subscription(
            String, '/emotion_output', self.emotion_callback, 10
        )
        self.publisher = self.create_publisher(String, '/response_output', 10)
        self.get_logger().info('Response Synthesis node ready.')

    def emotion_callback(self, msg: String) -> None:
        response = pick_response(msg.data)
        self.publisher.publish(String(data=response))
        self.get_logger().info(f"Emotion '{msg.data}' -> response: {response}")


def main(args=None):
    rclpy.init(args=args)
    node = ResponseSynthesisNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
