import argparse
import os

from chatgpt_voice_assistant.bases.options_parser import OptionsParser
from chatgpt_voice_assistant.models.command_line_arguments import CommandLineArguments

OPENAI_KEY_ENV_VAR_NAME = "OPENAI_API_KEY"


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
            help="Whether to print at the debug level or not.",
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
            "--wake-word",
            help="Word to trigger a response",
            default=None,
            type=str,
        )
        parser.add_argument(
            "--open-ai-key",
            help=f"Required. Open AI Secret Key (or set {OPENAI_KEY_ENV_VAR_NAME} environment variable)",
            default=os.environ.get(OPENAI_KEY_ENV_VAR_NAME),
            type=str,
        )
        parser.add_argument(
            "--open-ai-model",
            help="The Open AI model to use. See: https://platform.openai.com/docs/models/overview",
            default="gpt-3.5-turbo",
            type=str,
        )
        parser.add_argument(
            "--tts",
            choices=["apple", "google"],
            default="google",
            help="Choose a text-to-speech engine ('apple' (say) or 'google' (gtts), defaults to 'google')",
        )
        parser.add_argument(
            "--speech-rate",
            help="The rate at which to play speech. 1.0=normal",
            default=1.0,
            type=float,
        )

        parsed_args = parser.parse_args()

        if parsed_args.open_ai_key is None:
            parser.error(
                "Open AI Secret Key not specified and OPENAI_API_KEY not set in environment"
            )

        return CommandLineArguments(
            input_device_name=parsed_args.input_device_name,
            lang=parsed_args.lang,
            log_level=parsed_args.log_level,
            max_tokens=parsed_args.max_tokens,
            open_ai_key=parsed_args.open_ai_key,
            open_ai_model=parsed_args.open_ai_model,
            safe_word=parsed_args.safe_word,
            speech_rate=parsed_args.speech_rate,
            tld=parsed_args.tld,
            tts=parsed_args.tts,
            wake_word=parsed_args.wake_word,
        )
