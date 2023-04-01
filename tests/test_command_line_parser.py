import pytest
from mock import MagicMock, mock, patch

from chatgpt_voice_assistant.command_line_parser import CommandLineParser
from chatgpt_voice_assistant.models.command_line_arguments import CommandLineArguments


@patch("argparse.ArgumentParser.parse_args")
def test_parse_returns_command_line_arguments_object(mock_arg_parser):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert isinstance(args, CommandLineArguments)
    assert mock_arg_parser.call_count == 1


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=CommandLineArguments(
        log_level="INFO",
        input_device_name="Airpods",
        lang="en",
        tld="tld",
        open_ai_key="fake-key",
        safe_word="stop",
        wake_word="robot",
        max_tokens=100,
        speech_rate=1.0,
        tts="google",
    ),
)
def test_parse_returns_correct_values(mock_arg_parser):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert isinstance(args, CommandLineArguments)

    assert args.log_level == "INFO"
    assert args.input_device_name == "Airpods"
    assert args.lang == "en"
    assert args.tld == "tld"
    assert args.open_ai_key == "fake-key"
    assert args.safe_word == "stop"
    assert args.max_tokens == 100
    assert isinstance(args.max_tokens, int)
    assert mock_arg_parser.call_count == 1
