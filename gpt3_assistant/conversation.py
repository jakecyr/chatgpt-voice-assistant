import logging
import sys

from gpt3_assistant.bases.listener import Listener
from gpt3_assistant.bases.responder import Responder
from gpt3_assistant.bases.text_generator import TextGenerator
from gpt3_assistant.exceptions.failed_to_understand_listener_error import (
    FailedToUnderstandListenerError,
)
from gpt3_assistant.exceptions.listener_fatal_error import ListenerFatalError
from gpt3_assistant.exceptions.no_input_listener_error import NoInputListenerError


class Conversation:
    """Class to handle the conversation between the user and the computer."""

    def __init__(self, **kwargs):
        """
        Create a new Conversation instance.
        :keyword Listener listener: the listen instance to use to get user input.
        :keyword TextGenerator text_generator: the text generation instance.
        :keyword Responder responder: the service to response to the input received.
        :keyword str safe_word: optional safe word string that causes the program to exit on input.
        """
        self._listener: Listener = kwargs["listener"]
        self._text_generator: TextGenerator = kwargs["text_generator"]
        self._responder: Responder = kwargs["responder"]

        safe_word: str | None = kwargs.get("safe_word", None)
        self._safe_word: str = "EXIT" if safe_word is None else safe_word.upper()

    def start_conversation(self, run_once=False) -> None:
        """
        Start a continuous conversation until the safe word or the application is exited.
        :param run_once: if the method should run once or keep running.
        :return: None
        """
        text: str | None = None

        try:
            text = self._listener.listen()
        except ListenerFatalError as e:
            logging.error(f"Listener fatal error: {e}")
            self._cleanup_and_exit()
            return
        except (FailedToUnderstandListenerError, NoInputListenerError) as e:
            logging.error(f"Listener error: {e}")
            if not run_once:
                self.start_conversation(run_once=run_once)
            return

        if text is None:
            logging.error("Listener returned None")
            return

        print(f"SAFE WORD: {self._safe_word}")

        if text.upper() == self._safe_word:
            logging.info("Safe word detected, exiting...")
            return self._cleanup_and_exit()

        response = self._text_generator.generate_text(text)
        response_text = response.computer_response

        logging.info(f"Text generator response: {response_text}")

        self._responder.respond(response_text)

        if not run_once:
            logging.debug("Starting to listen again...")
            self.start_conversation(run_once=run_once)

    def _cleanup_and_exit(self, exit_code: int = 0) -> None:
        """
        Run cleanup (if needed) and end the application process.
        :param exit_code: the exit code to end the process with.
        :return: None
        """
        sys.exit(exit_code)
