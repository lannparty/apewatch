import json
import pathlib


def get_stocks() -> list[dict[str, str]]:
    stocks_json = pathlib.Path(__file__).parent / "data" / "stocks.json"
    with open(stocks_json, "r") as f:
        stocks = json.load(f)
    return stocks["data"]["rows"]


def get_common_words() -> set:
    word_list = pathlib.Path(__file__).parent / "data" / "1000-common-english-words.txt"
    with open(word_list, "r") as f:
        words = [w.upper() for w in f.read().splitlines()]
        words.extend(['RH', 'DD', 'EOD', 'IMO', 'CEO', 'USA'])
    return set(words)


def get_tickers(stocks, english_words) -> set:
    tickers = set()
    for stock in stocks:
        symbol = stock["symbol"]
        if len(symbol) == 1:
            tickers.add(f'${symbol}')
            continue
        if symbol in english_words:
            tickers.add(f'${symbol}')
            continue
        tickers.add(f'${symbol}')
        tickers.add(symbol)
    return tickers