import pyaudio
import speech_recognition as sr
from exceptions.CouldNotUnderstandSpeechError import CouldNotUnderstandSpeechError
from exceptions.SpeechRecognitionRequestError import SpeechRecognitionRequestError
import logging


class SpeechListener:
    def __init__(self):
        self._py_audio = pyaudio.PyAudio()
        self._recognizer = sr.Recognizer()

    def listen_for_speech(self, **kwargs):
        """
        Listen on the specified input device for speech and return the heard text.
        :keyword str device_index: the index of the input device to use (from get_list_of_input_devices method)
        :keyword str device_name: the name of the input device to use (from get_list_of_input_devices method)
        :return: the text from the speech listened to.
        """
        device_index = 0

        if "device_index" in kwargs:
            device_index = kwargs["device_index"]
        elif "device_name" in kwargs and kwargs['device_name'] is not None:
            device_index = self._get_device_index_from_name(kwargs["device_name"])

        input_device_name = self._py_audio.get_device_info_by_index(device_index)[
            "name"
        ]

        # can change device_index to something other than 0 to change the input mic
        with sr.Microphone(device_index=device_index) as source:
            logging.info(f"Listening for input with mic '{input_device_name}'...")
            audio = self._recognizer.listen(source)
            logging.debug("Received speech input.")

        return self._recognize_text_in_audio(audio)

    def get_list_of_input_devices(self):
        input_devices = []
        count_of_input_devices = self._py_audio.get_device_count()

        for device_index in range(0, count_of_input_devices):
            input_devices.append(self._py_audio.get_device_info_by_index(device_index))

        return input_devices

    def _get_device_index_from_name(self, name_to_find):
        logging.debug(f"Looking for input device {name_to_find}")
        count_of_input_devices = self._py_audio.get_device_count()

        for device_index in range(0, count_of_input_devices):
            device_info = self._py_audio.get_device_info_by_index(device_index)
            logging.debug(f"Checking for input device match {device_info['name']}")
            if device_info["name"] == name_to_find:
                return device_index

        raise Exception(f"Input device with name '{name_to_find}' not found")

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
