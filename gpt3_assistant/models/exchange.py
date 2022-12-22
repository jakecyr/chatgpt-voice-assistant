from typing import NamedTuple


class Exchange(NamedTuple):
    user_message: str
    computer_response: str
    was_cut_short: bool | None = None
