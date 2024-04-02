from datetime import datetime

class SimpleTweet:
    def __init__(self, id: str, username: str, rawContent: str, date: datetime):
        self.id = id
        self.username = username
        self.rawContent = rawContent
        self.date = date

    def __str__(self):
        return f"SimpleTweet(id={self.id}, username={self.username}, rawContent={self.rawContent}, date={self.date})"