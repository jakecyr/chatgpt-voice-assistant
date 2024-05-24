from __future__ import annotations
import os
from pathlib import Path
from typing import Literal
from openai._legacy_response import HttpxBinaryResponseContent

from chatgpt_voice_assistant.bases.text_to_speech_client import TextToSpeechClient
from openai import OpenAI

VoiceOptions = Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


class OpenAITextToSpeechClient(TextToSpeechClient):
    """Google Text to Speech API Client that converts a string to a mp3 file"""

    audio_extension = ".mp3"

    def __init__(
        self,
        api_key: str,
        voice: VoiceOptions = "alloy",
    ) -> None:
        self._client = OpenAI(api_key=api_key)
        self._voice: VoiceOptions = voice

    def convert_text_to_audio(
        self, text_to_speak: str, audio_file_path: str | Path
    ) -> None:
        if os.path.exists(audio_file_path):
            raise FileExistsError(
                f"The audio file path already exists: {audio_file_path}"
            )

        response: HttpxBinaryResponseContent = self._client.audio.speech.create(
            model="tts-1",
            voice=self._voice,
            input=text_to_speak,
        )

        # Save to audio file.
        with open(audio_file_path, "wb") as f:
            f.write(response.content)
