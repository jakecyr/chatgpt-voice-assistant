import mock
from pytest import fixture, raises

from chatgpt_voice_assistant.clients.open_ai_client import OpenAIClient
from chatgpt_voice_assistant.exceptions.text_generation_error import TextGenerationError
from chatgpt_voice_assistant.models.message import Message
import os
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.completion_usage import CompletionUsage


OPEN_AI_KEY = "fake-key"
os.environ["OPENAI_API_KEY"] = OPEN_AI_KEY

MOCK_RESPONSE_STOP_DUE_TO_LENGTH = Choice(
    message=ChatCompletionMessage(
        content="Hello there! How are you?",
        role="assistant",
    ),
    index=0,
    finish_reason="length",
)

MOCK_RESPONSES: list[Choice] = [
    Choice(
        message=ChatCompletionMessage(
            content="Hello there! How are you?",
            role="assistant",
        ),
        index=0,
        finish_reason="stop",
    ),
    Choice(
        message=ChatCompletionMessage(
            content="I'm doing well! How about you?",
            role="assistant",
        ),
        index=1,
        finish_reason="stop",
    ),
]


@fixture
def open_ai_client() -> OpenAIClient:
    return OpenAIClient(OPEN_AI_KEY)


def mock_create_completion_no_responses(**kwargs):
    return ChatCompletion(
        choices=[],
        usage=CompletionUsage(
            completion_tokens=0, prompt_tokens=0, total_tokens=kwargs["max_tokens"]
        ),
        model="gpt-3.5-turbo",
        created=0,
        id="chatcmpl-6Qp9nJjyCZ2UJyE2oXh8HqL5yq2KJ",
        object="chat.completion",
    )


def mock_create_completion_multiple_responses(**kwargs):
    return ChatCompletion(
        choices=MOCK_RESPONSES,
        usage=CompletionUsage(
            completion_tokens=0, prompt_tokens=0, total_tokens=kwargs["max_tokens"]
        ),
        model="gpt-3.5-turbo",
        created=0,
        id="chatcmpl-6Qp9nJjyCZ2UJyE2oXh8HqL5yq2KJ",
        object="chat.completion",
    )


def mock_create_completion_stop_due_to_length(**kwargs):
    return ChatCompletion(
        choices=[MOCK_RESPONSE_STOP_DUE_TO_LENGTH],
        usage=CompletionUsage(
            completion_tokens=0, prompt_tokens=0, total_tokens=kwargs["max_tokens"]
        ),
        model="gpt-3.5-turbo",
        created=0,
        id="chatcmpl-6Qp9nJjyCZ2UJyE2oXh8HqL5yq2KJ",
        object="chat.completion",
    )


@mock.patch(
    "chatgpt_voice_assistant.clients.open_ai_client.openai.chat.completions.create",
    mock_create_completion_no_responses,
)
def test_get_chat_completion_throws_exception_no_responses(
    open_ai_client: OpenAIClient,
) -> None:
    max_tokens = 70

    message: ChatCompletionMessage = {
        "role": "user",
        "content": "Yeah do you have one in mind?",
    }

    with raises(TextGenerationError):
        open_ai_client.get_chat_completion(messages=[message], max_tokens=max_tokens)


@mock.patch(
    "chatgpt_voice_assistant.clients.open_ai_client.openai.chat.completions.create",
    mock_create_completion_no_responses,
)
def test_get_chat_completion_throws_exception_if_no_messages_are_inputted(
    open_ai_client: OpenAIClient,
) -> None:
    max_tokens = 70

    with raises(ValueError):
        open_ai_client.get_chat_completion(messages=[], max_tokens=max_tokens)


@mock.patch(
    "chatgpt_voice_assistant.clients.open_ai_client.openai.chat.completions.create",
    mock_create_completion_multiple_responses,
)
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
    assert response.content == MOCK_RESPONSES[0].message.content
    assert response.role == "assistant"
    assert not response.was_cut_short


@mock.patch(
    "chatgpt_voice_assistant.clients.open_ai_client.openai.chat.completions.create",
    mock_create_completion_stop_due_to_length,
)
def test_get_chat_completion_sets_was_cut_short_to_true(open_ai_client: OpenAIClient):
    max_tokens = 70
    message: ChatCompletionMessage = {
        "role": "user",
        "content": "Yeah do you have one in mind?",
    }

    response: Message = open_ai_client.get_chat_completion(
        messages=[message], max_tokens=max_tokens
    )

    assert response is not None
    assert response.content == MOCK_RESPONSE_STOP_DUE_TO_LENGTH.message.content
    assert response.was_cut_short
