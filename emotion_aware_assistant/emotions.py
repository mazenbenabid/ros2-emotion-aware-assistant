"""Emotion taxonomy and canned responses.

This module is pure Python (no ROS dependency) so the core logic of the
system can be unit-tested anywhere, including in CI.
"""

import random
from typing import Optional

#: The 7 coarse emotions the system reasons about.
BASIC_EMOTIONS = ('anger', 'fear', 'joy', 'love', 'sadness', 'surprise', 'neutral')

#: Maps the 28 fine-grained GoEmotions labels predicted by the model
#: to one of the 7 basic emotions above.
GO_EMOTIONS_TO_BASIC = {
    'admiration': 'love',
    'amusement': 'joy',
    'anger': 'anger',
    'annoyance': 'anger',
    'approval': 'joy',
    'caring': 'love',
    'confusion': 'surprise',
    'curiosity': 'surprise',
    'desire': 'love',
    'disappointment': 'sadness',
    'disapproval': 'anger',
    'disgust': 'anger',
    'embarrassment': 'sadness',
    'excitement': 'joy',
    'fear': 'fear',
    'gratitude': 'love',
    'grief': 'sadness',
    'joy': 'joy',
    'love': 'love',
    'nervousness': 'fear',
    'optimism': 'joy',
    'pride': 'joy',
    'realization': 'surprise',
    'relief': 'joy',
    'remorse': 'sadness',
    'sadness': 'sadness',
    'surprise': 'surprise',
    'neutral': 'neutral',
}

#: Empathetic replies for each basic emotion (one is picked at random).
RESPONSES = {
    'anger': (
        "I can see you're upset. Want to talk about it?",
        "That sounds frustrating. What happened?",
        "It's okay to feel angry. I'm here to listen.",
    ),
    'fear': (
        "I understand you're scared. How can I support you?",
        "That sounds worrying. What's on your mind?",
        "You're not alone in this. Tell me more.",
    ),
    'joy': (
        "I'm glad you're happy! What's the reason?",
        "That's great news! Tell me more.",
        "Love that energy! What made your day?",
    ),
    'love': (
        "Love is amazing, share more!",
        "That's really heartwarming. Tell me more!",
        "It sounds like that means a lot to you.",
    ),
    'sadness': (
        "I'm sorry you're sad. How can I help?",
        "That sounds hard. Do you want to talk about it?",
        "I'm here for you. What's been going on?",
    ),
    'surprise': (
        "Wow, that's surprising! What happened?",
        "I didn't see that coming! Tell me more.",
        "Interesting! How do you feel about it?",
    ),
    'neutral': (
        "I'm listening, go ahead.",
        "Got it. Tell me more.",
        "Okay, what else is on your mind?",
    ),
}

FALLBACK_RESPONSE = "I don't understand that emotion yet. Can you clarify?"


def to_basic_emotion(label: str) -> Optional[str]:
    """Return the basic emotion for a GoEmotions label, or None if unknown."""
    return GO_EMOTIONS_TO_BASIC.get(label.strip().lower())


def pick_response(emotion: str, rng: random.Random = random) -> str:
    """Pick a reply for a basic emotion, falling back to a generic one."""
    options = RESPONSES.get(emotion.strip().lower())
    if not options:
        return FALLBACK_RESPONSE
    return rng.choice(options)
