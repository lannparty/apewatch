from no_brakes import *

def test_get_stocks():
    assert len(get_stocks()) >= 7154


def test_get_tickers():
    stocks = get_stocks()
    english_words = get_common_words()
    tickers = get_tickers(stocks, english_words)
    assert '$F' in tickers
    assert 'F' not in tickers
    assert 'GME' in tickers
    assert '$GME' in tickers
    assert 'DD' not in tickers
    assert 'IMO' not in tickers
    assert 'EOD' not in tickers
    assert 'RH' not in  tickers