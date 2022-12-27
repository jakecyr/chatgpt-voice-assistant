import sys
import signal
import logging
from command_line_parser import CommandLineParser
from conversation import Conversation
from input_device import InputDevice
from speech_listener import SpeechListener
from open_ai_client import OpenAIClient

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

    conversation = Conversation(
        open_ai_client=OpenAIClient(options.open_ai_key),
        speech_listener=SpeechListener(),
        input_device_index=InputDevice.get_input_device_index(options.input_device_name),
        lang=options.lang,
        tld=options.tld
    )


    def signal_handler(_sig, _frame):
        conversation.cleanup_and_exit()


    signal.signal(signal.SIGINT, signal_handler)
    conversation.start_conversation()
