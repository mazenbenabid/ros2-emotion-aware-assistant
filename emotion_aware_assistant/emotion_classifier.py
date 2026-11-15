"""ROS 2 node that detects the emotion expressed in a text message.

Subscribes : /text_input      (std_msgs/String)  raw user text
Publishes  : /emotion_output  (std_msgs/String)  one of the 7 basic emotions
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String
from transformers import pipeline

from emotion_aware_assistant.emotions import to_basic_emotion

DEFAULT_MODEL = 'SamLowe/roberta-base-go_emotions'


class EmotionClassifierNode(Node):
    """Classifies text with a RoBERTa model fine-tuned on GoEmotions."""

    def __init__(self):
        super().__init__('emotion_classifier')
        self.declare_parameter('model_name', DEFAULT_MODEL)
        self.declare_parameter('top_k', 3)
        model_name = self.get_parameter('model_name').value
        top_k = self.get_parameter('top_k').value

        self.get_logger().info(
            f"Loading model '{model_name}' (downloaded from Hugging Face on first run)..."
        )
        self.classifier = pipeline('text-classification', model=model_name, top_k=top_k)

        self.subscription = self.create_subscription(
            String, '/text_input', self.text_callback, 10
        )
        self.publisher = self.create_publisher(String, '/emotion_output', 10)
        self.get_logger().info('Emotion Classifier node ready.')

    def text_callback(self, msg: String) -> None:
        text = msg.data.strip()
        if not text:
            self.get_logger().warn('Received empty text, skipping.')
            return

        try:
            predictions = self._top_predictions(text)
        except Exception as exc:  # keep the node alive whatever the model raises
            self.get_logger().error(f'Error while classifying text: {exc}')
            return

        if not predictions:
            self.get_logger().warn('Model returned no prediction.')
            return

        label = predictions[0]['label']
        basic_emotion = to_basic_emotion(label)
        if basic_emotion is None:
            self.get_logger().warn(f"Unknown emotion label from model: '{label}'")
            return

        self.publisher.publish(String(data=basic_emotion))
        summary = ', '.join(f"{p['label']} ({p['score']:.2f})" for p in predictions)
        self.get_logger().info(f"Top predictions: {summary} -> published '{basic_emotion}'")

    def _top_predictions(self, text: str) -> list:
        """Run the model and return predictions sorted by decreasing score."""
        # truncation=True avoids a crash on texts longer than the model's 512-token limit.
        result = self.classifier(text, truncation=True)
        # Depending on the transformers version, one input returns either
        # [[{label, score}, ...]] or [{label, score}, ...]: normalise to a flat list.
        if result and isinstance(result[0], list):
            result = result[0]
        return sorted(result, key=lambda p: p['score'], reverse=True)


def main(args=None):
    rclpy.init(args=args)
    node = EmotionClassifierNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
