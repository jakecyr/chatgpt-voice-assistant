import logging
import pyaudio


class InputDevice:
    pyaudio = pyaudio.PyAudio()

    @staticmethod
    def get_input_device_index(input_device_name=None):
        """
        Get the input device to use from the user.
        :param input_device_name: the optional device name from the user to look for.
        :return: the index of the input device to use.
        """

        input_devices = list(filter(lambda x: x['maxInputChannels'] >= 1,
                                    InputDevice.get_list_of_input_devices()))

        if input_device_name is not None:
            chosen_input_device = None
            for input_device in input_devices:
                if input_device['name'] == input_device_name:
                    chosen_input_device = input_device
                    break

            if chosen_input_device is None:
                raise Exception(f"Input device with name '{input_device_name} not found")
            else:
                return chosen_input_device['index']
        else:
            for index, input_device in enumerate(input_devices):
                print(f"{index + 1}) {input_device['name']}")

            chosen_device_index = int(input("Which input device would you like to use? ")) - 1

            if chosen_device_index < 0 or chosen_device_index > len(input_devices) - 1:
                raise Exception("Invalid input device index chosen")

            chosen_device = input_devices[chosen_device_index]

            return chosen_device['index']

    @staticmethod
    def get_list_of_input_devices():
        """
        Get a list of the possible input devices for the current machine.
        :return: the list of input device objects for the current machine.
        """
        input_devices = []
        count_of_input_devices = InputDevice.pyaudio.get_device_count()

        for device_index in range(0, count_of_input_devices):
            input_devices.append(InputDevice.pyaudio.get_device_info_by_index(device_index))

        return input_devices

    @staticmethod
    def get_device_index_from_name(name_to_find: str):
        """
        Get the index of the device in the input device list by name.
        :param name_to_find: the name of the input device to find.
        :return: the device index if found.
        """
        logging.debug(f"Looking for input device {name_to_find}")
        count_of_input_devices = InputDevice.pyaudio.get_device_count()

        for device_index in range(0, count_of_input_devices):
            device_info = InputDevice.pyaudio.get_device_info_by_index(device_index)
            logging.debug(f"Checking for input device match {device_info['name']}")

            if device_info["name"].upper() == name_to_find.upper():
                return device_index

        raise Exception(f"Input device with name '{name_to_find}' not found")
