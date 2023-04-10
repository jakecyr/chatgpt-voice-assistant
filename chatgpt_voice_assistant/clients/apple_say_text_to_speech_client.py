import logging
import os
import subprocess

from chatgpt_voice_assistant.bases.text_to_speech_client import TextToSpeechClient


class AppleSayTextToSpeechClient(TextToSpeechClient):
    """Apple 'say' TTS CLI client that generates an AIFF file"""

    audio_extension = ".aiff"

    def convert_text_to_audio(self, text_to_speak: str, audio_file_path: str):
        if os.path.exists(audio_file_path):
            raise FileExistsError(
                f"The audio file path already exists: {audio_file_path}"
            )

        cmd = ["say", text_to_speak, "-o", audio_file_path]
        logging.debug(cmd)
        subprocess.call(cmd)
