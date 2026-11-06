from unittest.mock import MagicMock, patch

import pytest

from chatgpt_voice_assistant.clients.openai_text_to_speech_client import (
    OpenAITextToSpeechClient,
)
from chatgpt_voice_assistant.exceptions.no_input_listener_error import (
    NoInputListenerError,
)
from chatgpt_voice_assistant.models.input_device import InputDevice
from chatgpt_voice_assistant.whisper_listener import WhisperSpeechListener


def test_openai_speech_writes_audio_and_refuses_overwrite(tmp_path):
    with patch(
        "chatgpt_voice_assistant.clients.openai_text_to_speech_client.OpenAI"
    ) as client:
        client.return_value.audio.speech.create.return_value.content = b"audio"
        speaker = OpenAITextToSpeechClient("key")
        path = tmp_path / "speech.mp3"
        speaker.convert_text_to_audio("hello", path)
        assert path.read_bytes() == b"audio"
        client.return_value.audio.speech.create.assert_called_once_with(
            model="tts-1", voice="alloy", input="hello"
        )
        with pytest.raises(FileExistsError):
            speaker.convert_text_to_audio("hello", path)


def test_whisper_upload_contains_audio_and_rejects_empty():
    with patch("chatgpt_voice_assistant.whisper_listener.OpenAI") as client:
        listener = WhisperSpeechListener(InputDevice(0, "microphone"), "key")
        audio = MagicMock()
        audio.get_wav_data.return_value = b"wave data"

        def transcribe(**kwargs):
            assert kwargs["model"] == "whisper-1"
            assert kwargs["file"].read() == b"wave data"
            return MagicMock(text="hello")

        client.return_value.audio.transcriptions.create.side_effect = transcribe
        assert listener._recognize_text_in_audio(audio) == "hello"
        client.return_value.audio.transcriptions.create.side_effect = None
        client.return_value.audio.transcriptions.create.return_value.text = ""
        with pytest.raises(NoInputListenerError):
            listener._recognize_text_in_audio(audio)
