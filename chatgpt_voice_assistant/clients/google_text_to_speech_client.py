import logging
import os

import gtts

from chatgpt_voice_assistant.bases.text_to_speech_client import TextToSpeechClient


class GoogleTextToSpeechClient(TextToSpeechClient):
    """Google Text to Speech API Client that converts a string to a mp3 file"""

    audio_extension = ".mp3"

    def __init__(self, output_language, output_top_level_domain):
        self._output_language = output_language
        self._output_top_level_domain = output_top_level_domain

    def convert_text_to_audio(self, text_to_speak, audio_file_path):
        if os.path.exists(audio_file_path):
            raise FileExistsError(
                f"The audio file path already exists: {audio_file_path}"
            )

        tts = self._get_gtts(text_to_speak)
        tts.save(audio_file_path)

    def _get_gtts(self, text_to_speak: str) -> gtts.gTTS:
        if (
            self._output_language is not None
            and self._output_top_level_domain is not None
        ):
            logging.debug(
                f"GTTS Using language: {self._output_language} ({self._output_top_level_domain})"
            )
            return self._get_lang_gtts(text_to_speak)

        logging.debug("GTTS Using default language")
        return gtts.gTTS(text_to_speak)

    def _get_lang_gtts(self, text_to_speak: str) -> gtts.gTTS:
        try:
            gtts_instance = gtts.gTTS(
                text_to_speak,
                lang=self._output_language,
                tld=self._output_top_level_domain,
            )

            return gtts_instance
        except AssertionError as assertion_error:
            logging.error(
                f"Text to speak, '{text_to_speak}', can not be empty (before or after cleaning)"
            )
            raise assertion_error
        except ValueError as value_error:
            logging.error(
                f"Specified lang, '{self._output_language}', is not supported"
            )
            raise value_error
        except RuntimeError as runtime_error:
            logging.error(
                f"Unable to load language dictionaries for language '{self._output_language}'"
            )
            raise runtime_error
