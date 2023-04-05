from abc import ABC, abstractmethod

from chatgpt_voice_assistant.models.message import Message


class TextGenerator(ABC):
    @abstractmethod
    def generate_text(self, prompt: str) -> Message:
        """
        Generates text based on the input and returns it.

        Args:
            prompt: the input text.

        Returns:
            The generated message.
        """
