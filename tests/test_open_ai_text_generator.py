import pytest

from gpt3_assistant.exceptions.text_generation_error import TextGenerationError
from gpt3_assistant.models.exchange import Exchange
from gpt3_assistant.open_ai_text_generator import OpenAITextGenerator

OPEN_AI_KEY = "fake-key"
MOCK_RESPONSES = [
    {"finish_reason": "stop", "text": "hey there"},
    {"finish_reason": "stop", "text": "what's up"},
]


def mock_create_completion_no_responses(**kwargs):
    return {"choices": [], "usage": {"total_tokens": kwargs["max_tokens"]}}


def mock_create_completion_multiple_responses(**kwargs):
    return {"choices": MOCK_RESPONSES, "usage": {"total_tokens": kwargs["max_tokens"]}}


def test_throws_error_if_key_is_none():
    with pytest.raises(TextGenerationError):
        OpenAITextGenerator(open_ai_key=None, max_tokens=100, previous_responses=[])


def test_throws_error_if_key_is_empty():
    with pytest.raises(TextGenerationError):
        OpenAITextGenerator(open_ai_key="", max_tokens=100, previous_responses=[])


def test_throws_error_if_key_is_not_a_string():
    with pytest.raises(TextGenerationError):
        OpenAITextGenerator(open_ai_key=True, max_tokens=100, previous_responses=[])


def test_get_request_under_max_tokens_shows_all_previous():
    max_tokens = 150
    prompt = "Do you have something in mind?"
    previous_responses = [
        Exchange("Hey", "Hey there"),
        Exchange("What's up", "Not much"),
    ]

    open_ai_text_generator = OpenAITextGenerator(
        OPEN_AI_KEY, max_tokens=max_tokens, previous_responses=previous_responses
    )

    request = open_ai_text_generator._get_request_under_max_tokens(prompt)
    expected_request = f"\nUser: Hey\nAssistant: Hey there\nUser: What's up\nAssistant: Not much\nUser: {prompt}\nAssistant: "

    assert request == expected_request, f"Expected different request"


def test_get_request_under_max_tokens_maxes_out():
    max_tokens = 70
    prompt = "Yeah do you have one in mind?"
    previous_responses = [
        Exchange("Hey", "Hey there"),
        Exchange("What's up", "Not much. Wanna see a movie?"),
    ]

    open_ai_text_generator = OpenAITextGenerator(
        OPEN_AI_KEY, max_tokens=max_tokens, previous_responses=previous_responses
    )

    request = open_ai_text_generator._get_request_under_max_tokens(prompt)
    expected_request = f"\nUser: {prompt}\nAssistant: "

    assert request == expected_request, f"Expected different request"


def test_get_request_under_max_tokens_no_previous():
    max_tokens = 70
    prompt = "Yeah do you have one in mind?"
    previous_responses = []

    open_ai_text_generator = OpenAITextGenerator(
        OPEN_AI_KEY, max_tokens=max_tokens, previous_responses=previous_responses
    )

    request = open_ai_text_generator._get_request_under_max_tokens(prompt)
    expected_request = f"\nUser: {prompt}\nAssistant: "

    assert request == expected_request, f"Expected different request"
