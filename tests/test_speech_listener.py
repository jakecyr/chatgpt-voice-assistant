from gpt3_assistant.speech_listener import SpeechListener
from pytest import fixture
import mock
from exceptions.CouldNotUnderstandSpeechError import CouldNotUnderstandSpeechError
from exceptions.SpeechRecognitionRequestError import SpeechRecognitionRequestError
import pytest
import speech_recognition as sr
import pyaudio


@fixture
def speech_listener():
    return SpeechListener()


def recognize_google_raise_unknown_value_error(self, audio_data, **kwargs):
    raise sr.UnknownValueError("Error recognizing speech")


def recognize_google_raise_request_error(self, audio_data, **kwargs):
    raise sr.RequestError("Error making request")


def test_get_list_of_input_devices(speech_listener):
    input_devices = speech_listener.get_list_of_input_devices()
    assert len(input_devices) > 0, "Expected input devices length to be > 0"
    assert pyaudio.PyAudio().get_device_count() == len(input_devices)


def test_get_device_info_from_name(speech_listener):
    for index, input_device in enumerate(speech_listener.get_list_of_input_devices()):
        target_device_name = input_device["name"]
        device_index = speech_listener._get_device_index_from_name(target_device_name)
        assert device_index is not None
        assert device_index == index


@mock.patch("speech_recognition.Recognizer.recognize_google")
def test_recognize_text_in_audio(recognize_google, speech_listener):
    recognized_text = "Hello there"
    recognize_google.return_value = recognized_text
    text = speech_listener._recognize_text_in_audio({})
    assert type(text) == str
    assert text == recognized_text


@mock.patch(
    "speech_recognition.Recognizer.recognize_google",
    recognize_google_raise_unknown_value_error,
)
def test_recognize_text_in_audio_throws_could_not_understand_error(speech_listener):
    with pytest.raises(CouldNotUnderstandSpeechError):
        speech_listener._recognize_text_in_audio({})


@mock.patch(
    "speech_recognition.Recognizer.recognize_google",
    recognize_google_raise_request_error,
)
def test_recognize_text_in_audio_throws_request_error(speech_listener):
    with pytest.raises(SpeechRecognitionRequestError):
        speech_listener._recognize_text_in_audio({})
