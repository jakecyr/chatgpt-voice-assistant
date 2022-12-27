import sys
import signal
import logging
from gpt3_assistant.command_line_parser import CommandLineParser
from gpt3_assistant.conversation import Conversation
from gpt3_assistant.input_devices import InputDevices
from gpt3_assistant.speech_listener import SpeechListener
from gpt3_assistant.clients.open_ai_client import OpenAIClient

if __name__ == "__main__":
    # get CLI parameters
    options = CommandLineParser.parse()
    log_level = "INFO" if options.log_level is None else options.log_level

    # set log level
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % log_level)
    logging.basicConfig(level=numeric_level)

    # validate parameters
    if not options.open_ai_key:
        logging.error("Missing open-ai-key parameter")
        sys.exit(1)

    input_device_index = None

    if options.input_device_name is None:
        input_devices = InputDevices.get_list_of_input_devices()

        for index, input_device in enumerate(input_devices):
            print(f"{index + 1}) {input_device['name']}")

        chosen_device_index = (
                int(input("Which input device would you like to use? ")) - 1
        )

        if chosen_device_index < 0 or chosen_device_index > len(input_devices) - 1:
            raise Exception("Invalid input device index chosen")

        chosen_device = input_devices[chosen_device_index]
        input_device_index = chosen_device["index"]
    else:
        input_device_index = InputDevices.get_input_device_index(
            options.input_device_name
        )

    conversation = Conversation(
        open_ai_client=OpenAIClient(options.open_ai_key),
        speech_listener=SpeechListener(),
        input_device_index=input_device_index,
        lang=options.lang,
        tld=options.tld,
        safe_word=options.safe_word
    )


    def signal_handler(_sig, _frame):
        conversation.cleanup_and_exit()


    signal.signal(signal.SIGINT, signal_handler)
    conversation.start_conversation()
