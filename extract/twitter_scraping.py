"""A Twitter scraper that does not work without paying $100 a month"""
from tweepy import API, OAuth1UserHandler, Forbidden

from functions import get_secrets, configure_logging, write_log_message


def authenticate_tweepy(secrets: dict) -> API:
    """Gets an instance of a Twitter API with authentication"""
    auth = OAuth1UserHandler(
        secrets["TWITTER_API_KEY"],
        secrets["TWITTER_API_SECRET_KEY"],
        secrets["TWITTER_ACCESS_TOKEN"],
        secrets["TWITTER_ACCESS_TOKEN_SECRET"]
    )
    return API(auth)


if __name__ == "__main__":
    twitter_logger = configure_logging("twitter.log")

    env = get_secrets(twitter_logger)

    try:

        app = authenticate_tweepy(env)
        print(app.get_user(screen_name="elonmusk"))

    except Forbidden as e:
        for index, code in enumerate(e.api_codes):
            print(f"{code}: {e.api_messages[index]}")

    write_log_message(twitter_logger, "Finish run\n")
