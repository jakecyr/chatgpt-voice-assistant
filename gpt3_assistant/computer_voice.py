import os
import gtts
import subprocess
import logging


class ComputerVoice:

    def __init__(self, mp3_filename="temp.mp3", lang="en", tld="com"):
        self._mp3_filename = mp3_filename
        self._language = lang
        self._top_level_domain = tld

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == FileNotFoundError:
            logging.warning(f"File not found warning whent trying to delete file: '{self._mp3_filename}'")
            return True

    def speak(self, text_to_speak: str):
        try:
            logging.debug(f"Starting to speak: '{text_to_speak}'")
            tts = self.get_gtts(text_to_speak)
            tts.save(self._mp3_filename)
            full_mp3_path = os.path.join(os.getcwd(), self._mp3_filename)
            subprocess.call(["afplay", full_mp3_path])
        finally:
            self.cleanup_temp_files()

    def cleanup_temp_files(self):
        os.remove(self._mp3_filename)

    def get_gtts(self, text_to_speak: str):
        try:
            # if both language override params exist, attempt to use else default to no keyword args
            # throws an error if language cannot be processed
            # ran into an error with if TLD not valid the entire process ends.
            # Couldn't catch this no matter how hard I tried
            if self._language is not None and self._top_level_domain is not None:
                logging.debug(f"Using language: {self._language}")
                return gtts.gTTS(text_to_speak, lang=self._language, tld=self._top_level_domain)
            else:
                logging.debug("Using default language: English (United States)")
                return gtts.gTTS(text_to_speak)
        except Exception as e:
            logging.error(e)
            return gtts.gTTS(text_to_speak)
