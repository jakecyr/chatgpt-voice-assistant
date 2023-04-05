import pytest

from chatgpt_voice_assistant.exceptions.text_generation_error import \
    TextGenerationError
from chatgpt_voice_assistant.open_ai_text_generator import OpenAITextGenerator


def test_throws_error_if_key_is_none():
    with pytest.raises(TextGenerationError):
        OpenAITextGenerator(open_ai_key=None, max_tokens=100, previous_responses=[])


def test_throws_error_if_key_is_empty():
    with pytest.raises(TextGenerationError):
        OpenAITextGenerator(open_ai_key="", max_tokens=100, previous_responses=[])


def test_throws_error_if_key_is_not_a_string():
    with pytest.raises(TextGenerationError):
        OpenAITextGenerator(open_ai_key=True, max_tokens=100, previous_responses=[])
