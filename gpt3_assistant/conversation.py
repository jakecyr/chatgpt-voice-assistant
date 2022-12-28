import logging
from exceptions.speech_recognition_request_error import SpeechRecognitionRequestError
from exceptions.could_not_understand_speech_error import CouldNotUnderstandSpeechError
from gpt3_assistant.bases.text_generator import TextGenerator
from gpt3_assistant.bases.listener import Listener
from gpt3_assistant.bases.responder import Responder


class Conversation:
    def __init__(self, **kwargs):
        self._listener: Listener = kwargs["listener"]
        self._text_generator: TextGenerator = kwargs['text_generator']
        self._responder: Responder = kwargs['responder']

        safe_word = kwargs.get("safe_word", None)
        self._safe_word = "EXIT" if safe_word is None else safe_word

    def start_conversation(self):
        """
        Start a continuous conversation until the safe word is said alone or the application is exited.
        :return: None
        """
        text: str = None

        try:
            text = self._listener.listen_for_speech()
        except CouldNotUnderstandSpeechError as e:
            logging.error(e)
        except SpeechRecognitionRequestError as e:
            logging.error(e)
            self.cleanup_and_exit()

        if text is None or len(text) <= 1:
            return self.start_conversation()

        if text.upper() == self._safe_word.upper():
            return self.cleanup_and_exit()

        response = self._text_generator.generate_text(text)
        response_text = response.computer_response

        logging.info(f"Text generator response: {response_text}")

        self._responder.respond(response_text)

        # If the response was cut short, let the user know they hit the max token limit
        if response.was_cut_short:
            self._responder.respond(
                "I apologize, but I ran out of tokens to finish my response."
            )

        logging.debug("Starting to listen again...")
        self.start_conversation()
