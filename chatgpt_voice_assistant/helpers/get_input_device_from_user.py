import logging

from chatgpt_voice_assistant.exceptions.invalid_input_device_index_error import (
    InvalidInputDeviceIndexError,
)
from chatgpt_voice_assistant.exceptions.no_input_devices_found_error import (
    NoInputDevicesFoundError,
)
from chatgpt_voice_assistant.models.input_device import InputDevice


def ask_user_which_input_device_to_use(input_devices: list[InputDevice]) -> InputDevice:
    for index, input_device in enumerate(input_devices):
        logging.info(f"{index + 1}) {input_device.name}")

    chosen_device_index = int(input("Which input device would you like to use? ")) - 1

    if chosen_device_index < 0 or chosen_device_index > len(input_devices) - 1:
        raise InvalidInputDeviceIndexError("Invalid input device index chosen")

    return input_devices[chosen_device_index]


def get_input_device_from_user(
    input_devices: list[InputDevice], input_device_name: str
) -> InputDevice:
    if len(input_devices) == 0:
        raise NoInputDevicesFoundError("No input devices found")

    input_device = None

    if input_device_name is not None:
        if matches := [
            device for device in input_devices if device.name == input_device_name
        ]:
            return matches[0]
        else:
            logging.info(f'No input device named "{input_device_name}"')

    input_device = ask_user_which_input_device_to_use(input_devices)

    return input_device
