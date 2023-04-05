from typing import NamedTuple


class ChatCompletionMessage(NamedTuple):
    role: str
    content: str
