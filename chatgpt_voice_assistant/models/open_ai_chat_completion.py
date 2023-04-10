from typing import TypedDict


class ChatCompletionMessage(TypedDict):
    role: str
    content: str
