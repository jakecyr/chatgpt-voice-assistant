import speech_recognition as sr
from gpt3_assistant.exceptions.CouldNotUnderstandSpeechError import CouldNotUnderstandSpeechError
from gpt3_assistant.exceptions.SpeechRecognitionRequestError import SpeechRecognitionRequestError
from gpt3_assistant.input_devices import InputDevices
import logging


class SpeechListener:
    def __init__(self):
        self._recognizer = sr.Recognizer()

    def listen_for_speech(self, **kwargs):
        """
        Listen on the specified input device for speech and return the heard text.
        :keyword str device_index: the index of the input device to use (from get_list_of_input_devices method)
        :return: the text from the speech listened to.
        """
        device_index = 0

        if "device_index" in kwargs:
            device_index = kwargs["device_index"]

        input_device = InputDevices.get_device_info_by_index(device_index)
        input_device_name = input_device["name"]

        # can change device_index to something other than 0 to change the input mic
        with sr.Microphone(device_index=device_index) as source:
            logging.info(f"Listening for input with mic '{input_device_name}'...")
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
