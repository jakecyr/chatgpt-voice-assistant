import argparse
from typing import NamedTuple


class CommandLineArguments(NamedTuple):
    """The model object containing the values of the passed in CLI arguments"""
    log_level: str
    input_device_name: str
    lang: str
    tld: str
    open_ai_key: str
    safe_word: str


class CommandLineParser:
    @staticmethod
    def parse() -> CommandLineArguments:
        """
        Parse the command line arguments and return an object with the values.
        :return: CommandLineArguments the command line arguments tuple
        """
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--log-level",
            help="If to print at the debug level or not.",
            default="INFO",
            type=str,
        )
        parser.add_argument(
            "--input-device-name", help="Input device name", default=None, type=str
        )
        parser.add_argument("--lang", help="Language", default=None, type=str)
        parser.add_argument("--tld", help="Top level domain", default=None, type=str)
        parser.add_argument("--safe-word", help="Word to speak to exit the application", default=None, type=str)
        parser.add_argument(
            "--open-ai-key", help="Open AI Secret Key", required=True, type=str
        )

        return parser.parse_args()
