from abc import ABC, abstractmethod


class OptionsParser(ABC):
    """Abstract class for options parsing"""

    @abstractmethod
    def parse(self):
        """
        Parse options and return the result.
        :return: the parsed options.
        """
