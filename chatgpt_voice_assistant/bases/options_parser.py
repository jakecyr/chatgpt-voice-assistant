from abc import ABC, abstractmethod
from typing import Any


class OptionsParser(ABC):
    """Abstract class for options parsing"""

    @abstractmethod
    def parse(self) -> Any:
        """
        Parse options and return the result.
        :return: the parsed options.
        """
