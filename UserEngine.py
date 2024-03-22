from twscrape import User, API
from Helper import is_valid_api, is_valid_username, is_valid_user
from Exceptions import ApiNotFoundException
from enum import Enum


class State(Enum):
    NOT_SETUP = 0
    SETUP = 1


class UserEngine:
    """
    YOU MUST CALL SETUP FUNCTION!!!
    Example usage:
    user_engine = UserEngine("username")
    await user_engine.setup()
    """

    def __init__(self, api: API, username: str):
        self._user = None
        self._username = None
        self._api = None
        self._state = State.NOT_SETUP

        if not is_valid_api(api):
            raise ApiNotFoundException()

        if not is_valid_username(username):
            raise UserNotFoundException()

        self._api = api
        self._username = username

    async def setup(self):
        if not is_valid_username(self._username):
            raise UserNotFoundException("username must be set before calling setup.")

        if not is_valid_api(self._api):
            raise ApiNotFoundException()

        self._user = await _get_user_by_username(self._username, self._api)

        if is_valid_user(self._user):
            self._state = State.SETUP

    def get_current_user(self) -> User:
        if not is_valid_user(self._user):
            raise UserNotFoundException()

        return self._user

    def get_current_state(self):
        return self._state


async def _get_user_by_username(username: str, api: API) -> User:
    if not is_valid_api(api):
        raise ApiNotFoundException()

    if not is_valid_username(username):
        raise ApiNotFoundException()

    user = await api.user_by_login(username)

    if not is_valid_user(user):
        raise UserNotFoundException(f"User not found with username: %s " % username)

    user: User = user

    return user


class UserNotFoundException(Exception):
    pass
