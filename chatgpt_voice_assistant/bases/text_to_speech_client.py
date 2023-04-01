from abc import ABC, abstractmethod


class TextToSpeechClient(ABC):
    @abstractmethod
    def convert_text_to_audio(self, text_to_speak, audio_file_path):
        pass

    def get_audio_extension(self):
        return '.mp3'