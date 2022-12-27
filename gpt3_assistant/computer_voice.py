import os
import gtts
import subprocess
import logging


class ComputerVoice:
    def __init__(self, mp3_filename, lang=None, tld=None):
        self._mp3_filename = mp3_filename
        self._language = lang
        self._top_level_domain = tld

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cleanup_temp_files()
        except Exception as e:
            logging.error(f"Error cleaning up ComputerVoice context: {e}")

    def speak(self, text_to_speak: str):
        """
        Speak the referenced text on the machine speakers.
        :param text_to_speak: the text to speak.
        :return: None
        """
        logging.debug(f"ComputerVoice.speak - '{text_to_speak}'")
        tts = self._get_gtts(text_to_speak)
        tts.save(self._mp3_filename)
        full_mp3_path = os.path.join(os.getcwd(), self._mp3_filename)
        subprocess.call(["afplay", full_mp3_path])

    def cleanup_temp_files(self):
        """
        Remove all temporary files and cleanup before shutting down.
        :return: None
        """
        logging.debug(f"ComputerVoice.cleanup_temp_files - {self._mp3_filename}")

        # check if temporary file exists before trying to delete
        if os.path.exists(self._mp3_filename):
            os.remove(self._mp3_filename)

    def _get_gtts(self, text_to_speak: str):
        logging.debug(
            f"ComputerVoice.get_gtts - Language: {self._language}, TLD: {self._top_level_domain}"
        )
        exception_thrown = True

        try:
            gtts_instance = None

            # if both language override params exist, attempt to use else default to no keyword args
            # throws an error if language cannot be processed
            if self._language is not None and self._top_level_domain is not None:
                logging.debug(f"Using language: {self._language}")
                gtts_instance = gtts.gTTS(
                    text_to_speak, lang=self._language, tld=self._top_level_domain
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
            print(f"Specified lang, '{self._language}', is not supported: {e}")
        except RuntimeError as e:
            print(
                f"Unable to load language dictionaries for language '{self._language}': {e}"
            )
        except Exception as e:
            print(f"Unknown error getting gTTS: {e}")
        finally:
            if exception_thrown:
                return gtts.gTTS(text_to_speak)
