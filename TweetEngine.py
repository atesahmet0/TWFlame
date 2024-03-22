from enum import Enum
from twscrape import API, User, Tweet, gather
from Exceptions import ApiNotFoundException, EngineNotSetupException
from Helper import is_valid_api, is_valid_user
from UserEngine import UserNotFoundException

class State(Enum):
    SETUP = 0,
    NOT_SETUP = 1


class TweetEngine:
    """
    MUST SETUP RIGHT AFTER INITIALIZATION:
    tweet_engine = TweetEngine(api)
    await tweet_engine.setup()

    self.api must be set!!!
    """

    def __init__(self, api: API):
        self._state = State.NOT_SETUP

        if not is_valid_api(api):
            raise ApiNotFoundException("TweetEngine: Api is invalid.")

        self._api = api

    async def setup(self):
        self._state = State.SETUP

    def get_current_state(self):
        return self._state

    async def get_tweet_from_user_by_interval(self, user: User, start_time: str, final_time: str, limit=1) -> list[Tweet]:
        """
        Time is in YYYY-MM-DD format. Ex: 2023-01-01
        :param user:
        :param start_time:
        :param final_time:
        :return:
        """
        if self.get_current_state() != State.SETUP:
            raise EngineNotSetupException("TweetEngine: Engine is not setup.")

        if not is_valid_user(user):
            raise UserNotFoundException()

        search_query = f"From:@%s" % user.username

        if len(start_time) != 0:
            search_query += f" since:%s" % start_time

        if len(final_time) != 0:
            search_query += f" until:%s" % final_time

        print(f"TweetEngine: Given search query is: %s" % search_query)

        return await gather(self._api.search(search_query, limit=limit))

