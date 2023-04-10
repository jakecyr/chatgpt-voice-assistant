from typing import List, Optional

from chatgpt_voice_assistant.bases.text_generator import TextGenerator
from chatgpt_voice_assistant.clients.open_ai_client import OpenAIClient
from chatgpt_voice_assistant.exceptions.text_generation_error import TextGenerationError
from chatgpt_voice_assistant.models.message import Message, MessageRole
from chatgpt_voice_assistant.models.open_ai_chat_completion import ChatCompletionMessage


class OpenAITextGenerator(TextGenerator):
    """Text Generator using the OpenAI completion API"""

    def __init__(
        self,
        open_ai_key: str,
        model="gpt-3.5-turbo",
        max_tokens=200,
        temperature=0.7,
        previous_responses: Optional[List[Message]] = None,
    ):
        if not open_ai_key or not isinstance(open_ai_key, str):
            raise TextGenerationError("Missing open_ai_key value parameter")

        self._open_ai_client = OpenAIClient(open_ai_key)
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature
        self._previous_responses: List[Message] = previous_responses or []

    def generate_text(
        self, prompt: str, role: MessageRole = MessageRole.USER
    ) -> Message:
        """Generates and returns a response message based on the input.

        Args:
            prompt: The prompt to retrieve a response for.
            role: The role to generate a response as (user or assistant).
        """
        self._previous_responses.append(Message(prompt, role))

        generator_response: Message = self._open_ai_client.get_chat_completion(
            messages=self._messages_to_chat_completion_messages(
                self._previous_responses
            ),
            model=self._model,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
        )

        self._previous_responses.append(generator_response)

        return generator_response

    def _messages_to_chat_completion_messages(
        self,
        messages: List[Message],
    ) -> List[ChatCompletionMessage]:
        chat_completion_messages: List[ChatCompletionMessage] = []

        for message in messages:
            chat_completion_messages.append(
                {"content": message.content, "role": message.role}
            )

        return chat_completion_messages
