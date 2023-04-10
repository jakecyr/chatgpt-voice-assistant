import pytest

from chatgpt_voice_assistant.models.message import Message, MessageRole


def test_message_sets_correct_content_value():
    content = "hi"
    role = MessageRole.ASSISTANT

    exchange = Message(content, role)

    assert exchange.content == content


def test_message_sets_role_to_assistant():
    content = "hi"
    role = MessageRole.ASSISTANT

    exchange = Message(content, role)

    assert exchange.role == role
    assert isinstance(exchange.role, MessageRole)


def test_message_sets_role_to_user():
    content = "hi"
    role = MessageRole.USER

    exchange = Message(content, role)

    assert exchange.role == role
    assert isinstance(exchange.role, MessageRole)


def test_message_sets_was_cut_short():
    content = "hi"
    role = MessageRole.USER
    was_cut_short = True

    exchange = Message(content, role, was_cut_short)

    assert exchange.was_cut_short == was_cut_short


def test_message_cut_short_defaults_to_none():
    content = "hi"
    role = MessageRole.ASSISTANT

    exchange = Message(content, role)

    assert exchange.was_cut_short is None


def test_message_throws_error_on_change():
    content = "hi"
    role = MessageRole.ASSISTANT
    was_cut_short = None

    exchange = Message(content, role, was_cut_short)

    with pytest.raises(AttributeError):
        exchange.content = "New user message"  # type: ignore
