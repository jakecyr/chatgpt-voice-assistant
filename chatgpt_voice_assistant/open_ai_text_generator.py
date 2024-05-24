from __future__ import annotations

from chatgpt_voice_assistant.bases.text_generator import TextGenerator
from chatgpt_voice_assistant.clients.open_ai_client import OpenAIClient
from chatgpt_voice_assistant.exceptions.text_generation_error import TextGenerationError
from chatgpt_voice_assistant.models.message import Message, MessageRole

from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam,
)


class OpenAITextGenerator(TextGenerator):
    """Text Generator using the OpenAI completion API"""

    def __init__(
        self,
        open_ai_key: str,
        model="gpt-4o-2024-05-13",
        max_tokens=200,
        temperature=0.1,
        previous_responses: list[Message] | None = None,
    ) -> None:
        if not open_ai_key or not isinstance(open_ai_key, str):
            raise TextGenerationError("Missing open_ai_key value parameter")

        self._open_ai_client = OpenAIClient(open_ai_key)
        self._model: str = model
        self._max_tokens: int = max_tokens
        self._temperature: float = temperature
        self._previous_responses: list[Message] = previous_responses or []

    def generate_text(
        self,
        prompt: str,
        role: MessageRole = MessageRole.USER,
    ) -> Message:
        """Generates and returns a response message based on the input.

        Args:
            prompt: The prompt to retrieve a response for.
            role: The role to generate a response as (user or assistant).
        """
        self._previous_responses.append(Message(prompt, role))
        messages: list[ChatCompletionMessageParam] = (
            self._messages_to_chat_completion_messages(self._previous_responses)
        )
        generator_response: Message = self._open_ai_client.get_chat_completion(
            messages=messages,
            model=self._model,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
        )
        self._previous_responses.append(generator_response)
        return generator_response

    def reset(self) -> None:
        self._previous_responses = []

    def _messages_to_chat_completion_messages(
        self,
        messages: list[Message],
    ) -> list[ChatCompletionMessageParam]:
        chat_completion_messages: list[ChatCompletionMessageParam] = []

        for message in messages:
            if message.role == MessageRole.USER:
                user_message = ChatCompletionUserMessageParam(
                    content=message.content, role="user"
                )
                chat_completion_messages.append(user_message)
            elif message.role == MessageRole.ASSISTANT:
                assistant_message = ChatCompletionAssistantMessageParam(
                    content=message.content, role="assistant"
                )
                chat_completion_messages.append(assistant_message)

        return chat_completion_messages
