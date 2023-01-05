import pytest
from mock import MagicMock, mock

from gpt3_assistant.bases.listener import Listener
from gpt3_assistant.bases.responder import Responder
from gpt3_assistant.bases.text_generator import TextGenerator
from gpt3_assistant.conversation import Conversation
from gpt3_assistant.exceptions.failed_to_understand_listener_error import (
    FailedToUnderstandListenerError,
)
from gpt3_assistant.exceptions.listener_fatal_error import ListenerFatalError
from gpt3_assistant.models.exchange import Exchange

current_safe_word = "exit"


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
def conversation(listener, text_generator, responder, safe_word) -> Conversation:
    return Conversation(
        listener=listener,
        text_generator=text_generator,
        responder=responder,
        safe_word=safe_word,
    )


@mock.patch("sys.exit")
def test_start_conversation_no_safe_word(sys_exit: MagicMock, conversation: Conversation):
    conversation._listener.listen.return_value = "my response"
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello", "hey there", False
    )

    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen.call_count == 1
    assert conversation._text_generator.generate_text.call_count == 1
    assert conversation._responder.respond.call_count == 1
    assert sys_exit.call_count == 0


@mock.patch("sys.exit")
def test_start_conversation_could_not_understand_error(sys_exit: MagicMock, conversation: Conversation):
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello", "hey there", False
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
def test_start_conversation_recognition_request_error(sys_exit: MagicMock, conversation: Conversation):
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello", "hey there", False
    )

    conversation._listener.listen.side_effect = ListenerFatalError("Bad request")

    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen.call_count == 1
    assert sys_exit.call_count == 1
    assert conversation._responder.respond.call_count == 0
    assert conversation._text_generator.generate_text.call_count == 0


@mock.patch("sys.exit")
def test_start_conversation_exits(sys_exit: MagicMock, conversation: Conversation):
    conversation._listener.listen.return_value = current_safe_word
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello", "hey there", False
    )
    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen.call_count == 1
    assert conversation._responder.respond.call_count == 0
    assert conversation._text_generator.generate_text.call_count == 0
    assert sys_exit.call_count == 1


@mock.patch("sys.exit")
def test_start_conversation_called_again_if_no_text(sys_exit: MagicMock, conversation: Conversation):
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello", "hey there", False
    )

    conversation._listener.listen.side_effect = ["test", conversation._safe_word]
    conversation.start_conversation()

    assert conversation._listener.listen.call_count == 2
    assert conversation._text_generator.generate_text.call_count == 1
    assert conversation._responder.respond.call_count == 1


@mock.patch("sys.exit")
def test_start_conversation_keeps_running_until_safe_word(sys_exit: MagicMock, conversation: Conversation):
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello", "hey there", False
    )

    conversation._listener.listen.side_effect = [
        "test",
        "test2",
        "test3",
        conversation._safe_word,
    ]
    print(conversation._safe_word)
    conversation.start_conversation()

    assert conversation._listener.listen.call_count == 4
    assert conversation._text_generator.generate_text.call_count == 3
    assert conversation._responder.respond.call_count == 3
