import asyncio
from twscrape import API, gather, User, Tweet
from Exceptions import ApiNotFoundException
from BackendEngine import BackendEngine


async def main():
    # Initialize api with the database
    # Setup database with twscrape cli
    backend = BackendEngine("ntvspor")
    await backend.setup()

    tweets = await backend.get_tweets()
    print(i.rawContent for i in tweets)
    for i in tweets:
        print(i.rawContent)


async def get_tweets_of_user_by_intervar(api: API, user_name: str, initial_date: str = "", final_date: str = "",
                                         limit=20):
    """
    Search for user's tweets by date.
    Preferred way is to divide interval by days.
    Usage: get_tweets_of_user_by_id(123456789, "2012-01-01", 2012-02-02")
    :param api:
    :param limit:
    :param user_name: Username of the user.
    :param initial_date: date as string in format of YEAR-MONTH-DAY
    :param final_date:
    :return: List of tweets as Tweet object
    """
    if not api:
        raise ApiNotFoundException("Api is not initialized get_tweets_of_user_by_username")

    search_query = f"From:@%s" % user_name

    if len(initial_date) != 0:
        # Initial date is given. Use it
        search_query += f" since:%s" % initial_date

    if len(final_date) != 0:
        search_query += f" until:%s" % final_date

    print(f"Given search query is: %s" % search_query)
    return await gather(api.search(search_query, limit=limit))


async def get_user_by_username(username: str, api: API) -> User | None:
    """
    Get user by username.
    :param username:
    :param api:
    :return: Userid as int. If user is not found return None.
    """
    if not api:
        return

    return await api.user_by_login(username)


if __name__ == "__main__":
    asyncio.run(main())
