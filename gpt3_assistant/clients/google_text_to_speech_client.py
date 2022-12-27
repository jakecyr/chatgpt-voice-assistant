import logging
import gtts
from gpt3_assistant.clients.text_to_speech_client import TextToSpeechClient


class GoogleTextToSpeechClient(TextToSpeechClient):
    def __init__(self, output_language, output_top_level_domain):
        self._output_language = output_language
        self._output_top_level_domain = output_top_level_domain

    def convert_text_to_mp3(self, text_to_speak, mp3_file_path):
        tts = self._get_gtts(text_to_speak)
        tts.save(mp3_file_path)

    def _get_gtts(self, text_to_speak: str):
        logging.debug(
            f"ComputerVoice.get_gtts - Language: {self._output_language}, TLD: {self._output_top_level_domain}"
        )
        exception_thrown = True

        try:
            gtts_instance = None

            # if both language override params exist, attempt to use else default to no keyword args
            # throws an error if language cannot be processed
            if (
                    self._output_language is not None
                    and self._output_top_level_domain is not None
            ):
                logging.debug(f"Using language: {self._output_language}")
                gtts_instance = gtts.gTTS(
                    text_to_speak,
                    lang=self._output_language,
                    tld=self._output_top_level_domain,
                )
            else:
                logging.debug("Using default language")
                gtts_instance = gtts.gTTS(text_to_speak)

            exception_thrown = False
            return gtts_instance
        except AssertionError as e:
            print(
                f"Text to speak, '{text_to_speak}', can not be empty (before or after cleaning): {e}"
            )
        except ValueError as e:
            print(f"Specified lang, '{self._output_language}', is not supported: {e}")
        except RuntimeError as e:
            print(
                f"Unable to load language dictionaries for language '{self._output_language}': {e}"
            )
        except Exception as e:
            print(f"Unknown error getting gTTS: {e}")
        finally:
            if exception_thrown:
                return gtts.gTTS(text_to_speak)
