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


def test_get_list_of_input_devices(speech_listener):
    input_devices = speech_listener._get_list_of_input_devices()
    assert len(input_devices) > 0, "Expected input devices length to be > 0"
    assert pyaudio.PyAudio().get_device_count() == len(input_devices)


def test_recognize_text_in_audio(speech_listener):
    recognized_text = "Hello there"

    def mock_recognize_google(self, audio, **kwargs):
        return recognized_text

    with mock.patch("speech_recognition.Recognizer.recognize_google", mock_recognize_google):
        text = speech_listener._recognize_text_in_audio({})
        assert type(text) == str
        assert text == recognized_text


def test_recognize_text_in_audio_throws_could_not_understand_error(speech_listener):
    def mock_recognize_google(self, audio, **kwargs):
        raise sr.UnknownValueError("Error recognizing speech")

    with mock.patch("speech_recognition.Recognizer.recognize_google", mock_recognize_google):
        with pytest.raises(CouldNotUnderstandSpeechError):
            speech_listener._recognize_text_in_audio({})


def test_recognize_text_in_audio_throws_request_error(speech_listener):
    def mock_recognize_google(self, audio, **kwargs):
        raise sr.RequestError("Error recognizing speech")

    with mock.patch("speech_recognition.Recognizer.recognize_google", mock_recognize_google):
        with pytest.raises(SpeechRecognitionRequestError):
            speech_listener._recognize_text_in_audio({})
