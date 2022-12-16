import os
import gtts
import subprocess

class ComputerVoice:

    def __init__(self, mp3_filename="temp.mp3"):
        self._mp3_filename = mp3_filename
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup_temp_files()

    def speak(self, text_to_speak):
        tts = gtts.gTTS(text_to_speak)
        tts.save(self._mp3_filename)
        full_mp3_path = os.path.join(os.getcwd(), self._mp3_filename)
        subprocess.call(["afplay", full_mp3_path])
        os.remove(self._mp3_filename)

    def cleanup_temp_files(self):
        try:
            os.remove(self._mp3_filename)
        except:
            pass
