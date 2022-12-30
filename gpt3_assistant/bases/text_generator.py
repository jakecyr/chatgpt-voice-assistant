from abc import ABC, abstractmethod

from gpt3_assistant.models.exchange import Exchange


class TextGenerator(ABC):
    @abstractmethod
    def generate_text(self, input_text: str) -> Exchange:
        """
        Generates text based on the input and returns it.
        :param str input_text: the input text.
        :return: the generated text.
        """
        pass
