from twscrape import Tweet, API, User
from datetime import datetime
import pickle


def extract_date_from_tweet(tweet) -> str:
    """Extract the date from a tweet and return it as a string in the format 'DD-MM-YYYY'."""
    date = tweet.date
    formatted_date = date.strftime('%d-%m-%Y')
    return formatted_date


def is_valid_date(date_string: str) -> bool:
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def extract_date_from_datetime(date) -> str:
    """Extract the date from a datetime object and return it as a string in the format 'DD-MM-YYYY'."""
    formatted_date = date.strftime('%Y-%m-%d')
    return formatted_date


def extract_date_from_tweet_year_month_day(tweet: Tweet) -> str:
    """Extract the date from a tweet and return it as a string in the format 'YYYY-MM-DD'."""
    date = tweet.date
    formatted_date = date.strftime('%Y-%m-%d')
    return formatted_date


def remove_reply_tweets_from_the_list(tweets: list[Tweet]) -> list[Tweet]:
    new_tweets = []
    for tweet in tweets:
        if tweet.inReplyToUser is None:
            new_tweets.append(tweet)
    return new_tweets


def is_valid_api(api) -> bool:
    if api is None or not api:
        return False
    if not isinstance(api, API):
        return False
    return True


def is_valid_username(username: str) -> bool:
    if username is None:
        return False

    if username == "":
        return False

    return True


def is_valid_user(user: User) -> bool:
    if user is None:
        return False

    if not isinstance(user, User):
        return False

    return True


def fetch_tweets_from_pickle(file_path: str = 'result.pkl') -> list[Tweet]:
    """Load tweets from a pickle file."""
    with open(file_path, 'rb') as f:
        tweets = pickle.load(f)
    return tweets
