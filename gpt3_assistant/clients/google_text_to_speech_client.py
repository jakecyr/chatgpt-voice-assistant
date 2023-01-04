import logging
import os

import gtts

from gpt3_assistant.bases.text_to_speech_client import TextToSpeechClient


class GoogleTextToSpeechClient(TextToSpeechClient):
    """Google Text to Speech Client that converts a string to a mp3 file"""

    def __init__(self, output_language, output_top_level_domain):
        self._output_language = output_language
        self._output_top_level_domain = output_top_level_domain

    def convert_text_to_mp3(self, text_to_speak, mp3_file_path):
        if os.path.exists(mp3_file_path):
            raise FileExistsError(f"The MP3 file path already exists: {mp3_file_path}")

        tts = self._get_gtts(text_to_speak)
        tts.save(mp3_file_path)

    def _get_gtts(self, text_to_speak: str) -> gtts.gTTS:
        if (
            self._output_language is not None
            and self._output_top_level_domain is not None
        ):
            logging.debug(
                f"Using language: {self._output_language} ({self._output_top_level_domain})"
            )
            return self._get_lang_gtts(text_to_speak)
        else:
            logging.debug("Using default language")
            return gtts.gTTS(text_to_speak)

    def _get_lang_gtts(self, text_to_speak: str) -> gtts.gTTS:
        try:
            gtts_instance = gtts.gTTS(
                text_to_speak,
                lang=self._output_language,
                tld=self._output_top_level_domain,
            )

            return gtts_instance
        except AssertionError as e:
            logging.error(
                f"Text to speak, '{text_to_speak}', can not be empty (before or after cleaning): {e}"
            )
            raise e
        except ValueError as e:
            logging.error(
                f"Specified lang, '{self._output_language}', is not supported: {e}"
            )
            raise e
        except RuntimeError as e:
            logging.error(
                f"Unable to load language dictionaries for language '{self._output_language}': {e}"
            )
            raise e
