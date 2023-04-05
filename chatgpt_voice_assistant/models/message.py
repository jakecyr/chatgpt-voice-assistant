from enum import Enum
from typing import NamedTuple, Optional


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(NamedTuple):
    """Details about an exchange between a user and the computer"""

    content: str
    role: MessageRole
    was_cut_short: Optional[bool] = None
