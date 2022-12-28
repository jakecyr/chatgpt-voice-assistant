import logging


def set_log_level(log_level: str = None) -> None:
    log_level = "INFO" if log_level is None else log_level

    # set log level
    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % log_level)

    logging.basicConfig(level=numeric_level)
