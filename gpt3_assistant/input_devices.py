import logging
from pyaudio import PyAudio
from gpt3_assistant.models.input_device import InputDevice
from typing import cast
from gpt3_assistant.models.pyaudio_device_info import PyAudioDeviceInfo


class InputDevices:
    """
    Class to interact with the current machines input devices.
    """

    py_audio = PyAudio()

    @staticmethod
    def get_list_of_input_devices() -> list[InputDevice]:
        """
        Get a list of the possible input devices for the current machine.
        :return: the list of input device objects for the current machine.
        """
        logging.debug("InputDevices.get_list_of_input_devices called")

        all_devices: list[PyAudioDeviceInfo] = []
        count_of_input_devices = InputDevices.py_audio.get_device_count()

        for device_index in range(0, count_of_input_devices):
            device_info: PyAudioDeviceInfo = cast(PyAudioDeviceInfo, InputDevices.py_audio.get_device_info_by_index(device_index))
            all_devices.append(device_info)

        # filter out non-input devices (ex. speakers)
        input_devices: list[InputDevice] = []

        for input_device in all_devices:
            max_input_channels = cast(int, input_device["maxInputChannels"])

            if max_input_channels >= 1:
                device_index = cast(int, input_device["index"])
                device_name = cast(str, input_device["name"])
                input_device_object = InputDevice(device_index, device_name)
                input_devices.append(input_device_object)

        logging.info(f"Found {len(input_devices)} input devices.")
        return input_devices
