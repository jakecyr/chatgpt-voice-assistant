import pytest

from chatgpt_voice_assistant.exceptions.text_generation_error import TextGenerationError
from chatgpt_voice_assistant.open_ai_text_generator import OpenAITextGenerator


def test_init_defaults_model():
    text_generator = OpenAITextGenerator(
        open_ai_key="some-key", max_tokens=100, previous_responses=[]
    )

    assert isinstance(text_generator._model, str)


def test_init_defaults_tokens():
    text_generator = OpenAITextGenerator(open_ai_key="some-key", previous_responses=[])

    assert isinstance(text_generator._max_tokens, int)


def test_throws_error_if_key_is_none():
    with pytest.raises(TextGenerationError):
        OpenAITextGenerator(open_ai_key=None, max_tokens=100, previous_responses=[])  # type: ignore


def test_throws_error_if_key_is_empty():
    with pytest.raises(TextGenerationError):
        OpenAITextGenerator(open_ai_key="", max_tokens=100, previous_responses=[])


def test_throws_error_if_key_is_not_a_string():
    with pytest.raises(TextGenerationError):
        OpenAITextGenerator(open_ai_key=True, max_tokens=100, previous_responses=[])  # type: ignore
