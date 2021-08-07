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


def process_submission(tickers, submission):
    if submission.over_18:
        return
    potential_stock_tickers = extract_stock_symbols(submission.title)
    if tickers & potential_stock_tickers:
        ticker = list(tickers & potential_stock_tickers)
        submission_export = {
            "ticker": [t.removeprefix('$') for t in ticker],
            "body": submission.selftext,
            "link_title": submission.title,
            "link_author": submission.author.name,
            "permalink": submission.permalink,
            "subreddit_name": submission.subreddit_name_prefixed,
            "created_utc": int(submission.created_utc),
        }
        return submission_export


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
    for submission in subreddit.stream.submissions():
        s = process_submission(tickers, submission)
        if s:
            print(json.dumps(s, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
