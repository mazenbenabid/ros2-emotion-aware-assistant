"""Unit tests for the ROS-independent emotion logic."""

import random

from emotion_aware_assistant.emotions import (
    BASIC_EMOTIONS,
    FALLBACK_RESPONSE,
    GO_EMOTIONS_TO_BASIC,
    RESPONSES,
    pick_response,
    to_basic_emotion,
)


def test_all_28_go_emotions_labels_are_mapped():
    assert len(GO_EMOTIONS_TO_BASIC) == 28


def test_every_label_maps_to_a_basic_emotion():
    assert set(GO_EMOTIONS_TO_BASIC.values()) <= set(BASIC_EMOTIONS)


def test_every_basic_emotion_is_reachable_and_has_responses():
    assert set(GO_EMOTIONS_TO_BASIC.values()) == set(BASIC_EMOTIONS)
    for emotion in BASIC_EMOTIONS:
        assert RESPONSES[emotion], f'No response for {emotion}'


def test_to_basic_emotion_is_case_insensitive():
    assert to_basic_emotion('Gratitude') == 'love'
    assert to_basic_emotion(' nervousness ') == 'fear'


def test_unknown_label_returns_none():
    assert to_basic_emotion('boredom') is None


def test_pick_response_returns_a_reply_for_the_emotion():
    reply = pick_response('joy', rng=random.Random(0))
    assert reply in RESPONSES['joy']


def test_pick_response_falls_back_for_unknown_emotion():
    assert pick_response('boredom') == FALLBACK_RESPONSE
