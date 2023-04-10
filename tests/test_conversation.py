import pytest
from mock import MagicMock, mock

from chatgpt_voice_assistant.bases.listener import Listener
from chatgpt_voice_assistant.bases.responder import Responder
from chatgpt_voice_assistant.bases.text_generator import TextGenerator
from chatgpt_voice_assistant.conversation import Conversation
from chatgpt_voice_assistant.exceptions.failed_to_understand_listener_error import (
    FailedToUnderstandListenerError,
)
from chatgpt_voice_assistant.exceptions.listener_fatal_error import ListenerFatalError
from chatgpt_voice_assistant.models.message import Message, MessageRole

current_safe_word = "exit"
current_wake_word = "robot"


@pytest.fixture
def listener() -> MagicMock:
    return MagicMock(spec=Listener)


@pytest.fixture
def text_generator() -> MagicMock:
    return MagicMock(spec=TextGenerator)


@pytest.fixture
def responder() -> MagicMock:
    return MagicMock(spec=Responder)


@pytest.fixture
def safe_word() -> str:
    return current_safe_word


@pytest.fixture
def wake_word() -> str:
    return current_wake_word


@pytest.fixture
def conversation(
    listener, text_generator, responder, safe_word, wake_word
) -> Conversation:
    return Conversation(
        listener=listener,
        text_generator=text_generator,
        responder=responder,
        safe_word=safe_word,
    )


@pytest.fixture
def conversation_with_wake_word(
    listener, text_generator, responder, safe_word, wake_word
) -> Conversation:
    return Conversation(
        listener=listener,
        text_generator=text_generator,
        responder=responder,
        safe_word=safe_word,
        wake_word=wake_word,
    )


@mock.patch("sys.exit")
def test_start_conversation_no_safe_word(sys_exit: MagicMock, conversation: MagicMock):
    conversation._listener.listen.return_value = "my response"
    conversation._text_generator.generate_text.return_value = Message(
        "hello", MessageRole.USER, False
    )

    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen.call_count == 1
    assert conversation._text_generator.generate_text.call_count == 1
    assert conversation._responder.respond.call_count == 1
    assert sys_exit.call_count == 0


@mock.patch("sys.exit")
def test_start_conversation_could_not_understand_error(
    sys_exit: MagicMock, conversation: MagicMock
):
    conversation._text_generator.generate_text.return_value = Message(
        "hello", MessageRole.USER, False
    )

    conversation._listener.listen.side_effect = FailedToUnderstandListenerError(
        "Bad speech"
    )

    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen.call_count == 1
    assert conversation._responder.respond.call_count == 0
    assert conversation._text_generator.generate_text.call_count == 0
    assert sys_exit.call_count == 0


@mock.patch("sys.exit")
def test_start_conversation_recognition_request_error(
    sys_exit: MagicMock, conversation: MagicMock
):
    conversation._text_generator.generate_text.return_value = Message(
        "hello", MessageRole.USER, False
    )

    conversation._listener.listen.side_effect = ListenerFatalError("Bad request")

    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen.call_count == 1
    assert sys_exit.call_count == 1
    assert conversation._responder.respond.call_count == 0
    assert conversation._text_generator.generate_text.call_count == 0


@mock.patch("sys.exit")
def test_start_conversation_exits(sys_exit: MagicMock, conversation: MagicMock):
    conversation._listener.listen.return_value = current_safe_word
    conversation._text_generator.generate_text.return_value = Message(
        "hello", MessageRole.USER, False
    )
    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen.call_count == 1
    assert conversation._responder.respond.call_count == 0
    assert conversation._text_generator.generate_text.call_count == 0
    assert sys_exit.call_count == 1


@mock.patch("sys.exit")
def test_start_conversation_called_again_if_no_text(
    sys_exit: MagicMock, conversation: MagicMock
):
    conversation._text_generator.generate_text.return_value = Message(
        "hello", MessageRole.USER, False
    )

    conversation._listener.listen.side_effect = ["test", conversation._safe_word]
    conversation.start_conversation()

    assert conversation._listener.listen.call_count == 2
    assert conversation._text_generator.generate_text.call_count == 1
    assert conversation._responder.respond.call_count == 1


@mock.patch("sys.exit")
def test_start_conversation_starts_again_if_wake_word_not_spoken(
    sys_exit: MagicMock, conversation: MagicMock
):
    conversation._text_generator.generate_text.return_value = Message(
        "hello", MessageRole.USER, False
    )

    conversation._listener.listen.side_effect = ["test", conversation._safe_word]
    conversation.start_conversation()

    assert conversation._listener.listen.call_count == 2
    assert conversation._text_generator.generate_text.call_count == 1
    assert conversation._responder.respond.call_count == 1


@mock.patch("sys.exit")
def test_start_conversation_keeps_running_until_safe_word(
    sys_exit: MagicMock, conversation: MagicMock
):
    conversation._text_generator.generate_text.return_value = Message(
        "hello", MessageRole.USER, False
    )

    conversation._listener.listen.side_effect = [
        "test",
        "test2",
        "test3",
        conversation._safe_word,
    ]
    conversation.start_conversation()

    assert conversation._listener.listen.call_count == 4
    assert conversation._text_generator.generate_text.call_count == 3
    assert conversation._responder.respond.call_count == 3
