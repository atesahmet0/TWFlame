from enum import Enum
from TweetEngine import TweetEngine
from TweetEngine import State as TweetState
from UserEngine import UserEngine, UserNotFoundException
from UserEngine import State as UserState
from Helper import is_valid_api, is_valid_username
from twscrape import API, Tweet, User
from Config import get_current_database
from Exceptions import ApiNotFoundException, EngineNotSetupException


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

    async def setup(self) -> None:
        """
        This has to be called right after initialization!
        :return:
        """
        await self._user_engine.setup()
        await self._tweet_engine.setup()

    def get_current_state(self) -> State:
        if self._user_engine.get_current_state() != UserState.SETUP:
            return State.NOT_SETUP

        if self._tweet_engine.get_current_state() != TweetState.SETUP:
            return State.NOT_SETUP

        return State.SETUP

    def get_current_user(self) -> User:
        if self.get_current_state() != State.SETUP:
            raise EngineNotSetupException("")

        return self._user_engine.get_current_user()

    async def get_tweets(self, limit=1) -> list[Tweet]:
        """
        Set limit to higher if you want to fetch more. But don't exceed 1000 tweets per DAY!!!
        :param limit:
        :return: 
        """

        if self.get_current_state() != State.SETUP:
            raise EngineNotSetupException("Backend Engine: _tweet_engine is not setup.")

        return await self._tweet_engine.get_tweet_from_user_by_interval(self.get_current_user(),
                                                                        "2024-01-01", "2024-01-02", limit)
