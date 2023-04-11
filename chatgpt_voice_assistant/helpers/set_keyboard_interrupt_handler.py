import logging
import signal
import sys
from typing import NoReturn


def set_keyboard_interrupt_handler() -> None:
    def signal_handler(_sig, _frame) -> NoReturn:
        logging.info("Shutting down...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
