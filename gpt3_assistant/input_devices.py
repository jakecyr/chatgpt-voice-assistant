import logging
import pyaudio
from typing import Mapping


class InputDevices:
    pyaudio = pyaudio.PyAudio()

    @staticmethod
    def get_input_device_index(input_device_name):
        """
        Get the input device to use from the user.
        :param input_device_name: the optional device name from the user to look for.
        :return: the index of the input device to use.
        """
        logging.debug(f"get_input_device_index called with: {input_device_name}")

        input_devices = InputDevices.get_list_of_input_devices()

        if len(input_devices) == 0:
            raise Exception("No input devices detected")

        chosen_input_device = None

        for input_device in input_devices:
            if input_device["name"] == input_device_name:
                chosen_input_device = input_device
                break

        if chosen_input_device is None:
            logging.debug(
                f"Input device '{input_device_name}' not found in list: {input_devices}"
            )
            raise Exception(f"Input device with name '{input_device_name}' not found")
        else:
            logging.debug(f"Found input device index: {chosen_input_device['index']}")
            return chosen_input_device["index"]

    @staticmethod
    def get_list_of_input_devices():
        """
        Get a list of the possible input devices for the current machine.
        :return: the list of input device objects for the current machine.
        """
        logging.debug("get_list_of_input_devices called")

        all_devices = []
        count_of_input_devices = InputDevices.pyaudio.get_device_count()

        for device_index in range(0, count_of_input_devices):
            all_devices.append(
                InputDevices.pyaudio.get_device_info_by_index(device_index)
            )

        # filter out non-input devices (ex. speakers)
        input_devices = list(filter(lambda x: x["maxInputChannels"] >= 1, all_devices))

        logging.info(f"Found {len(input_devices)} input devices")

        return input_devices

    @staticmethod
    def get_device_info_by_index(index) -> Mapping[str, int | str | float]:
        return InputDevices.pyaudio.get_device_info_by_index(index)
