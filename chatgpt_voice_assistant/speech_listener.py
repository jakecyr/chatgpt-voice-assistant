import logging

from speech_recognition import (
    AudioData,
    Microphone,
    Recognizer,
    RequestError,
    UnknownValueError,
)

from chatgpt_voice_assistant.bases.listener import Listener
from chatgpt_voice_assistant.exceptions.failed_to_understand_listener_error import (
    FailedToUnderstandListenerError,
)
from chatgpt_voice_assistant.exceptions.listener_fatal_error import ListenerFatalError
from chatgpt_voice_assistant.exceptions.no_input_listener_error import (
    NoInputListenerError,
)
from chatgpt_voice_assistant.models.input_device import InputDevice


class SpeechListener(Listener):
    """Class to listen to speech convert it to text"""

    def __init__(self, input_device: InputDevice):
        self._recognizer = Recognizer()
        self._input_device = input_device

    def listen(self) -> str:
        """
        Listen on the specified input device for speech and return the heard text.
        :return: the text from the speech listened to.
        """
        # can change device_index to something other than 0 to change the input mic
        with Microphone(device_index=self._input_device.index) as source:
            logging.info(f"Listening for input with mic '{self._input_device.name}'...")
            audio: AudioData = self._recognizer.listen(source)
            logging.debug("Received speech input.")

        return self._recognize_text_in_audio(audio)

    def _recognize_text_in_audio(self, audio: AudioData) -> str:
        try:
            text: str = self._recognizer.recognize_google(
                audio, show_all=False, with_confidence=False
            )

            if text is None or len(text) == 0:
                raise NoInputListenerError("No speech detected in audio")
            else:
                logging.info(f"Speech: {text}")

            return text
        except UnknownValueError as unknown_value:
            raise FailedToUnderstandListenerError(
                "Google Speech Recognition could not understand audio"
            ) from unknown_value
        except RequestError as e:
            raise ListenerFatalError(
                f"Could not request results from Google Speech Recognition service: {e}"
            ) from e
