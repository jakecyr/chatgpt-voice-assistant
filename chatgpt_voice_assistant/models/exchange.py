from typing import NamedTuple, Optional


class Exchange(NamedTuple):
    """Details about an exchange between a user and the computer"""

    user_message: str
    computer_response: str
    was_cut_short: Optional[bool] = None
