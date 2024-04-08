from twscrape import Tweet
from Database import Database
from loguru import logger
from Helper import extract_date_from_tweet_year_month_day
from datetime import datetime
from SimpleTweet import SimpleTweet


class TweetDatabase(Database):
    """
    Database per user
    """

    def __init__(self, username):
        super().__init__(username)
        self.username = username
        logger.info(f"TweetDatabase initialized for {username}")

    def _store_tweet(self, tweet: Tweet):
        """ store a tweet in the database """
        logger.info(f"Storing tweet: {tweet.id}")
        tweet_date = extract_date_from_tweet_year_month_day(tweet)
        table_structure = """
            id TEXT PRIMARY KEY,
            username TEXT,
            rawContent TEXT,
            date REAL
        """
        self.create_table(self.format_table_name(extract_date_from_tweet_year_month_day(tweet)), table_structure)

        self.store_data(tweet_date, 'id, username, rawContent, date',
                        (tweet.id, tweet.user.username, tweet.rawContent, tweet.date.timestamp()))

    def save_tweets(self, tweets: list[Tweet]) -> None:
        """ save tweets in the database """
        for tweet in tweets:
            self._store_tweet(tweet)

    def fetch_all_tweets_of_user(self) -> list[SimpleTweet]:
        """ fetch all tweets from the database """
        result = []
        fetched = self.fetch_all_tables()
        for key in fetched.keys():
            list = fetched[key]
            for tweet_as_list in list:
                tweet = SimpleTweet(id=tweet_as_list[0], username=tweet_as_list[1], rawContent=tweet_as_list[2],
                                    date=datetime.fromtimestamp(tweet_as_list[3]))
                result.append(tweet)
        return result

    def fetch_tweet_by_table(self, table_name: str) -> list[SimpleTweet]:
        """ fetch tweets from the database by table name """
        result = []
        fetched = self.fetch_data(self.format_table_name(table_name), 'date')
        for tweet_as_list in fetched:
            tweet = SimpleTweet(id=tweet_as_list[0], username=tweet_as_list[1], rawContent=tweet_as_list[2],
                                date=datetime.fromtimestamp(tweet_as_list[3]))
            result.append(tweet)
        return result

    def fetch_latest_tweet_of_user(self):
        """ fetch the latest tweet from the database """
        table_names = self.fetch_and_sort_table_dates()
        logger.info(f"Tables: {table_names}")

        latest_table = table_names[-1]
        logger.info(f"Latest table: {latest_table}")

        latest_tweets = self.fetch_tweet_by_table(latest_table)
        logger.info(f"Latest tweets: {latest_tweets}")

        latest_tweet = latest_tweets[0]
        logger.info(f"Latest tweet: {latest_tweet}")

        return latest_tweet
