from gpt3_assistant.open_ai_client import OpenAIClient
from gpt3_assistant.exchange import Exchange

OPEN_AI_KEY = "fake-key"


def test_get_request_under_max_tokens_shows_all_previous():
    open_ai_client = OpenAIClient(OPEN_AI_KEY)
    max_tokens = 150

    prompt = "Do you have something in mind?"
    previous_responses = [
        Exchange("Hey", "Hey there"),
        Exchange("What's up", "Not much"),
    ]

    request = open_ai_client.get_request_under_max_tokens(max_tokens, prompt, previous_responses)
    expected_request = f"\nUser: Hey\nAssistant: Hey there\nUser: What's up\nAssistant: Not much\nUser: {prompt}\nAssistant: "

    assert request == expected_request, f"Expected different request"


def test_get_request_under_max_tokens_maxes_out():
    open_ai_client = OpenAIClient(OPEN_AI_KEY)
    max_tokens = 70

    prompt = "Yeah do you have one in mind?"
    previous_responses = [
        Exchange("Hey", "Hey there"),
        Exchange("What's up", "Not much. Wanna see a movie?"),
    ]

    request = open_ai_client.get_request_under_max_tokens(max_tokens, prompt, previous_responses)
    expected_request = f"\nUser: {prompt}\nAssistant: "

    assert request == expected_request, f"Expected different request"


def test_get_request_under_max_tokens_no_previous():
    open_ai_client = OpenAIClient(OPEN_AI_KEY)
    max_tokens = 70

    prompt = "Yeah do you have one in mind?"
    previous_responses = []

    request = open_ai_client.get_request_under_max_tokens(max_tokens, prompt, previous_responses)
    expected_request = f"\nUser: {prompt}\nAssistant: "

    assert request == expected_request, f"Expected different request"
