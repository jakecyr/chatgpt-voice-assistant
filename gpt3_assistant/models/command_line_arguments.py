from typing import NamedTuple


class CommandLineArguments(NamedTuple):
    """
    The model object of the allowed CLI arguments.
    """
    log_level: str
    input_device_name: str
    lang: str
    tld: str
    open_ai_key: str
