import os.path
from mock import mock
from gpt3_assistant.computer_voice_responder import ComputerVoiceResponder
from pytest import fixture
from gpt3_assistant.clients.text_to_speech_client import TextToSpeechClient

TEMP_FILE_NAME = "temp.mp3"
FULL_MP3_PATH = os.path.join(os.getcwd(), TEMP_FILE_NAME)
TEXT_TO_SPEAK = "hello there"
GTTS_ERROR_TO_THROW = AssertionError


class mock_subprocess_call():
    _calls = 0
    _last_inputs = None

    def __init__(self, inputs: list[str]):
        mock_subprocess_call._calls += 1
        mock_subprocess_call._last_inputs = inputs

    @staticmethod
    def reset():
        mock_subprocess_call._calls = 0
        mock_subprocess_call._last_inputs = None


class MockGoogleTextToSpeechClient(TextToSpeechClient):
    _exception = None

    def convert_text_to_mp3(self, text_to_speak, mp3_file_path):
        if MockGoogleTextToSpeechClient._exception is not None:
            raise MockGoogleTextToSpeechClient._exception

        pass


class mock_print:
    _calls: int = 0
    _last_printed: str = None

    def __init__(self, text: str):
        mock_print._calls += 1
        mock_print._last_printed = text

    @staticmethod
    def reset():
        mock_print._calls = 0
        mock_print._last_printed = None


@fixture
def computer_voice():
    mock_text_to_speech_client = MockGoogleTextToSpeechClient()

    return ComputerVoiceResponder(
        text_to_speech_client=mock_text_to_speech_client,
        mp3_filename=TEMP_FILE_NAME
    )


@mock.patch(
    'gpt3_assistant.clients.google_text_to_speech_client.GoogleTextToSpeechClient',
    MockGoogleTextToSpeechClient
)
@mock.patch('builtins.print', mock_print)
@mock.patch("subprocess.call", mock_subprocess_call)
def test_respond_succeeds(computer_voice):
    computer_voice.respond(TEXT_TO_SPEAK)
    assert mock_print._last_printed is None or not mock_print._last_printed.startswith("Exception")
    assert mock_subprocess_call._calls == 1
    mock_print.reset()
    mock_subprocess_call.reset()


@mock.patch(
    'gpt3_assistant.clients.google_text_to_speech_client.GoogleTextToSpeechClient',
    MockGoogleTextToSpeechClient
)
@mock.patch('builtins.print', mock_print)
@mock.patch("subprocess.call", mock_subprocess_call)
def test_respond_throws_error(computer_voice):
    MockGoogleTextToSpeechClient._exception = Exception("Bad news")
    computer_voice.respond(TEXT_TO_SPEAK)
    assert mock_print._calls == 1
    assert mock_print._last_printed is not None
    assert mock_print._last_printed.startswith("Exception caught")
    assert mock_subprocess_call._calls == 0
    mock_print.reset()
    mock_subprocess_call.reset()
