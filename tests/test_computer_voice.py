import os.path
import mock

from gpt3_assistant.computer_voice import ComputerVoice
from pytest import fixture

TEMP_FILE_NAME = "temp.mp3"
FULL_MP3_PATH = os.path.join(os.getcwd(), TEMP_FILE_NAME)


@fixture
def computer_voice():
    return ComputerVoice(mp3_filename=TEMP_FILE_NAME)


class MockGTTS:
    def save(self, filename):
        with open(filename, "w") as f:
            f.write("test")


@mock.patch("gtts.gTTS.save", new_callable=MockGTTS)
@mock.patch('subprocess.call')
def test_speak_context_manager_file_deletion(_gtts_save, _subprocess_call, computer_voice):
    with computer_voice as cv:
        cv.speak("hello there")

    assert not os.path.exists(FULL_MP3_PATH)


def test_cleanup_temporary_files(computer_voice):
    mock_gtts = MockGTTS()
    mock_gtts.save(FULL_MP3_PATH)
    assert os.path.exists(FULL_MP3_PATH)

    computer_voice.cleanup_temp_files()

    assert not os.path.exists(FULL_MP3_PATH)
