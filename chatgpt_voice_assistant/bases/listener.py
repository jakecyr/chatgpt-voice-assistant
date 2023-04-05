from abc import ABC, abstractmethod


class Listener(ABC):
    @abstractmethod
    def listen(self) -> str:
        """
        Listen for user input and return the text.
        """
