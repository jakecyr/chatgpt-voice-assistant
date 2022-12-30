import mock
import pytest

from gpt3_assistant.input_devices import InputDevices


def return_fake_input_devices():
    return [{"name": "My Mic", "index": 0}, {"name": "My Speaker", "index": 1}]


def return_no_input_devices():
    return []


def test_get_list_of_input_devices_returns_list():
    input_devices = InputDevices.get_list_of_input_devices()
    assert type(input_devices) == list


@mock.patch(
    "gpt3_assistant.input_devices.InputDevices.get_list_of_input_devices",
    return_fake_input_devices,
)
def test_get_input_device_index_when_exists():
    fake_input_devices = return_fake_input_devices()
    input_device_index = InputDevices.get_input_device_index(
        fake_input_devices[0]["name"]
    )
    assert type(input_device_index) == int
    assert input_device_index == fake_input_devices[0]["index"]


@mock.patch(
    "gpt3_assistant.input_devices.InputDevices.get_list_of_input_devices",
    return_no_input_devices,
)
def test_get_input_device_index_throws_error_when_no_devics():
    # make sure the mock is working properly
    assert len(InputDevices.get_list_of_input_devices()) == 0

    with pytest.raises(Exception) as e:
        InputDevices.get_input_device_index("name")

    assert str(e.value) == "No input devices detected"


@mock.patch(
    "gpt3_assistant.input_devices.InputDevices.get_list_of_input_devices",
    return_fake_input_devices,
)
def test_get_input_device_index_throws_error_not_found():
    fake_input_device_name = "AirPods Pro"

    with pytest.raises(Exception) as e:
        InputDevices.get_input_device_index(fake_input_device_name)

    assert (
        str(e.value) == f"Input device with name '{fake_input_device_name}' not found"
    )
