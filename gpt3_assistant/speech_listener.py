import logging

import speech_recognition as sr

from gpt3_assistant.bases.listener import Listener
from gpt3_assistant.exceptions.could_not_understand_speech_error import (
    CouldNotUnderstandSpeechError,
)
from gpt3_assistant.exceptions.speech_recognition_request_error import (
    SpeechRecognitionRequestError,
)
from gpt3_assistant.models.input_device import InputDevice


class SpeechListener(Listener):
    def __init__(self, input_device: InputDevice):
        self._recognizer = sr.Recognizer()
        self._input_device = input_device

    def listen_for_speech(self):
        """
        Listen on the specified input device for speech and return the heard text.
        :keyword InputDevice input_device: the input device to listen on.
        :return: the text from the speech listened to.
        """
        # can change device_index to something other than 0 to change the input mic
        with sr.Microphone(device_index=self._input_device.index) as source:
            logging.info(f"Listening for input with mic '{self._input_device.name}'...")
            audio = self._recognizer.listen(source)
            logging.debug("Received speech input.")

        return self._recognize_text_in_audio(audio)

    def _recognize_text_in_audio(self, audio):
        try:
            return self._recognizer.recognize_google(
                audio, show_all=False, with_confidence=False
            )
        except sr.UnknownValueError:
            raise CouldNotUnderstandSpeechError(
                "Google Speech Recognition could not understand audio"
            )
        except sr.RequestError as e:
            raise SpeechRecognitionRequestError(
                f"Could not request results from Google Speech Recognition service: {e}"
            )
