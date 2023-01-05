import mock
from pytest import fixture, raises

from gpt3_assistant.clients.open_ai_client import OpenAIClient
from gpt3_assistant.exceptions.text_generation_error import TextGenerationError

OPEN_AI_KEY = "fake-key"
MOCK_RESPONSES = [
    {"finish_reason": "stop", "text": "hey there"},
    {"finish_reason": "stop", "text": "what's up"},
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
        "choices": [{"finish_reason": "length", "text": "hey there"}],
        "usage": {"total_tokens": kwargs["max_tokens"]}
    }


@mock.patch("openai.Completion.create", mock_create_completion_no_responses)
def test_get_completion_throws_exception_no_responses(open_ai_client):
    max_tokens = 70

    prompt = "Yeah do you have one in mind?"

    with raises(TextGenerationError):
        open_ai_client.get_completion(prompt=prompt, max_tokens=max_tokens)


@mock.patch("openai.Completion.create", mock_create_completion_multiple_responses)
def test_get_completion_returns_first_response(open_ai_client):
    max_tokens = 70
    prompt = "Yeah do you have one in mind?"

    response = open_ai_client.get_completion(prompt=prompt, max_tokens=max_tokens)

    assert response is not None
    assert response.computer_response == MOCK_RESPONSES[0]["text"]
    assert response.user_message == prompt
    assert not response.was_cut_short


@mock.patch("openai.Completion.create", mock_create_completion_stop_due_to_length)
def test_get_completion_sets_was_cut_short_to_true(open_ai_client):
    max_tokens = 70
    prompt = "Yeah do you have one in mind?"

    response = open_ai_client.get_completion(prompt=prompt, max_tokens=max_tokens)

    assert response is not None
    assert response.computer_response == MOCK_RESPONSES[0]["text"]
    assert response.user_message == prompt
    assert response.was_cut_short
