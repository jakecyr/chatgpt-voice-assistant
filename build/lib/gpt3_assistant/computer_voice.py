import os
import gtts
import subprocess


class ComputerVoice:

    def __init__(self):
        pass

    @staticmethod
    def speak(text_to_speak, mp3_filename="temp.mp3"):
        tts = gtts.gTTS(text_to_speak)
        tts.save(mp3_filename)
        full_mp3_path = os.path.join(os.getcwd(), mp3_filename)
        subprocess.call(["afplay", full_mp3_path])
        os.remove(mp3_filename)
