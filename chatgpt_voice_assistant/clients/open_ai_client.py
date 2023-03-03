import logging

import openai

from chatgpt_voice_assistant.exceptions.text_generation_error import \
    TextGenerationError
from chatgpt_voice_assistant.models.exchange import Exchange


# Client to interact with the OpenAI API
class OpenAIClient:
    def __init__(self, api_key: str):
        logging.debug("Setting Open API key...")
        openai.api_key = api_key

    def get_completion(
        self, prompt, model="gpt-3.5-turbo", max_tokens=200, temperature=0.7
    ) -> Exchange:
        """
        Get a chat completion (response) from the specified OpenAI GPT-3 model.
        Reference: https://platform.openai.com/docs/api-reference/chat/create

        Args:
            prompt:       the prompt to send to the model for completion.
            model:        optionally specify the model to use.
            max_tokens:   the max number of tokens to use including the prompt and response.
            temperature:  the temperature for the model to use.

        Returns:
            the exchange between the user and the model
        """
        completion = openai.Completion.create(
            model=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature
        )

        choices = completion["choices"]
        tokens_used = completion["usage"]["total_tokens"]
        was_cut_short = False

        if len(choices) == 0:
            raise TextGenerationError(
                f"No choices returned from Open AI for prompt: {prompt}"
            )

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
