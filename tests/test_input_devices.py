from mock import MagicMock, patch

from chatgpt_voice_assistant.input_devices import InputDevices

fake_input_devices = [
    {"name": "My Mic", "index": 0, "maxInputChannels": 0},
    {"name": "My Speaker", "index": 1, "maxInputChannels": 1},
]


@patch("pyaudio.PyAudio.get_device_count", return_value=2)
@patch("pyaudio.PyAudio.get_device_info_by_index", side_effect=fake_input_devices)
def test_get_list_of_input_devices_returns_list(
    get_device_count: MagicMock, get_device_info_by_index: MagicMock
):
    input_devices = InputDevices.get_list_of_input_devices()
    assert isinstance(input_devices, list)
    assert len(input_devices) == 1
    assert input_devices[0].name == fake_input_devices[1]["name"]
    assert input_devices[0].index == fake_input_devices[1]["index"]


@patch("pyaudio.PyAudio.get_device_count", return_value=0)
@patch("pyaudio.PyAudio.get_device_info_by_index", side_effect=fake_input_devices)
def test_get_list_of_input_devices_no_inputs_returns_empty_list(
    get_device_count: MagicMock, get_device_info_by_index: MagicMock
):
    input_devices = InputDevices.get_list_of_input_devices()
    assert isinstance(input_devices, list)
    assert len(input_devices) == 0


@patch("pyaudio.PyAudio.get_device_count", return_value=2)
@patch("pyaudio.PyAudio.get_device_info_by_index", side_effect=fake_input_devices)
def test_get_all_pyaudio_input_devices_returns_list(
    get_device_count: MagicMock, get_device_info_by_index: MagicMock
):
    input_devices = InputDevices._get_all_pyaudio_input_devices()
    assert isinstance(input_devices, list)
    assert len(input_devices) == 1


@patch("pyaudio.PyAudio.get_device_count", return_value=0)
@patch("pyaudio.PyAudio.get_device_info_by_index", side_effect=fake_input_devices)
def test_get_all_pyaudio_input_devices_no_inputs_returns_empty_list(
    get_device_count: MagicMock, get_device_info_by_index: MagicMock
):
    input_devices = InputDevices._get_all_pyaudio_input_devices()
    assert isinstance(input_devices, list)
    assert len(input_devices) == 0
