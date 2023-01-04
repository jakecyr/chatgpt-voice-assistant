from abc import ABC, abstractmethod


class Listener(ABC):
    @abstractmethod
    def listen(self):
        """
        Listen for user input and return it.
        :return: the user input received.
        """
