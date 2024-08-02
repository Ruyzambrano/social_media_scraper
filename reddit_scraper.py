"""Reddit Scraper"""
from praw import Reddit

from functions import get_secrets, configure_logging, write_log_message

def get_reddit_instance(env: dict) -> Reddit:
    """Returns a Reddit instance"""
    # Read-only instance
    reddit_read_only = Reddit(client_id=env["REDDIT_KEY"],
                                client_secret=env["REDDIT_SECRET_KEY"],
                                user_agent=env["REDDIT_AGENT"])

    # Authorized instance
    # reddit_authorized = Reddit(client_id="",         # your client id
    #                                 client_secret="",      # your client secret
    #                                 user_agent="",        # your user agent
    #                                 username="",        # your reddit username
    #                                 password="")        # your reddit password
    return reddit_read_only

if __name__ == "__main__":
    reddit_logger = configure_logging("reddit.log")
    secrets = get_secrets(reddit_logger)
    reddit_instance = get_reddit_instance(secrets)
    write_log_message(reddit_logger, "Finished Running\n")
