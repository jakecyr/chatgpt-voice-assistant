import mimetypes
import os

import gtts
import pytest

from gpt3_assistant.bases.text_to_speech_client import TextToSpeechClient
from gpt3_assistant.clients.google_text_to_speech_client import GoogleTextToSpeechClient


def test_convert_text_to_mp3():
    # Test that the convert_text_to_mp3 method creates a valid MP3 file
    text_to_speak = "This is a test"
    mp3_file_path = "test.mp3"
    client: TextToSpeechClient = GoogleTextToSpeechClient("en", "com")
    client.convert_text_to_mp3(text_to_speak, mp3_file_path)

    # Check that the file was created and is a valid MP3 file
    assert os.path.exists(mp3_file_path)
    assert mimetypes.guess_type(mp3_file_path)[0] == "audio/mpeg"

    os.remove(mp3_file_path)


def test_get_gtts():
    # Test that the _get_gtts method returns a gTTS instance
    text_to_speak = "This is a test"
    client = GoogleTextToSpeechClient("en", "com")
    gtts_instance = client._get_gtts(text_to_speak)
    assert isinstance(gtts_instance, gtts.gTTS)


def test_get_lang_gtts():
    # Test that the _get_lang_gtts method returns a gTTS instance with the correct language and top-level domain
    text_to_speak = "This is a test"
    client = GoogleTextToSpeechClient("en", "com")
    gtts_instance = client._get_lang_gtts(text_to_speak)
    assert gtts_instance.lang == "en"
    assert gtts_instance.tld == "com"


def test_get_gtts_default_language():
    text_to_speak = "This is a test"
    client = GoogleTextToSpeechClient(None, None)
    gtts_instance = client._get_gtts(text_to_speak)
    assert gtts_instance.lang == "en"
    assert gtts_instance.tld == "com"


def test_get_lang_gtts_empty_text():
    # Test that the _get_lang_gtts method raises an AssertionError when the text to speak is empty
    text_to_speak = ""
    client = GoogleTextToSpeechClient("en", "com")
    with pytest.raises(AssertionError):
        client._get_lang_gtts(text_to_speak)


def test_get_lang_gtts_unsupported_language():
    # Test that the _get_lang_gtts method raises a ValueError when the specified language is not supported
    text_to_speak = "This is a test"
    client = GoogleTextToSpeechClient("zz", "com")
    with pytest.raises(ValueError):
        client._get_lang_gtts(text_to_speak)


def test_get_lang_gtts_missing_dictionaries():
    # Test that the _get_lang_gtts method raises a RuntimeError when the language dictionaries are missing
    text_to_speak = "This is a test"
    client = GoogleTextToSpeechClient("xx", "com")
    with pytest.raises(ValueError):
        client._get_lang_gtts(text_to_speak)


def test_convert_text_to_mp3_file_exists():
    # Test that the convert_text_to_mp3 method raises an error if the output file already exists
    text_to_speak = "This is a test"
    mp3_file_path = "test.mp3"
    client = GoogleTextToSpeechClient("en", "com")
    client.convert_text_to_mp3(text_to_speak, mp3_file_path)

    with pytest.raises(FileExistsError):
        client.convert_text_to_mp3(text_to_speak, mp3_file_path)

    os.remove(mp3_file_path)


def test_convert_text_to_mp3_invalid_file_path():
    # Test that the convert_text_to_mp3 method raises an error if the output file path is invalid
    text_to_speak = "This is a test"
    mp3_file_path = "invalid/path/test.mp3"
    client = GoogleTextToSpeechClient("en", "com")
    with pytest.raises(FileNotFoundError):
        client.convert_text_to_mp3(text_to_speak, mp3_file_path)


def test_convert_text_to_mp3_special_characters():
    # Test that the convert_text_to_mp3 method correctly handles special characters in the input text
    text_to_speak = "This is a test with special characters: !@#$%^&*()"
    mp3_file_path = "test.mp3"
    client = GoogleTextToSpeechClient("en", "com")
    client.convert_text_to_mp3(text_to_speak, mp3_file_path)
    os.remove(mp3_file_path)


def test_convert_text_to_mp3_non_latin_scripts():
    # Test that the convert_text_to_mp3 method correctly handles non-Latin scripts in the input text
    text_to_speak = "これはテストです"  # Japanese
    mp3_file_path = "test.mp3"
    client = GoogleTextToSpeechClient("ja", "jp")
    client.convert_text_to_mp3(text_to_speak, mp3_file_path)
    os.remove(mp3_file_path)
