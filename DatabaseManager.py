from TweetDatabase import TweetDatabase
from twscrape import Tweet
from loguru import logger


class DatabaseManager:
    def __init__(self, username: str):
        self.tweet_database = TweetDatabase(username)

    def save_tweets(self, tweets: list[Tweet]):
        if not self.tweet_database:
            logger.error("tweet_database is no initialized.")
            return

        self.tweet_database.save_tweets(tweets)

    def fetch_latest_tweet(self):
        return self.tweet_database.fetch_latest_tweet_of_user()
