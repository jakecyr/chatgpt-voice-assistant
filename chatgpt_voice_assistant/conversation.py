import logging
import sys
from typing import Optional

from chatgpt_voice_assistant.bases.listener import Listener
from chatgpt_voice_assistant.bases.responder import Responder
from chatgpt_voice_assistant.bases.text_generator import TextGenerator
from chatgpt_voice_assistant.exceptions.failed_to_understand_listener_error import (
    FailedToUnderstandListenerError,
)
from chatgpt_voice_assistant.exceptions.listener_fatal_error import ListenerFatalError
from chatgpt_voice_assistant.exceptions.no_input_listener_error import (
    NoInputListenerError,
)


class Conversation:
    """Class to handle the conversation between the user and the computer."""

    def __init__(
        self,
        listener: Listener,
        text_generator: TextGenerator,
        responder: Responder,
        safe_word: Optional[str] = None,
        wake_word: Optional[str] = None,
    ):
        """
        Create a new Conversation instance.

        Args:
            listener: the listen instance to use to get user input.
            text_generator: the text generation instance.
            responder: the service to response to the input received.
            safe_word: optional safe word string that causes the program to exit on input.
            wake_word: optional wake word that will trigger the program to respond.
        """
        self._listener: Listener = listener
        self._text_generator: TextGenerator = text_generator
        self._responder: Responder = responder
        self._safe_word: str = "EXIT" if safe_word is None else safe_word.upper()
        self._wake_word: Optional[str] = wake_word.upper() if wake_word else None

    def start_conversation(self, run_once: bool = False) -> None:
        """
        Start a continuous conversation until the safe word or the application is exited.
        :param run_once: if the method should run once or keep running.
        :return: None
        """
        text: Optional[str] = None

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

        if self._wake_word is not None:
            if not text.upper().startswith(self._wake_word):
                logging.info(
                    f"Speech recognized, but wake word '{self._wake_word}' not heard."
                )

                logging.debug("Starting to listen again...")
                return self.start_conversation(run_once=run_once)

            wake_word_length = len(self._wake_word)
            text = text[wake_word_length:].strip()

        if text.upper() == self._safe_word:
            logging.info("Safe word detected, exiting...")
            return self._cleanup_and_exit()

        response = self._text_generator.generate_text(text)
        response_text = response.content

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
