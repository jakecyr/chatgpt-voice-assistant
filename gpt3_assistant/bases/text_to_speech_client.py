from abc import ABC, abstractmethod


class TextToSpeechClient(ABC):
    @abstractmethod
    def convert_text_to_mp3(self, text_to_speak, mp3_file_path):
        pass
