from typing import TypedDict


class PyAudioDeviceInfo(TypedDict):
    """PyAudio device info object type definition."""
    index: int
    structVersion: str
    name: str
    hostApi: str
    maxInputChannels: int
    maxOutputChannels: int
    defaultLowInputLatency: int
    defaultLowOutputLatency: int
    defaultHighInputLatency: int
    defaultHighOutputLatency: int
    defaultSampleRate: int
