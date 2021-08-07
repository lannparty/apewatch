import praw
from praw.models import subreddits

SEARCHES = [
    "stocks",
    "stock",
    "wallstreet",
    "invest",
    "investing",
    "bets",
    "shares",
    "funds",
    "equities",
    "options",
    "robinhood",
    "DankExchange",
]

BLOCKED_SUBS = [
    "ethtrader",
    "SatoshiStreetBets",
    "wtfstockphotos",
    "altcoin",
    "mtgfinance",
    "Silverbugs",
    "sportsbetting",
    "csgomarketforum",
    "MemeEconomy",
    "realestateinvesting",
    "RealEstate",
]

SUBSCRIBER_THRESHOLD = 50_000


def find_subreddits(reddit: praw.reddit.Reddit, searches: list[str], threshold: int):
    subreddits = set()
    for search in searches:
        for sub in reddit.subreddits.search(query=search, limit=100):
            if sub.subscribers and sub.subscribers > threshold:
                if any(n == sub.display_name for n in BLOCKED_SUBS):
                    continue
                normalized_name = sub.display_name.lower()
                normalized_description = sub.public_description.lower()
                if any(n in normalized_name for n in searches) or any(
                    n in normalized_description for n in searches
                ):
                    subreddits.add(sub)
    return subreddits


def join_subreddits(subreddits):
    return "+".join((sub.display_name for sub in subreddits))


if __name__ == "__main__":
    from no_brakes import config
    reddit = praw.Reddit(
        user_agent="no_brakes",
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        username=config.USERNAME,
        password=config.PASSWORD,
    )
    subs = list(find_subreddits(reddit, SEARCHES, SUBSCRIBER_THRESHOLD))
    subs.sort(key=lambda x: x.subscribers, reverse=True)
    for sub in subs:
        print(f'{sub.display_name:<25}{sub.subscribers:,}')
    print(join_subreddits(subs))
