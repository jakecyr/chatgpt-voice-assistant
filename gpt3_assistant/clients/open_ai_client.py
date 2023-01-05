import logging

import openai

from gpt3_assistant.models.exchange import Exchange
from gpt3_assistant.exceptions.text_generation_error import TextGenerationError


# Client to interact with the OpenAI API
class OpenAIClient:
    def __init__(self, api_key: str):
        logging.debug("Setting Open API key...")
        openai.api_key = api_key

    def get_completion(
            self, prompt, model="text-davinci-003", max_tokens=200, temperature=0.7
    ) -> Exchange:
        """
        Get a completion (response) from the specified OpenAI GPT-3 model.
        Reference: https://beta.openai.com/docs/api-reference/completions

        :param str prompt:       the prompt to send to the model for completion.
        :param str model:        optionally specify the model to use.
        :param int max_tokens:   the max number of tokens to use including the prompt and response.
        :param int temperature:  the temperature for the model to use.
        """
        completion = openai.Completion.create(
            model=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature
        )

        choices = completion["choices"]
        tokens_used = completion["usage"]["total_tokens"]
        was_cut_short = False

        if len(choices) == 0:
            raise TextGenerationError(f"No choices returned from Open AI for prompt: {prompt}")

        first_choice = choices[0]

        if first_choice["finish_reason"] == "length":
            logging.warning(
                "OpenAI stopped producing output due to a limit on the max tokens"
            )
            logging.warning(
                "Max tokens is set to: %d. Total tokens consumed with prompt were: %d",
                max_tokens,
                tokens_used,
            )
            was_cut_short = True

        first_choice_text = first_choice["text"].replace("\n", " ").strip()

        return Exchange(prompt, first_choice_text, was_cut_short)
