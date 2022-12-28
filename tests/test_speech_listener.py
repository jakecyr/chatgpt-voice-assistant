# from gpt3_assistant.speech_listener import SpeechListener
# from pytest import fixture
# import mock
# from exceptions.could_not_understand_speech_error import CouldNotUnderstandSpeechError
# from exceptions.speech_recognition_request_error import SpeechRecognitionRequestError
# import pytest
# import speech_recognition as sr
# from gpt3_assistant.input_devices import InputDevices
#
#
# @fixture
# def speech_listener():
#     return SpeechListener()
#
#
# def recognize_google_raise_unknown_value_error(self, audio_data, **kwargs):
#     raise sr.UnknownValueError("Error recognizing speech")
#
#
# def recognize_google_raise_request_error(self, audio_data, **kwargs):
#     raise sr.RequestError("Error making request")
#
#
# @mock.patch("speech_recognition.Recognizer.recognize_google")
# def test_recognize_text_in_audio(recognize_google, speech_listener):
#     recognized_text = "Hello there"
#     recognize_google.return_value = recognized_text
#     text = speech_listener._recognize_text_in_audio({})
#     assert type(text) == str
#     assert text == recognized_text
#
#
# @mock.patch(
#     "speech_recognition.Recognizer.recognize_google",
#     recognize_google_raise_unknown_value_error,
# )
# def test_recognize_text_in_audio_throws_could_not_understand_error(speech_listener):
#     with pytest.raises(CouldNotUnderstandSpeechError):
#         speech_listener._recognize_text_in_audio({})
#
#
# @mock.patch(
#     "speech_recognition.Recognizer.recognize_google",
#     recognize_google_raise_request_error,
# )
# def test_recognize_text_in_audio_throws_request_error(speech_listener):
#     with pytest.raises(SpeechRecognitionRequestError):
#         speech_listener._recognize_text_in_audio({})
