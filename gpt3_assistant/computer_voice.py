import os
import gtts
import subprocess

class ComputerVoice:

    def __init__(self, mp3_filename="temp.mp3", lang="en", tld="com"):
        self._mp3_filename = mp3_filename
        self._language = lang
        self._top_level_domain = tld
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup_temp_files()

    def speak(self, text_to_speak):
        tts = self.get_gTTS(text_to_speak)
        tts.save(self._mp3_filename)
        full_mp3_path = os.path.join(os.getcwd(), self._mp3_filename)
        subprocess.call(["afplay", full_mp3_path])
        os.remove(self._mp3_filename)

    def cleanup_temp_files(self):
        try:
            os.remove(self._mp3_filename)
        except:
            pass

    def get_gTTS(self, text_to_speak):
        try:
            # if both language override params exist, attempt to use else default to no keyword args
            # throws an error if language cannot be processed
            # ran into an error with if TLD not valid the entire process ends. Couldn't catch this no matter how hard I tried
            if self._language is not None and self._top_level_domain is not None:
                return gtts.gTTS(text_to_speak, lang=self._language, tld=self._top_level_domain)
            else:
                return gtts.gTTS(text_to_speak)
        except Exception as e:
            print(e)
            print("Using default language: English (United States)")
            return gtts.gTTS(text_to_speak)
