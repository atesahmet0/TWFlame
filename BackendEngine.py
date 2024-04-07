from datetime import timedelta, datetime
from enum import Enum

from DatabaseManager import DatabaseManager
from SimpleTweet import SimpleTweet
from TweetEngine import TweetEngine
from TweetEngine import State as TweetState
from UserEngine import UserEngine, UserNotFoundException
from UserEngine import State as UserState
from Helper import is_valid_api, is_valid_username, convert_to_datetime, extract_date_from_datetime
from twscrape import API, User
from Config import get_current_database
from Exceptions import ApiNotFoundException, EngineNotSetupException
from loguru import logger


class State(Enum):
    SETUP = 0,
    NOT_SETUP = 1


class BackendEngine:
    """
    This handles twitter operations for only ONE ACCOUNT
    create multiple backend engines if you have to scrape more
    than one accounts
    """

    def __init__(self, username: str, api: API = None):
        self._state = State.NOT_SETUP
        self.username = username

        if not is_valid_username(username):
            raise UserNotFoundException("username parameter is not valid.")

        if not is_valid_api(api):
            print("BackendEngine: Not valid api is given. New api will be initialized.")
            self._api = API(get_current_database())
        else:
            self._api = api

        if not is_valid_api(self._api):
            raise ApiNotFoundException(f"Api couldn't be initialized. Location: %s" % get_current_database())

        self._user_engine = UserEngine(self._api, username)
        self._tweet_engine = TweetEngine(self._api)
        self._database_manager = DatabaseManager(username)

    async def setup(self) -> None:
        """
        This has to be called right after initialization!
        :return:
        """
        await self._user_engine.setup()
        await self._tweet_engine.setup()

    def get_current_state(self) -> State:
        if self._user_engine.get_current_state() != UserState.SETUP:
            logger.error("UserEngine is not setup.")
            return State.NOT_SETUP

        if self._tweet_engine.get_current_state() != TweetState.SETUP:
            logger.error("TweetEngine is not setup.")
            return State.NOT_SETUP

        if self._database_manager is None:
            logger.error("DatabaseManager is not setup.")
            return State.NOT_SETUP

        return State.SETUP

    def get_current_user(self) -> User:
        if self.get_current_state() != State.SETUP:
            raise EngineNotSetupException("")

        return self._user_engine.get_current_user()

    async def get_tweets_from_database(self) -> list[SimpleTweet]:
        """
        Fetch all tweets from the database
        :return:
        """
        if self.get_current_state() != State.SETUP:
            raise EngineNotSetupException("Backend Engine: backend engine is not setup.")

        return self._database_manager.fetch_all_tweets()

    async def fetch_all_tweets(self, start_date: str = None, final_date: str = None):
        """
        Set limit to higher if you want to fetch more. But don't exceed 1000 tweets per DAY!!!
        :final_date: Must be in YYYY-MM-DD format
        :return:
        """
        if self.get_current_state() != State.SETUP:
            raise EngineNotSetupException("Backend Engine: backend engine is not setup.")

        logger.info(f"Fetching tweets for {self.get_current_user().username}")

        while (self.latest_fetch_date_timestamp < (datetime.now() - timedelta(1)).timestamp()
               and self.latest_fetch_date_timestamp < convert_to_datetime(final_date).timestamp()):
            await self._get_tweet_one_more_day()

        logger.info(f"Fetching tweets for {self.get_current_user().username} is done.")

    latest_fetch_date_timestamp = -1

    async def _get_tweet_one_more_day(self):
        """
        Fetch tweets for one more day
        :return: Newly fetched tweets
        """
        if self.get_current_state() != State.SETUP:
            raise EngineNotSetupException("Backend Engine: backendengine is not setup.")

        logger.info(f"Fetching tweets for {self.get_current_user().username}")

        # Check where did we leave off
        try:
            latest_tweet = self._database_manager.fetch_latest_tweet()
            # Extract date from latest_tweet
            date_start = max(latest_tweet.date.timestamp(), self.latest_fetch_date_timestamp)
            logger.info(f"Latest fetch date: {self.latest_fetch_date_timestamp}")
            logger.info(f"Latest tweet date: {latest_tweet.date.timestamp()}")
            date_end = date_start + 86400
            self.latest_fetch_date_timestamp = date_end
            logger.info(f"Latest tweet: {latest_tweet}")

            date_start = extract_date_from_datetime(datetime.fromtimestamp(date_start))
            date_end = extract_date_from_datetime(datetime.fromtimestamp(date_end))

            logger.info(f"Fetching tweets from {date_start} to {date_end}")
            result = await self._tweet_engine.get_tweet_from_user_by_interval(self.get_current_user(), date_start,
                                                                              date_end,
                                                                              limit=1000)
            logger.info(f"Fetched {len(result)} tweets for {self.get_current_user().username}")

            self._database_manager.save_tweets(result)
            return result
        except Exception as e:
            result = await self._tweet_engine.get_tweet_from_user_by_interval(self.get_current_user(),
                                                                              limit=1000)
            logger.info(f"Fetched {len(result)} tweets for {self.get_current_user().username}")

            self._database_manager.save_tweets(result)
            return result
