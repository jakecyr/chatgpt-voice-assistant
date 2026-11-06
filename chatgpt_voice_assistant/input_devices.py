import logging
from typing import cast

from pyaudio import PyAudio

from chatgpt_voice_assistant.models.input_device import InputDevice
from chatgpt_voice_assistant.models.pyaudio_device_info import PyAudioDeviceInfo


class InputDevices:
    """Class to interact with the current machines input devices."""

    @staticmethod
    def get_list_of_input_devices() -> list[InputDevice]:
        """Get a list of input devices on the current machine.

        Returns:
            List of input device objects on the current machine.
        """
        logging.debug("InputDevices.get_list_of_input_devices called")

        pyaudio_input_devices: list[PyAudioDeviceInfo] = (
            InputDevices._get_all_pyaudio_input_devices()
        )
        input_devices: list[InputDevice] = []

        for input_device in pyaudio_input_devices:
            device_index: int = cast(int, input_device["index"])
            device_name: str = cast(str, input_device["name"])
            input_devices.append(InputDevice(device_index, device_name))

        logging.info(f"Found {len(input_devices)} input devices.")
        return input_devices

    @staticmethod
    def _get_all_pyaudio_input_devices() -> list[PyAudioDeviceInfo]:
        """Get a list of pyaudio input devices.

        Returns:
            A list of pyaudio input device objects.
        """
        audio = PyAudio()
        try:
            all_devices = [
                cast(PyAudioDeviceInfo, audio.get_device_info_by_index(index))
                for index in range(audio.get_device_count())
            ]
            return [
                device
                for device in all_devices
                if cast(int, device["maxInputChannels"]) >= 1
            ]
        finally:
            audio.terminate()
