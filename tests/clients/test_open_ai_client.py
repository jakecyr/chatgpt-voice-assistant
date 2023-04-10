from typing import Any, Dict, List

import mock
from pytest import fixture, raises

from chatgpt_voice_assistant.clients.open_ai_client import OpenAIClient
from chatgpt_voice_assistant.exceptions.text_generation_error import TextGenerationError
from chatgpt_voice_assistant.models.open_ai_chat_completion import ChatCompletionMessage

OPEN_AI_KEY = "fake-key"

MOCK_RESPONSE_STOP_DUE_TO_LENGTH: Dict[str, Any] = {
    "index": 0,
    "finish_reason": "length",
    "message": {
        "role": "assistant",
        "content": "Hello",
    },
}

MOCK_RESPONSES: List[Dict[str, Any]] = [
    {
        "index": 0,
        "finish_reason": "stop",
        "message": {
            "role": "assistant",
            "content": "Hello",
        },
    },
    {
        "index": 1,
        "finish_reason": "stop",
        "message": {
            "role": "assistant",
            "content": "Hello there! How are you?",
        },
    },
]


@fixture
def open_ai_client():
    return OpenAIClient(OPEN_AI_KEY)


def mock_create_completion_no_responses(**kwargs):
    return {"choices": [], "usage": {"total_tokens": kwargs["max_tokens"]}}


def mock_create_completion_multiple_responses(**kwargs):
    return {"choices": MOCK_RESPONSES, "usage": {"total_tokens": kwargs["max_tokens"]}}


def mock_create_completion_stop_due_to_length(**kwargs):
    return {
        "choices": [MOCK_RESPONSE_STOP_DUE_TO_LENGTH],
        "usage": {"total_tokens": kwargs["max_tokens"]},
    }


@mock.patch("openai.ChatCompletion.create", mock_create_completion_no_responses)
def test_get_chat_completion_throws_exception_no_responses(
    open_ai_client: OpenAIClient,
):
    max_tokens = 70

    message: ChatCompletionMessage = {
        "role": "user",
        "content": "Yeah do you have one in mind?",
    }

    with raises(TextGenerationError):
        open_ai_client.get_chat_completion(messages=[message], max_tokens=max_tokens)


@mock.patch("openai.ChatCompletion.create", mock_create_completion_no_responses)
def test_get_chat_completion_throws_exception_if_no_messages_are_inputted(
    open_ai_client: OpenAIClient,
):
    max_tokens = 70

    with raises(ValueError):
        open_ai_client.get_chat_completion(messages=[], max_tokens=max_tokens)


@mock.patch("openai.ChatCompletion.create", mock_create_completion_multiple_responses)
def test_get_chat_completion_returns_first_response(open_ai_client: OpenAIClient):
    max_tokens = 70
    message: ChatCompletionMessage = {
        "role": "user",
        "content": "Yeah do you have one in mind?",
    }

    response = open_ai_client.get_chat_completion(
        messages=[message], max_tokens=max_tokens
    )

    assert response is not None
    assert response.content == MOCK_RESPONSES[0]["message"]["content"]
    assert response.role == "assistant"
    assert not response.was_cut_short


@mock.patch("openai.ChatCompletion.create", mock_create_completion_stop_due_to_length)
def test_get_chat_completion_sets_was_cut_short_to_true(open_ai_client: OpenAIClient):
    max_tokens = 70
    message: ChatCompletionMessage = {
        "role": "user",
        "content": "Yeah do you have one in mind?",
    }

    response = open_ai_client.get_chat_completion(
        messages=[message], max_tokens=max_tokens
    )

    assert response is not None
    assert response.content == MOCK_RESPONSE_STOP_DUE_TO_LENGTH["message"]["content"]
    assert response.was_cut_short
