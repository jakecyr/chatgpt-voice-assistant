from abc import ABC, abstractmethod


class Responder(ABC):
    """Abstract class for way to respond to user input"""

    @abstractmethod
    def respond(self, text_to_speak: str):
        pass
