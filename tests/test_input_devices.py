from gpt3_assistant.input_devices import InputDevices


def return_fake_input_devices():
    return [{"name": "My Mic", "index": 0}, {"name": "My Speaker", "index": 1}]


def return_no_input_devices():
    return []


def test_get_list_of_input_devices_returns_list():
    input_devices = InputDevices.get_list_of_input_devices()
    assert type(input_devices) == list
