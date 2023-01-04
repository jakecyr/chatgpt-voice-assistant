import logging


def set_log_level(log_level: str | None = None) -> None:
    log_level = "INFO" if log_level is None else log_level

    # set log level
    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.basicConfig(level=numeric_level)
