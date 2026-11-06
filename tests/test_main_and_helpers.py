from unittest.mock import MagicMock, patch

import pytest

from chatgpt_voice_assistant.exceptions.invalid_input_device_index_error import (
    InvalidInputDeviceIndexError,
)
from chatgpt_voice_assistant.exceptions.no_input_devices_found_error import (
    NoInputDevicesFoundError,
)
from chatgpt_voice_assistant.helpers.get_input_device_from_user import (
    get_input_device_from_user,
)
from chatgpt_voice_assistant.helpers.set_log_level import set_log_level
from chatgpt_voice_assistant.models.input_device import InputDevice


def test_device_selection():
    device = InputDevice(0, "mic")
    assert get_input_device_from_user([device], "mic") == device
    with patch("builtins.input", return_value="1"):
        assert get_input_device_from_user([device], "missing") == device
    with (
        patch("builtins.input", return_value="0"),
        pytest.raises(InvalidInputDeviceIndexError),
    ):
        get_input_device_from_user([device], None)
    with pytest.raises(NoInputDevicesFoundError):
        get_input_device_from_user([], None)


def test_logging_level():
    set_log_level(None)
    with pytest.raises(ValueError):
        set_log_level("not-a-level")


@pytest.mark.parametrize("tts", ["openai", "google", "apple"])
def test_main_connects_options(tts):
    from chatgpt_voice_assistant import main

    options = MagicMock(
        open_ai_key="key",
        open_ai_model="gpt-6.1-terra",
        max_tokens=444,
        reasoning_effort="low",
        tts=tts,
    )
    with patch.multiple(
        main,
        CommandLineParser=MagicMock(),
        InputDevices=MagicMock(),
        get_input_device_from_user=MagicMock(),
        WhisperSpeechListener=MagicMock(),
        OpenAITextGenerator=MagicMock(),
        OpenAITextToSpeechClient=MagicMock(),
        GoogleTextToSpeechClient=MagicMock(),
        AppleSayTextToSpeechClient=MagicMock(),
        ComputerVoiceResponder=MagicMock(),
        Conversation=MagicMock(),
        set_keyboard_interrupt_handler=MagicMock(),
        set_log_level=MagicMock(),
    ):
        main.CommandLineParser.return_value.parse.return_value = options
        main.main()
        main.OpenAITextGenerator.assert_called_once_with(
            open_ai_key="key",
            model="gpt-6.1-terra",
            max_tokens=444,
            reasoning_effort="low",
        )
        main.Conversation.return_value.start_conversation.assert_called_once_with()
