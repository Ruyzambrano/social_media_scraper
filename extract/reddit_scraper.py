"""Reddit Scraper that works"""
from logging import Logger
from datetime import datetime

from praw import Reddit
from praw.models.reddit.subreddit import Subreddit
from praw.models.reddit.submission import Submission
import pandas as pd

from functions import get_secrets, configure_logging, write_log_message

DATA_FILEPATH = "./data/reddit_posts.csv"

def get_reddit_instance(env: dict) -> Reddit:
    """Returns a read-only Reddit instance"""
    return Reddit(
        client_id=env["REDDIT_KEY"],
        client_secret=env["REDDIT_SECRET_KEY"],
        user_agent=env["REDDIT_AGENT"])


def get_subreddit(reddit_instance: Reddit, subreddit_instance: str) -> Subreddit:
    return reddit_instance.subreddit(subreddit_instance)

def get_latest_posts(subreddit_instance: Subreddit, limit=5):
    return subreddit_instance.new(limit=limit)

def display_post(post: Submission):
    print(post.title)
    print(post.selftext)
    print(datetime.fromtimestamp(post.created_utc))

def get_latest_time() -> datetime:
    data = pd.read_csv(DATA_FILEPATH)
    time_data = pd.to_datetime(data["Time Posted"], errors='coerce', format="%Y-%m-%d %H:%M:%S")
    return max(time_data, default=datetime.min)


def add_posts_to_pandas(posts: list[Submission]) -> pd.DataFrame:
    posts_dict = {"Title": [], 
                  "Post Text": [],
                  "ID": [],
                  "Score": [],
                  "Total Comments": [],
                  "Post URL": [],
                  "Time Posted": []
                  }
    for post in posts:
        post_date = datetime.fromtimestamp(post.created_utc)
        if post_date > get_latest_time():
            # Title of each post
            posts_dict["Title"].append(post.title)

            # Text inside a post
            posts_dict["Post Text"].append(post.selftext)

            # Unique ID of each post
            posts_dict["ID"].append(post.id)

            # The score of a post
            posts_dict["Score"].append(post.score)

            # Total number of comments inside the post
            posts_dict["Total Comments"].append(post.num_comments)

            # URL of each post
            posts_dict["Post URL"].append(post.url)

            # Time of Post
            posts_dict["Time Posted"].append(post_date)

    return pd.DataFrame(posts_dict)

def write_to_csv(reddit_logger: Logger, dataframe: pd.DataFrame):
    dataframe.to_csv(DATA_FILEPATH, index=False, mode="a", 
                           header=False)
    write_log_message(reddit_logger, f"{len(dataframe)} record(s) added to csv file.")


if __name__ == "__main__":
    reddit_logger = configure_logging("./logs/reddit.log")
    secrets = get_secrets(reddit_logger)
    reddit = get_reddit_instance(secrets)
    subreddit = get_subreddit(reddit, "cats")
    subreddit_posts = get_latest_posts(subreddit, 20)
    posts_dataframe = add_posts_to_pandas(subreddit_posts)
    write_to_csv(reddit_logger, posts_dataframe)
    write_log_message(reddit_logger, "Finished Running\n")
