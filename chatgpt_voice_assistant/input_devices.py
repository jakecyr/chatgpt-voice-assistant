import logging
from typing import List, cast

from pyaudio import PyAudio

from chatgpt_voice_assistant.models.input_device import InputDevice
from chatgpt_voice_assistant.models.pyaudio_device_info import PyAudioDeviceInfo


class InputDevices:
    """
    Class to interact with the current machines input devices.
    """

    py_audio = PyAudio()

    @staticmethod
    def get_list_of_input_devices() -> List[InputDevice]:
        """Get a list of input devices on the current machine.

        Returns:
            List of input device objects on the current machine.
        """
        logging.debug("InputDevices.get_list_of_input_devices called")

        pyaudio_input_devices: List[
            PyAudioDeviceInfo
        ] = InputDevices._get_all_pyaudio_input_devices()
        input_devices: List[InputDevice] = []

        for input_device in pyaudio_input_devices:
            device_index = cast(int, input_device["index"])
            device_name = cast(str, input_device["name"])
            input_devices.append(InputDevice(device_index, device_name))

        logging.info(f"Found {len(input_devices)} input devices.")
        return input_devices

    @staticmethod
    def _get_all_pyaudio_input_devices() -> List[PyAudioDeviceInfo]:
        """Get a list of pyaudio input devices.

        Returns:
            A list of pyaudio input device objects.
        """
        all_devices: List[PyAudioDeviceInfo] = []
        count_of_input_devices = InputDevices.py_audio.get_device_count()

        for device_index in range(0, count_of_input_devices):
            device_info: PyAudioDeviceInfo = cast(
                PyAudioDeviceInfo,
                InputDevices.py_audio.get_device_info_by_index(device_index),
            )
            all_devices.append(device_info)

        return list(
            filter(lambda x: cast(int, x["maxInputChannels"]) >= 1, all_devices)
        )
