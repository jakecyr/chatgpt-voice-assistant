from abc import ABC, abstractmethod


class TextToSpeechClient(ABC):
    audio_extension: str

    @abstractmethod
    def convert_text_to_audio(self, text_to_speak: str, audio_file_path: str) -> None:
        pass
