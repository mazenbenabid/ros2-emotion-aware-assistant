"""Interactive terminal front-end for the emotion-aware assistant.

Publishes  : /text_input       (std_msgs/String)  what the user types
Subscribes : /emotion_output   (std_msgs/String)  detected emotion
             /response_output  (std_msgs/String)  system reply
"""

import time

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String

EXIT_WORDS = ('quit', 'exit')


class UserInterfaceNode(Node):
    """Reads user input, sends it to the pipeline and prints the result."""

    def __init__(self):
        super().__init__('user_interface')
        self.declare_parameter('response_timeout', 15.0)
        self.response_timeout = float(self.get_parameter('response_timeout').value)

        self.publisher = self.create_publisher(String, '/text_input', 10)
        self.emotion_subscription = self.create_subscription(
            String, '/emotion_output', self.emotion_callback, 10
        )
        self.response_subscription = self.create_subscription(
            String, '/response_output', self.response_callback, 10
        )
        self.current_emotion = None
        self.current_response = None
        self.get_logger().info('User Interface node ready.')

    def emotion_callback(self, msg: String) -> None:
        self.current_emotion = msg.data

    def response_callback(self, msg: String) -> None:
        self.current_response = msg.data

    def send_and_wait(self, text: str) -> None:
        """Publish one message and wait for its emotion and response."""
        if self.publisher.get_subscription_count() == 0:
            print('[!] Nobody is listening on /text_input. Is emotion_classifier running?')
            return

        self.current_emotion = None
        self.current_response = None
        self.publisher.publish(String(data=text))

        # Emotion and response arrive on two different topics, so their order is
        # not guaranteed: wait for both, with a timeout so the UI never hangs.
        deadline = time.monotonic() + self.response_timeout
        while rclpy.ok() and time.monotonic() < deadline:
            if self.current_emotion is not None and self.current_response is not None:
                break
            rclpy.spin_once(self, timeout_sec=0.1)

        if self.current_response is None:
            print(f'[!] No response after {self.response_timeout:g}s. '
                  'Check that all nodes are running.')
            return
        print(f'Detected emotion: {self.current_emotion or "unknown"}')
        print(f'System response:  {self.current_response}')

    def run(self) -> None:
        print("Emotion-aware assistant. Type a message, or 'quit' to exit.\n")
        while rclpy.ok():
            try:
                text = input('You: ').strip()
            except EOFError:
                break
            if not text:
                continue
            if text.lower() in EXIT_WORDS:
                break
            self.send_and_wait(text)
            print()


def main(args=None):
    rclpy.init(args=args)
    node = UserInterfaceNode()
    try:
        node.run()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
