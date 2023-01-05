from dataclasses import dataclass

@dataclass(frozen=True)
class InputDevice:
    """
    Data model for an input device option
    """

    index: int
    name: str
