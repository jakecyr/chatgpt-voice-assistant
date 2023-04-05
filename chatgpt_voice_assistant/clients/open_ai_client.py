import json
import logging
from typing import List

import openai

from chatgpt_voice_assistant.exceptions.text_generation_error import TextGenerationError
from chatgpt_voice_assistant.models.message import Message
from chatgpt_voice_assistant.models.open_ai_chat_completion import ChatCompletionMessage


class OpenAIClient:
    """Client to interact with the OpenAI API."""

    def __init__(self, api_key: str):
        logging.debug("Setting Open API key...")
        openai.api_key = api_key

    def get_chat_completion(
        self,
        messages: List[ChatCompletionMessage],
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> Message:
        """
        Returns a completion (response) from the specified OpenAI GPT model.
        Reference: https://platform.openai.com/docs/api-reference/chat

        Args:
            messages:    messages to provide as context.
            prompt:      the prompt to send to the model for completion.
            model:       optionally specify the model to use.
            max_tokens:  the max number of tokens to use including the prompt and response.
            temperature: the temperature for the model to use.

        Returns:
            The exchange between the user and the model.
        """
        if len(messages) == 0:
            raise ValueError(
                "The messages argument must be a list with at least one object."
            )

        logging.debug(
            f"Sending prompt to chat completion endpoint: {json.dumps(messages)}"
        )

        completion = openai.ChatCompletion.create(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        choices = completion["choices"]
        tokens_used = completion["usage"]["total_tokens"]
        was_cut_short = False

        if len(choices) == 0:
            raise TextGenerationError(
                "No choices returned from Open AI for provided context"
            )

        first_choice = choices[0]

        if first_choice["finish_reason"] == "length":
            logging.warning(
                "OpenAI stopped generating due to a limit on the max tokens. "
                f"Max tokens is set to: {max_tokens}. "
                f"Total tokens consumed with prompt were: {tokens_used}"
            )
            was_cut_short = True

        first_choice_text = (
            first_choice["message"]["content"].replace("\n", " ").strip()
        )

        return Message(
            first_choice_text, first_choice["message"]["role"], was_cut_short
        )
