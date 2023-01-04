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
from gpt3_assistant.exceptions.respond_error import RespondError


class Conversation:
    def __init__(self, **kwargs):
        self._listener: Listener = kwargs["listener"]
        self._text_generator: TextGenerator = kwargs["text_generator"]
        self._responder: Responder = kwargs["responder"]

        safe_word = kwargs.get("safe_word", None)
        self._safe_word = "EXIT" if safe_word is None else safe_word

    def start_conversation(self, run_once=False):
        """
        Start a continuous conversation until the safe word or the application is exited.
        :return: None
        """
        text: str = None

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

        if text.upper() == self._safe_word.upper():
            return self._cleanup_and_exit()

        response = self._text_generator.generate_text(text)
        response_text = response.computer_response

        logging.info(f"Text generator response: {response_text}")

        self._responder.respond(response_text)

        if not run_once:
            logging.debug("Starting to listen again...")
            self.start_conversation(run_once=run_once)

    def _send_response(self, response_text: str) -> None:
        try:
            self._responder.respond(response_text)
        except RespondError as e:
            logging.error(f"Error responding to user: {e}")

    def _cleanup_and_exit(self, exit_code=0):
        sys.exit(exit_code)
