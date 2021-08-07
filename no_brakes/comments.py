import json
import sys

import praw

from no_brakes.subreddits import (
    SEARCHES,
    SUBSCRIBER_THRESHOLD,
    find_subreddits,
    join_subreddits,
)
from no_brakes.tickers import get_common_words, get_stocks, get_tickers
from no_brakes.utils import extract_stock_symbols


def process_comment(tickers, comment):
    potential_stock_tickers = extract_stock_symbols(comment.body)
    if tickers & potential_stock_tickers:
        ticker = list(tickers & potential_stock_tickers)
        comment_export = {
            "ticker": [t.removeprefix("$") for t in ticker],
            "body": comment.body,
            "link_title": comment.link_title,
            "link_author": comment.link_author,
            "permalink": comment.permalink,
            "subreddit_name": comment.subreddit_name_prefixed,
            "created_utc": int(comment.created_utc),
            "comment_author": comment.author.name,
            "edited": comment.edited,
        }
        return comment_export


def main():
    from no_brakes import config

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
    for comment in subreddit.stream.comments(skip_existing=True):
        c = process_comment(tickers, comment)
        if c:
            print(json.dumps(c, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
