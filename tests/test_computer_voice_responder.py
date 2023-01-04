import os.path

import pytest
from mock import MagicMock, mock
from pytest import fixture

from gpt3_assistant.computer_voice_responder import ComputerVoiceResponder
from gpt3_assistant.exceptions.respond_error import RespondError

TEMP_FILE_NAME = "temp.mp3"
FULL_MP3_PATH = os.path.join(os.getcwd(), TEMP_FILE_NAME)
TEXT_TO_SPEAK = "hello there"
GTTS_ERROR_TO_THROW = AssertionError


@fixture
def computer_voice():
    return ComputerVoiceResponder(
        text_to_speech_client=MagicMock(), mp3_filename=TEMP_FILE_NAME
    )


@mock.patch("subprocess.call")
def test_respond_succeeds(mock_subprocess, computer_voice):
    computer_voice._cleanup_temp_files = MagicMock()
    computer_voice.respond(TEXT_TO_SPEAK)
    computer_voice.text_to_speech_client.convert_text_to_mp3.assert_called_once()
    mock_subprocess.assert_called_once()
    computer_voice._cleanup_temp_files.assert_called_once()


@mock.patch("subprocess.call")
def test_respond_throws_error(mock_subprocess, computer_voice):
    with pytest.raises(RespondError):
        computer_voice._cleanup_temp_files
        computer_voice.text_to_speech_client.convert_text_to_mp3.side_effect = (
            Exception("Bad bad")
        )
        computer_voice.respond(TEXT_TO_SPEAK)
        mock_subprocess.assert_not_called()
        computer_voice._cleanup_temp_files.assert_called_once()
