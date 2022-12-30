import pytest

from gpt3_assistant.models.exchange import Exchange


def test_basic_methods():
    user_message = "hi"
    computer_response = "hey there"
    was_cut_short = False

    exchange = Exchange(user_message, computer_response, was_cut_short)

    assert exchange.user_message == user_message
    assert exchange.computer_response == computer_response
    assert exchange.was_cut_short == was_cut_short


def test_cut_short_defaults_to_none():
    user_message = "hi"
    computer_response = "hey there"
    was_cut_short = None

    exchange = Exchange(user_message, computer_response)

    assert exchange.user_message == user_message
    assert exchange.computer_response == computer_response
    assert exchange.was_cut_short == was_cut_short


def test_throws_error_on_change():
    user_message = "hi"
    computer_response = "hey there"
    was_cut_short = None

    exchange = Exchange(user_message, computer_response, was_cut_short)

    with pytest.raises(AttributeError):
        exchange.user_message = "New user message"
