import os.path
import mock
from mock import mock
from gpt3_assistant.computer_voice import ComputerVoice
from pytest import fixture

TEMP_FILE_NAME = "temp.mp3"
FULL_MP3_PATH = os.path.join(os.getcwd(), TEMP_FILE_NAME)
TEXT_TO_SPEAK = "hello there"
GTTS_ERROR_TO_THROW = AssertionError


@fixture
def computer_voice():
    return ComputerVoice(mp3_filename=TEMP_FILE_NAME)


class MockGTTS:
    _init_calls = 0
    _save_calls = 0

    def __init__(self, text_to_speech, **kwargs):
        print(f"mock_get_gtts called with: {text_to_speech}, {kwargs}")
        MockGTTS._init_calls += 1
        assert text_to_speech == TEXT_TO_SPEAK
        self.text_to_speech = text_to_speech
        self.kwargs = kwargs

    def save(self, filename):
        print(f'mock_gtts_save called with filename: "{filename}"')
        MockGTTS._save_calls += 1
        assert filename == TEMP_FILE_NAME

        with open(filename, "w") as f:
            f.write("test")


class MockGTTSThrowsError:
    _init_calls = 0
    _save_calls = 0

    def __init__(self, text_to_speech, **kwargs):
        MockGTTSThrowsError._init_calls += 1

        print(f"calls: {MockGTTSThrowsError._init_calls}")
        print(f"text to speech: {text_to_speech}")
        print(f"kwargs: {kwargs}")

        if self._init_calls == 1:
            raise GTTS_ERROR_TO_THROW("Error")
        else:
            pass

    def save(self, filename):
        print(f'mock_gtts_save called with filename: "{filename}"')
        MockGTTSThrowsError._save_calls += 1
        assert filename == TEMP_FILE_NAME


@mock.patch("subprocess.call")
def test_speak_context_manager_file_deletion(_subprocess_call, computer_voice):
    with mock.patch("gtts.gTTS", MockGTTS) as mock_gtts:
        with computer_voice as cv:
            cv.speak(TEXT_TO_SPEAK)
            assert os.path.exists(FULL_MP3_PATH)
            assert mock_gtts._init_calls == 1
            assert mock_gtts._save_calls == 1

    assert not os.path.exists(FULL_MP3_PATH)


@mock.patch("subprocess.call")
def test_speak_error_handling(_subprocess_call, computer_voice):
    with mock.patch("gtts.gTTS", MockGTTSThrowsError) as mock_gtts:
        with computer_voice as cv:
            cv.speak(TEXT_TO_SPEAK)
            assert mock_gtts._init_calls == 2
            assert mock_gtts._save_calls == 1
