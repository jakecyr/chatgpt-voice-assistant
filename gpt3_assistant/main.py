import sys
import os
import signal
from computer_voice import ComputerVoice
from open_ai_client import OpenAIClient
from speech_listener import SpeechListener
import logging
from exceptions.SpeechRecognitionRequestError import SpeechRecognitionRequestError
from exceptions.CouldNotUnderstandSpeechError import CouldNotUnderstandSpeechError
import argparse

lang = os.getenv("LANGUAGE")
tld = os.getenv("TOP_LEVEL_DOMAIN")
previous_responses = []


class Main:

    def __init__(self, open_ai_key, input_device_name):
        self.open_ai_key = open_ai_key
        self.input_device_name = input_device_name
        self.computer_voice = ComputerVoice("temp.mp3", lang, tld)

    def start_conversation(self):
        open_ai_client = OpenAIClient(self.open_ai_key)
        speech_listener = SpeechListener()
        text: str = None

        try:
            text = speech_listener.listen_for_speech(device_name=self.input_device_name)
        except CouldNotUnderstandSpeechError as e:
            logging.error(e)
        except SpeechRecognitionRequestError as e:
            logging.error(e)
            self.cleanup_and_exit()

        if text == "Exit" or text == "exit":
            self.cleanup_and_exit()

        if text is None or len(text) <= 1:
            self.start_conversation()

        response = open_ai_client.get_completion(
            prompt=text,
            previous_exchanges=previous_responses,
            model="text-davinci-003",
            max_tokens=200
        )

        previous_responses.append(response)
        response_text = response.get_computer_response()

        logging.info(f"Open AI Response: {response_text}")

        self.computer_voice.speak(response_text)

        if not response.was_cut_short():
            logging.debug("Starting to listen again...")
            self.start_conversation()

        # If the response was cut short, let the user know they hit the max token limit
        self.computer_voice.speak("I apologize, but I ran out of tokens to finish my response.")

    def cleanup_and_exit(self):
        logging.debug("Making sure temp files are cleaned up...")
        self.computer_voice.cleanup_temp_files()
        logging.debug('Closing conversation...')
        sys.exit(0)


def get_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", help="If to print at the debug level or not.", default="INFO", type=str)
    parser.add_argument("--input-device-name", help="Input device name", default=None, type=str)
    parser.add_argument("--open-ai-key", help="Open AI Secret Key", required=True, type=str)
    return parser.parse_args()


def set_logging_level(level_name):
    numeric_level = getattr(logging, level_name.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % level_name)
    logging.basicConfig(level=numeric_level)


if __name__ == "__main__":
    args = get_command_line_arguments()
    log_level = args.log_level
    set_logging_level(log_level)

    input_device_name = args.input_device_name if 'input_device_name' in args else None

    if not args.open_ai_key:
        logging.error("missing open-ai-key CLI")
        sys.exit(1)

    main = Main(args.open_ai_key, input_device_name)


    def signal_handler(sig, frame):
        main.cleanup_and_exit()


    signal.signal(signal.SIGINT, signal_handler)
    main.start_conversation()
