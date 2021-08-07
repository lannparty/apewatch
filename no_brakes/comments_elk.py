import logging
import sys
from datetime import datetime, timezone
from urllib.parse import quote_plus

import praw
from elasticsearch_dsl import Date, Document, Keyword, Text, Boolean
from elasticsearch_dsl.connections import connections

from no_brakes import process_comment
from no_brakes.subreddits import (
    SEARCHES,
    SUBSCRIBER_THRESHOLD,
    find_subreddits,
    join_subreddits,
)
from no_brakes.tickers import get_common_words, get_stocks, get_tickers


class Comment(Document):
    ticker = Keyword()
    body = Text()
    link_title = Text()
    link_author = Keyword()
    permalink = Keyword()
    subreddit_name = Keyword()
    created_utc = Date()
    comment_author = Keyword()
    edited = Boolean()

    class Index:
        name = "reddit-comments-*"

    def save(self, **kwargs):
        if not self.created_utc:
            self.created_utc = datetime.now()
        kwargs["index"] = self.created_utc.strftime("reddit-comments-%Y%m%d")
        return super(Comment, self).save(**kwargs)


def main():
    from no_brakes import config

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    for logger_name in ("praw", "prawcore"):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    stocks = get_stocks()
    common_words = get_common_words()
    tickers = get_tickers(stocks, common_words)

    reddit = praw.Reddit(
        user_agent="no_brakes",
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        username=config.USERNAME,
        password=config.PASSWORD,
    )

    multiple_subreddits = join_subreddits(
        find_subreddits(reddit, SEARCHES, SUBSCRIBER_THRESHOLD)
    )
    subreddit = reddit.subreddit(multiple_subreddits)

    connections.create_connection(hosts=["elasticsearch"])
    index_template = Comment._index.as_template("reddit-comments", order=0)
    index_template.save()

    for comment in subreddit.stream.comments(skip_existing=True):
        c = process_comment(tickers, comment)
        if c:
            c["created_utc"] = datetime.fromtimestamp(c["created_utc"], timezone.utc)
            c = Comment(**c)
            c.save()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
