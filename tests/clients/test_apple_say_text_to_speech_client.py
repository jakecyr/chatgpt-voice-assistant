import mimetypes
import os
import sys

import pytest

from chatgpt_voice_assistant.bases.text_to_speech_client import TextToSpeechClient
from chatgpt_voice_assistant.clients.apple_say_text_to_speech_client import (
    AppleSayTextToSpeechClient,
)

NOT_DARWIN = sys.platform != "darwin"


@pytest.mark.skipif(NOT_DARWIN, reason="Skipping on non-Mac platforms")
def test_convert_text_to_audio_creates_audio_file():
    # Test that the convert_text_to_audio method creates a valid MP3 file
    text_to_speak = "This is a test"
    audio_file_path = "test.aiff"

    client: TextToSpeechClient = AppleSayTextToSpeechClient()
    client.convert_text_to_audio(text_to_speak, audio_file_path)

    # Check that the file was created and is a valid aiff file
    assert os.path.exists(audio_file_path)
    assert mimetypes.guess_type(audio_file_path)[0] == "audio/x-aiff"

    os.remove(audio_file_path)


@pytest.mark.skipif(NOT_DARWIN, reason="Skipping on non-Mac platforms")
def test_convert_text_to_audio_raises_error_if_file_exists() -> None:
    # Test that the convert_text_to_audio method creates a valid MP3 file
    text_to_speak = "This is a test"
    audio_file_path = "test.aiff"

    client: TextToSpeechClient = AppleSayTextToSpeechClient()
    client.convert_text_to_audio(text_to_speak, audio_file_path)

    with pytest.raises(FileExistsError):
        client.convert_text_to_audio(text_to_speak, audio_file_path)

    os.remove(audio_file_path)
