from datetime import timedelta, datetime
from enum import Enum

from DatabaseManager import DatabaseManager
from SimpleTweet import SimpleTweet
from TweetEngine import TweetEngine
from TweetEngine import State as TweetState
from UserEngine import UserEngine, UserNotFoundException
from UserEngine import State as UserState
from Helper import is_valid_api, is_valid_username, convert_to_datetime, extract_date_from_datetime, is_valid_date
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

        user = self._user_engine.get_current_user()
        logger.info(f"Current user: {user.username}")
        return user

    async def get_tweets_from_database(self) -> list[SimpleTweet]:
        """
        Fetch all tweets from the database
        :return:
        """
        if self.get_current_state() != State.SETUP:
            raise EngineNotSetupException("Backend Engine: backend engine is not setup.")

        tweets = self._database_manager.fetch_all_tweets()
        logger.info(f"Fetched {len(tweets)} tweets from database")
        return tweets

    async def fetch_all_tweets(self, start_date: str = None, final_date: str = None) -> None:
        """
        Set limit to higher if you want to fetch more. But don't exceed 1000 tweets per DAY!!!
        :start_date: Must be in YYYY-MM-DD format
        :final_date: Must be in YYYY-MM-DD format
        """
        if self.get_current_state() != State.SETUP:
            raise EngineNotSetupException("Backend Engine: backend engine is not setup.")

        if start_date != "" and not is_valid_date(start_date):
            logger.info(f"Start Date: {start_date} is not in the correct format 'YYYY-MM-DD'")
            return

        if final_date != "" and not is_valid_date(final_date):
            logger.info(f"Final Date: {final_date} is not in the correct format 'YYYY-MM-DD'")
            return

        logger.info(f"Fetching tweets for {self.get_current_user().username}")

        start_timestamp = int(convert_to_datetime(start_date).timestamp())
        end_timestamp = int(convert_to_datetime(final_date).timestamp())

        for timestamp in range(start_timestamp, end_timestamp, 86400):
            end = timestamp + 86400
            start_string = extract_date_from_datetime(datetime.fromtimestamp(timestamp))
            end_string = extract_date_from_datetime(datetime.fromtimestamp(end))
            logger.info(f"Fetching tweets from {start_string} to {end_string}")

            result = await self._tweet_engine.get_tweet_from_user_by_interval(self.get_current_user(),
                                                                              start_string, end_string, limit=1000)
            logger.info(f"Fetched {len(result)} tweets for {self.get_current_user().username}")
            self._database_manager.save_tweets(result)

        logger.info(f"Fetching tweets for {self.get_current_user().username} is done.")
