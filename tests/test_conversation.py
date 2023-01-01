import pytest
from mock import MagicMock, mock

from gpt3_assistant.bases.listener import Listener
from gpt3_assistant.bases.responder import Responder
from gpt3_assistant.bases.text_generator import TextGenerator
from gpt3_assistant.conversation import Conversation
from gpt3_assistant.models.exchange import Exchange
from gpt3_assistant.exceptions.could_not_understand_speech_error import (
    CouldNotUnderstandSpeechError,
)
from gpt3_assistant.exceptions.speech_recognition_request_error import (
    SpeechRecognitionRequestError,
)

current_safe_word = "exit"


@pytest.fixture
def listener():
    return MagicMock(spec=Listener)


@pytest.fixture
def text_generator():
    return MagicMock(spec=TextGenerator)


@pytest.fixture
def responder():
    return MagicMock(spec=Responder)


@pytest.fixture
def safe_word():
    return current_safe_word


@pytest.fixture
def conversation(listener, text_generator, responder, safe_word):
    return Conversation(
        listener=listener,
        text_generator=text_generator,
        responder=responder,
        safe_word=safe_word
    )


@mock.patch('sys.exit')
def test_start_conversation_no_safe_word(sys_exit, conversation):
    conversation._listener.listen_for_speech.return_value = "my response"
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello",
        "hey there",
        False
    )

    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen_for_speech.call_count == 1
    assert conversation._text_generator.generate_text.call_count == 1
    assert conversation._responder.respond.call_count == 1
    assert sys_exit.call_count == 0


@mock.patch('sys.exit')
def test_start_conversation_could_not_understand_error(sys_exit, conversation):
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello",
        "hey there",
        False
    )

    conversation._listener.listen_for_speech.side_effect = CouldNotUnderstandSpeechError("Bad speech")

    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen_for_speech.call_count == 1
    assert conversation._responder.respond.call_count == 0
    assert conversation._text_generator.generate_text.call_count == 0
    assert sys_exit.call_count == 0


@mock.patch('sys.exit')
def test_start_conversation_recognition_request_error(sys_exit, conversation):
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello",
        "hey there",
        False
    )

    conversation._listener.listen_for_speech.side_effect = SpeechRecognitionRequestError("Bad request")

    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen_for_speech.call_count == 1
    assert sys_exit.call_count == 1
    assert conversation._responder.respond.call_count == 0
    assert conversation._text_generator.generate_text.call_count == 0


@mock.patch('sys.exit')
def test_start_conversation_exits(sys_exit, conversation):
    conversation._listener.listen_for_speech.return_value = current_safe_word
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello",
        "hey there",
        False
    )
    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen_for_speech.call_count == 1
    assert conversation._responder.respond.call_count == 0
    assert conversation._text_generator.generate_text.call_count == 0
    assert sys_exit.call_count == 1


@mock.patch('sys.exit')
def test_start_conversation_response_cut_short(sys_exit, conversation):
    conversation._listener.listen_for_speech.return_value = "my response"
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello",
        "hey there",
        True
    )

    conversation.start_conversation(run_once=True)

    assert conversation._listener.listen_for_speech.call_count == 1
    assert conversation._text_generator.generate_text.call_count == 1
    assert conversation._responder.respond.call_count == 2
    assert sys_exit.call_count == 0


@mock.patch('sys.exit')
def test_start_conversation_called_again_if_no_text(sys_exit, conversation):
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello",
        "hey there",
        False
    )

    conversation._listener.listen_for_speech.side_effect = [None, "test", current_safe_word]
    conversation.start_conversation()

    assert conversation._listener.listen_for_speech.call_count == 3
    assert conversation._text_generator.generate_text.call_count == 1
    assert conversation._responder.respond.call_count == 1



@mock.patch('sys.exit')
def test_start_conversation_keeps_running_until_safe_word(sys_exit, conversation):
    conversation._text_generator.generate_text.return_value = Exchange(
        "hello",
        "hey there",
        False
    )

    conversation._listener.listen_for_speech.side_effect = [None, "test", "test2", "test3", current_safe_word]
    conversation.start_conversation()

    assert conversation._listener.listen_for_speech.call_count == 5
    assert conversation._text_generator.generate_text.call_count == 3
    assert conversation._responder.respond.call_count == 3
