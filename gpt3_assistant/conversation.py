import sys
import logging
from gpt3_assistant.computer_voice import ComputerVoice
from gpt3_assistant.exceptions.SpeechRecognitionRequestError import SpeechRecognitionRequestError
from gpt3_assistant.exceptions.CouldNotUnderstandSpeechError import CouldNotUnderstandSpeechError


class Conversation:
    def __init__(self, **kwargs):
        self._previous_responses = []
        self._open_ai_client = kwargs["open_ai_client"]
        self._speech_listener = kwargs["speech_listener"]
        self._input_device_index = kwargs["input_device_index"]
        self._model = kwargs.get("model", "text-davinci-003")
        self._max_tokens = kwargs.get("max_tokens", 200)
        self._safe_word = kwargs.get("safe_word", "EXIT")
        self._computer_voice = ComputerVoice(
            kwargs.get("temp_mp3_filename", "temp.mp3"),
            kwargs.get("lang", None),
            kwargs.get("tld", None),
        )

    def start_conversation(self):
        """
        Start a continuous conversation until the safe word is said alone or the application is exited.
        :return: None
        """
        text: str = None

        try:
            text = self._speech_listener.listen_for_speech(
                device_index=self._input_device_index
            )
        except CouldNotUnderstandSpeechError as e:
            logging.error(e)
        except SpeechRecognitionRequestError as e:
            logging.error(e)
            self.cleanup_and_exit()

        if text is None or len(text) <= 1:
            return self.start_conversation()

        if text.upper() == self._safe_word.upper():
            return self.cleanup_and_exit()

        response = self._open_ai_client.get_completion(
            prompt=text,
            previous_exchanges=self._previous_responses,
            model=self._model,
            max_tokens=self._max_tokens,
        )

        self._previous_responses.append(response)
        response_text = response.computer_response

        logging.info(f"Open AI Response: {response_text}")

        self._computer_voice.speak(response_text)

        if not response.was_cut_short:
            logging.debug("Starting to listen again...")
            return self.start_conversation()

        # If the response was cut short, let the user know they hit the max token limit
        self._computer_voice.speak(
            "I apologize, but I ran out of tokens to finish my response."
        )

    def cleanup_and_exit(self):
        """
        Cleanup the temporary files and exit.
        :return: None
        """
        logging.debug("Making sure temp files are cleaned up...")

        try:
            self._computer_voice.cleanup_temp_files()
        except Exception as e:
            logging.warning(f"Exception while cleaning up temporary files: {e}")

        logging.debug("Closing conversation...")
        sys.exit(0)
