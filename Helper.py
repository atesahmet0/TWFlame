from twscrape import Tweet, API, User


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
