from gpt3_assistant.bases.text_generator import TextGenerator
from clients.open_ai_client import OpenAIClient
from sys import exit
from gpt3_assistant.models.exchange import Exchange
import logging


class OpenAITextGenerator(TextGenerator):

    def __init__(self, open_ai_key: str, **kwargs):
        if not open_ai_key:
            logging.error("Missing open-ai-key parameter")
            exit(1)

        self._open_ai_client = OpenAIClient(open_ai_key)
        self._model = kwargs.get("model", "text-davinci-003")
        self._max_tokens = kwargs.get("max_tokens", 200)
        self._previous_responses: list[Exchange] = []

    def generate_text(self, input_text) -> Exchange:
        """
        Generates text based on the input and returns it.
        :param input_text: the input text.
        :return: the response.
        """
        full_prompt_with_history: str = self._get_request_under_max_tokens(input_text)

        exchange: Exchange = self._open_ai_client.get_completion(
            prompt=full_prompt_with_history,
            model=self._model,
            max_tokens=self._max_tokens,
            temperature=0.7
        )

        self._previous_responses.append(exchange)

        return exchange

    def _get_request_under_max_tokens(self, prompt):
        """
        Get a full request with previous context to send to the completion endpoint.
        :param str prompt: the new prompt to be sent for completion.
        :return: str the full request with context and the new prompt to be sent to the completion endpoint.
        """
        new_request = f"User: {prompt}\nAssistant: "
        request_header = ""

        for exchange in self._previous_responses:
            exchange_string = f"User: {exchange.user_message}\nAssistant: {exchange.computer_response}"
            draft_request = f"{request_header}\n{exchange_string}\n{new_request}"

            if len(draft_request) > self._max_tokens:
                return f"{request_header}\n{new_request}"
            else:
                request_header += f"\n{exchange_string}"

        return f"{request_header}\n{new_request}"
