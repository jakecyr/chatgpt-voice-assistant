from typing import NamedTuple


class CommandLineArguments(NamedTuple):
    """The model object containing the values of the passed in CLI arguments"""

    log_level: str
    input_device_name: str
    lang: str
    tld: str
    open_ai_key: str
    safe_word: str
    max_token: int
