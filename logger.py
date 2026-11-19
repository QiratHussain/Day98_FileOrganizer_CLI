import logging


def setup_logger(name: str = "file-organizer") -> logging.Logger:

    logger = logging.getLogger(name)

    # Prevent duplicate handlers if called twice
    if logger.handlers:
        return logger