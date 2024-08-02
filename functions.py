"""Contains reuseable functions"""
from datetime import datetime
from logging import getLogger, Logger, DEBUG, FileHandler

from dotenv import dotenv_values


def get_secrets(logger: Logger) -> dict:
    """Returns the .env as a dictionary"""
    write_log_message(logger, "Getting Secrets")
    return dotenv_values()


def configure_logging(filename: str) -> Logger:
    """Returns a configured logger object"""
    logger = getLogger()
    logger.setLevel(DEBUG)
    handler = FileHandler(filename=filename)
    logger.addHandler(handler)
    logger.info("Starting App")
    return logger


def write_log_message(logger: Logger, message: str) -> None:
    """Writes a message to the different loggers"""
    logger.info(f"{datetime.now()}: {message}")
