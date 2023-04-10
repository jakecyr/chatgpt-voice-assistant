import os

from mock import MagicMock, patch

from chatgpt_voice_assistant.command_line_parser import (
    OPENAI_KEY_ENV_VAR_NAME,
    CommandLineParser,
)
from chatgpt_voice_assistant.models.command_line_arguments import CommandLineArguments

MOCK_COMMAND_LINE_ARGUMENTS: CommandLineArguments = CommandLineArguments(
    input_device_name="Airpods",
    lang="en",
    log_level="INFO",
    max_tokens=100,
    open_ai_key="fake-key",
    open_ai_model="gpt-3.5-turbo",
    safe_word="stop",
    speech_rate=1.0,
    tld="tld",
    tts="google",
    wake_word="robot",
)


MOCK_COMMAND_LINE_ARGUMENTS_NO_API_KEY: CommandLineArguments = CommandLineArguments(
    input_device_name="Airpods",
    lang="en",
    log_level="INFO",
    max_tokens=100,
    open_ai_key="",
    open_ai_model="gpt-3.5-turbo",
    safe_word="stop",
    speech_rate=1.0,
    tld="tld",
    tts="google",
    wake_word="robot",
)


@patch("argparse.ArgumentParser.parse_args")
def test_parse_returns_command_line_arguments_object(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert isinstance(args, CommandLineArguments)
    assert mock_arg_parser.call_count == 1


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=MOCK_COMMAND_LINE_ARGUMENTS,
)
def test_parse_returns_correct_instance(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert isinstance(args, CommandLineArguments)


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=MOCK_COMMAND_LINE_ARGUMENTS,
)
def test_parse_returns_correct_log_level(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert args.log_level == "INFO"


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=MOCK_COMMAND_LINE_ARGUMENTS,
)
def test_parse_returns_correct_input_device_name(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert args.input_device_name == "Airpods"


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=MOCK_COMMAND_LINE_ARGUMENTS,
)
def test_parse_returns_correct_lang(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert args.lang == "en"


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=MOCK_COMMAND_LINE_ARGUMENTS,
)
def test_parse_returns_correct_tld(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert args.tld == "tld"


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=MOCK_COMMAND_LINE_ARGUMENTS,
)
def test_parse_returns_correct_open_ai_key(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert args.open_ai_key == "fake-key"


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=MOCK_COMMAND_LINE_ARGUMENTS,
)
def test_parse_returns_correct_open_ai_model(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert args.open_ai_model == "gpt-3.5-turbo"


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=MOCK_COMMAND_LINE_ARGUMENTS,
)
def test_parse_returns_correct_safe_word(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert args.safe_word == "stop"


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=MOCK_COMMAND_LINE_ARGUMENTS,
)
def test_parse_returns_correct_max_tokens(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert args.max_tokens == 100


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=MOCK_COMMAND_LINE_ARGUMENTS,
)
def test_parse_returns_correct_speech_rate(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert args.speech_rate == 1.0


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=MOCK_COMMAND_LINE_ARGUMENTS,
)
def test_parse_returns_correct_tts(mock_arg_parser: MagicMock):
    command_line_parser = CommandLineParser()
    args: CommandLineArguments = command_line_parser.parse()
    assert args.tts == "google"


@patch(
    "sys.argv",
    ["main.py"],
)
@patch(
    "sys.exit",
)
def test_parse_exits_if_no_api_key_provided(sys_exit: MagicMock, capsys):
    command_line_parser = CommandLineParser()

    original_key = os.environ.get(OPENAI_KEY_ENV_VAR_NAME)

    if OPENAI_KEY_ENV_VAR_NAME in os.environ:
        del os.environ[OPENAI_KEY_ENV_VAR_NAME]

    command_line_parser.parse()

    if original_key is not None:
        os.environ.update({OPENAI_KEY_ENV_VAR_NAME: original_key})

    assert sys_exit.call_count == 1
    assert sys_exit.call_args.args[0] == 2
    assert (
        capsys.readouterr().err.find(
            "error: Open AI Secret Key not specified and OPENAI_API_KEY not set in environment"
        )
        != -1
    )
