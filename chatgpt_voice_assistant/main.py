from chatgpt_voice_assistant.bases.listener import Listener
from chatgpt_voice_assistant.bases.options_parser import OptionsParser
from chatgpt_voice_assistant.bases.text_generator import TextGenerator
from chatgpt_voice_assistant.bases.text_to_speech_client import TextToSpeechClient
from chatgpt_voice_assistant.clients.apple_say_text_to_speech_client import (
    AppleSayTextToSpeechClient,
)
from chatgpt_voice_assistant.clients.google_text_to_speech_client import (
    GoogleTextToSpeechClient,
)
from chatgpt_voice_assistant.command_line_parser import CommandLineParser
from chatgpt_voice_assistant.computer_voice_responder import ComputerVoiceResponder
from chatgpt_voice_assistant.conversation import Conversation
from chatgpt_voice_assistant.helpers.get_input_device_from_user import (
    get_input_device_from_user,
)
from chatgpt_voice_assistant.helpers.set_keyboard_interrupt_handler import (
    set_keyboard_interrupt_handler,
)
from chatgpt_voice_assistant.helpers.set_log_level import set_log_level
from chatgpt_voice_assistant.input_devices import InputDevices
from chatgpt_voice_assistant.models.input_device import InputDevice
from chatgpt_voice_assistant.open_ai_text_generator import OpenAITextGenerator
from chatgpt_voice_assistant.speech_listener import SpeechListener


def main() -> None:
    options_parser: OptionsParser = CommandLineParser()

    # parse the options passed in from the user
    options = options_parser.parse()

    # set log level from CLI options
    set_log_level(options.log_level)

    # get all input devices on the current machine
    input_devices: list[InputDevice] = InputDevices.get_list_of_input_devices()

    # ask the user which input device to use for this session
    input_device: InputDevice = get_input_device_from_user(
        input_devices=input_devices, input_device_name=options.input_device_name
    )

    # service to listen for speech and convert it to text
    listener: Listener = SpeechListener(input_device)

    # service to generate text given an input
    text_generator: TextGenerator = OpenAITextGenerator(
        open_ai_key=options.open_ai_key, model=options.open_ai_model
    )

    # client to create speech from a given text
    text_to_speech_client: TextToSpeechClient
    if options.tts == "apple":
        text_to_speech_client = AppleSayTextToSpeechClient()
    else:
        text_to_speech_client = GoogleTextToSpeechClient(options.lang, options.tld)

    # service to respond to the user the generated text
    responder = ComputerVoiceResponder(
        text_to_speech_client, "temp_audio", options.speech_rate
    )

    # set interrupt to exit the process when Cmd+C / Ctrl+C is hit
    set_keyboard_interrupt_handler()

    conversation = Conversation(
        listener=listener,
        text_generator=text_generator,
        responder=responder,
        safe_word=options.safe_word,
        wake_word=options.wake_word,
    )

    conversation.start_conversation()


if __name__ == "__main__":
    main()
