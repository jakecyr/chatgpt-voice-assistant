from gpt3_assistant.input_devices import InputDevices
from mock import MagicMock
from pyaudio import PyAudio

fake_input_devices = [
    {"name": "My Mic", "index": 0, "maxInputChannels": 0},
    {"name": "My Speaker", "index": 1, "maxInputChannels": 1}
]

InputDevices.py_audio = MagicMock(spec=PyAudio)
InputDevices.py_audio.get_device_count = MagicMock(return_value=2)
InputDevices.py_audio.get_device_info_by_index = MagicMock()
InputDevices.py_audio.get_device_info_by_index.side_effect = fake_input_devices


def test_get_list_of_input_devices_returns_list():
    input_devices = InputDevices.get_list_of_input_devices()
    assert type(input_devices) == list
    assert len(input_devices) == 1
    assert input_devices[0].name == fake_input_devices[1]['name']
    assert input_devices[0].index == fake_input_devices[1]['index']


def test_get_list_of_input_devices_no_inputs_returns_empty_list():
    InputDevices.py_audio.get_device_count = MagicMock(return_value=0)
    input_devices = InputDevices.get_list_of_input_devices()
    assert type(input_devices) == list
    assert len(input_devices) == 0
