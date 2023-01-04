import logging

from gpt3_assistant.models.input_device import InputDevice


def ask_user_which_input_device_to_use(input_devices: list[InputDevice]) -> InputDevice:
    for index, input_device in enumerate(input_devices):
        logging.info(f"{index + 1}) {input_device.name}")

    chosen_device_index = int(input("Which input device would you like to use? ")) - 1

    if chosen_device_index < 0 or chosen_device_index > len(input_devices) - 1:
        raise Exception("Invalid input device index chosen")

    return input_devices[chosen_device_index]


def get_input_device_from_user(
    input_devices: list[InputDevice], input_device_name: str
) -> InputDevice:
    if len(input_devices) == 0:
        raise Exception("No input devices found")

    input_device = None

    if input_device_name is None:
        input_device = ask_user_which_input_device_to_use(input_devices)
    else:
        input_device = input_devices[0]

    return input_device
