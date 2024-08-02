from datetime import datetime

from dotenv import dotenv_values
from logging import getLogger, Logger, DEBUG, FileHandler

import tweepy

def configure_logging() -> Logger:
    logger = getLogger("tweepy")
    logger.setLevel(DEBUG)
    handler = FileHandler(filename="tweepy.log")
    logger.addHandler(handler)
    logger.info("Starting App")
    return logger

def get_secrets(logger: Logger) -> dict:
    logger.info(f"{datetime.now()}: Getting Secrets")
    return dotenv_values()

def authenticate_tweepy(secrets: dict) -> tweepy.API:
    auth = tweepy.OAuth1UserHandler(
        env["API_KEY"],
        env["API_SECRET_KEY"],
        env["ACCESS_TOKEN"], 
        env["ACCESS_TOKEN_SECRET"]
    )
    return tweepy.API(auth)

if __name__ == "__main__":
    logger = configure_logging()

    env = get_secrets(logger)

    app = authenticate_tweepy(env)

    print(app.get_user(screen_name="ruyzambrano"))

    logger.info("Finish run\n")
