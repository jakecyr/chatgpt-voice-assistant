import logging
import os
import subprocess

from gpt3_assistant.bases.responder import Responder
from gpt3_assistant.bases.text_to_speech_client import TextToSpeechClient
from gpt3_assistant.exceptions.respond_error import RespondError


class ComputerVoiceResponder(Responder):
    """Responder that responds to the user with the Computer Voice"""

    def __init__(self, text_to_speech_client: TextToSpeechClient, mp3_filename: str):
        self._mp3_filename = mp3_filename
        self.text_to_speech_client: TextToSpeechClient = text_to_speech_client

    def respond(self, text_to_speak: str) -> None:
        """
        Speak the referenced text on the machine speakers.
        :param text_to_speak: the text to speak.
        :return: None
        """
        try:
            logging.debug(f"ComputerVoiceResponder.speak - '{text_to_speak}'")
            full_mp3_path = os.path.join(os.getcwd(), self._mp3_filename)
            self.text_to_speech_client.convert_text_to_mp3(text_to_speak, full_mp3_path)
            subprocess.call(["afplay", full_mp3_path])
        except Exception as e:
            raise RespondError(f"Error running computer voice response: {e}")
        finally:
            self._cleanup_temp_files()

    def _cleanup_temp_files(self):
        """
        Remove all temporary files and cleanup before shutting down.
        :return: None
        """
        logging.debug(
            f"ComputerVoiceResponder._cleanup_temp_files - {self._mp3_filename}"
        )

        # check if temporary file exists before trying to delete
        if os.path.exists(self._mp3_filename):
            os.remove(self._mp3_filename)
