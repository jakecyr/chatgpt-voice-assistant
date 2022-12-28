from gpt3_assistant.clients.open_ai_client import OpenAIClient
from pytest import fixture, raises
import mock

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


@mock.patch("openai.Completion.create", mock_create_completion_no_responses)
def test_get_completion_throws_exception_no_responses(open_ai_client):
    max_tokens = 70

    prompt = "Yeah do you have one in mind?"

    with raises(Exception):
        open_ai_client.get_completion(prompt=prompt, max_tokens=max_tokens)


@mock.patch("openai.Completion.create", mock_create_completion_multiple_responses)
def test_get_completion_returns_first_response(open_ai_client):
    max_tokens = 70
    prompt = "Yeah do you have one in mind?"

    response = open_ai_client.get_completion(prompt=prompt, max_tokens=max_tokens)

    assert response is not None
    assert response.computer_response == MOCK_RESPONSES[0]["text"]
    assert response.user_message == prompt
