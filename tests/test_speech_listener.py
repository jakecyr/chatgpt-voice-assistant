from unittest.mock import MagicMock, patch

import pytest
from speech_recognition import RequestError, UnknownValueError

from chatgpt_voice_assistant.exceptions.failed_to_understand_listener_error import (
    FailedToUnderstandListenerError,
)
from chatgpt_voice_assistant.exceptions.listener_fatal_error import ListenerFatalError
from chatgpt_voice_assistant.exceptions.no_input_listener_error import (
    NoInputListenerError,
)
from chatgpt_voice_assistant.models.input_device import InputDevice
from chatgpt_voice_assistant.speech_listener import SpeechListener


@pytest.fixture
def speech_listener():
    return SpeechListener(InputDevice(0, "Computer"))


@patch("speech_recognition.Microphone")
@patch("speech_recognition.Recognizer.listen")
@patch("speech_recognition.Recognizer.recognize_google", return_value="Hey there")
def test_speech_listener_listen_returns_text(
    microphone_mock: MagicMock,
    recognizer_listen_mock: MagicMock,
    speech_listener: SpeechListener,
):
    speech_listener.listen()


def test_set_input_device_updates_the_input_device(speech_listener: SpeechListener):
    new_input_device = InputDevice(index=1, name="My Phone")
    speech_listener.set_input_device(new_input_device)
    assert speech_listener._input_device.index == new_input_device.index
    assert speech_listener._input_device.name == new_input_device.name


@patch("speech_recognition.Recognizer.recognize_google")
def test_recognize_text_in_audio_returns_text(
    recognize_google: MagicMock, speech_listener: SpeechListener
):
    expected_recognized_text = "hey there"
    recognize_google.return_value = expected_recognized_text
    text = speech_listener._recognize_text_in_audio(MagicMock())
    assert isinstance(text, str)
    assert text == expected_recognized_text


@patch("speech_recognition.Recognizer.recognize_google")
def test_recognize_text_in_audio_raises_no_input_listener_error_if_text_returned_is_none(
    recognize_google: MagicMock, speech_listener: SpeechListener
):
    recognized_text = None
    recognize_google.return_value = recognized_text

    with pytest.raises(NoInputListenerError):
        speech_listener._recognize_text_in_audio(MagicMock())


@patch("speech_recognition.Recognizer.recognize_google")
def test_recognize_text_in_audio_maps_unknown_value_to_failure_to_understand_error(
    recognize_google: MagicMock, speech_listener: SpeechListener
):
    recognize_google.side_effect = UnknownValueError()

    with pytest.raises(FailedToUnderstandListenerError):
        speech_listener._recognize_text_in_audio(MagicMock())


@patch("speech_recognition.Recognizer.recognize_google")
def test_recognize_text_in_audio_maps_request_error_to_listener_fatal_error(
    recognize_google: MagicMock, speech_listener: SpeechListener
):
    recognize_google.side_effect = RequestError()

    with pytest.raises(ListenerFatalError):
        speech_listener._recognize_text_in_audio(MagicMock())
