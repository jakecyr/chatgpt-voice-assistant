import logging
import pyaudio

from gpt3_assistant.models.input_device import InputDevice


class InputDevices:
    """
    Class to interact with the current machines input devices.
    """

    pyaudio = pyaudio.PyAudio()

    @staticmethod
    def get_list_of_input_devices() -> list[InputDevice]:
        """
        Get a list of the possible input devices for the current machine.
        :return: the list of input device objects for the current machine.
        """
        logging.debug("InputDevices.get_list_of_input_devices called")

        all_devices = []
        count_of_input_devices = InputDevices.pyaudio.get_device_count()

        for device_index in range(0, count_of_input_devices):
            all_devices.append(
                InputDevices.pyaudio.get_device_info_by_index(device_index)
            )

        # filter out non-input devices (ex. speakers)
        input_devices: list[InputDevice] = []

        for input_device in all_devices:
            if input_device["maxInputChannels"] >= 1:
                input_devices.append(
                    InputDevice(input_device["index"], input_device["name"])
                )

        logging.info(f"Found {len(input_devices)} input devices.")
        return input_devices
