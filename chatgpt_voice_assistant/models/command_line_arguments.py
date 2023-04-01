from typing import NamedTuple


class CommandLineArguments(NamedTuple):
    """The model object containing the values of the passed in CLI arguments"""

    input_device_name: str
    lang: str
    log_level: str
    max_tokens: int
    open_ai_key: str
    safe_word: str
    speech_rate: float
    tld: str
    tts: str
    wake_word: str
