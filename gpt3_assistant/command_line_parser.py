import argparse

from gpt3_assistant.bases.options_parser import OptionsParser
from gpt3_assistant.models.command_line_arguments import CommandLineArguments


class CommandLineParser(OptionsParser):
    """Class to parse the command line arguments."""

    def parse(self) -> CommandLineArguments:
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
        parser.add_argument(
            "--max-tokens",
            help="Max tokens to use for text generation",
            default=200,
            type=int,
        )
        parser.add_argument("--tld", help="Top level domain", default=None, type=str)
        parser.add_argument(
            "--safe-word",
            help="Word to speak to exit the application",
            default=None,
            type=str,
        )
        parser.add_argument(
            "--open-ai-key", help="Open AI Secret Key", required=True, type=str
        )

        return parser.parse_args()
