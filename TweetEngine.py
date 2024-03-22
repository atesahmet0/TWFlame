from twscrape import API
from Exceptions import ApiNotFoundException
from Helper import is_valid_api


class TweetEngine:
    """
    MUST SETUP RIGHT AFTER INITIALIZATION:
    tweet_engine = TweetEngine(api)
    await tweet_engine.setup()

    self.api must be set!!!
    """

    def __init__(self, api: API):
        if not is_valid_api(api):
            raise ApiNotFoundException("TweetEngine: Api is invalid.")

        self.api = api


