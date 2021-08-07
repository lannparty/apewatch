from copy import deepcopy
from datetime import datetime, timedelta
from time import sleep
from zoneinfo import ZoneInfo

import requests
from elasticsearch import Elasticsearch
from elasticsearch.client import MlClient
from yahooquery import Ticker

BLOCKED_TICKERS = ["AMC", "GME", "AMC,GME", "TD"]
WEBHOOK_FORMAT = {
    "content": None,
    "embeds": [
        {
            "title": None,
            "url": "https://finance.yahoo.com/quote/",
            "color": None,
            "fields": [],
            "image": {
                "url": "https://www.ivolatility.com/nchart.j?charts=fdlvolatility,fdloptions_volume&1=ticker*"
            },
        }
    ],
}


def get_ticker_bid(ticker):
    try:
        details = Ticker(ticker)
        details = details.summary_detail
        return details[ticker].get("bid")
    except Exception:
        return None


def discord_alert(timestamp, ticker, record_score):
    if any(t in ticker for t in BLOCKED_TICKERS):
        return
    ticker = "".join(ticker)
    bid = get_ticker_bid(ticker)
    webhook = deepcopy(WEBHOOK_FORMAT)
    webhook["embeds"][0]["title"] = ticker
    webhook["embeds"][0]["url"] += ticker
    webhook["embeds"][0]["image"]["url"] += ticker
    webhook["embeds"][0]["fields"].append(
        {"name": "Time", "value": str(timestamp), "inline": True}
    )
    webhook["embeds"][0]["fields"].append(
        {"name": "Score", "value": str(record_score), "inline": True}
    )
    webhook["embeds"][0]["fields"].append(
        {"name": "Bid", "value": f"${bid}", "inline": True},
    )
    requests.post(
        "https://discord.com/api/webhooks/818674516116242433/pmZrjXi0gctBhOns-S0ZOxI7DVnrBzefJB7VV6-GgeE6i1zKFIu54kJYagfEqOgJ6i9A",
        json=webhook,
    )


def main():
    es = Elasticsearch(hosts=["elasticsearch"])
    # es = Elasticsearch()
    start = datetime.now()
    # start = datetime.now() - timedelta(minutes=30)
    start = round(start.timestamp() * 1000)
    es_ml = MlClient(es)
    while True:
        anomalies = es_ml.get_records(
            "ticker-pop15",
            exclude_interim=True,
            sort="record_score",
            desc=True,
            record_score=3,
            start=start,
        )
        records = anomalies["records"]
        if records:
            start = max(a["timestamp"] for a in records) + 1
            for anomaly in records:
                timestamp = datetime.fromtimestamp(
                    anomaly["timestamp"] / 1000, tz=ZoneInfo("America/New_York")
                )
                print(timestamp, anomaly["ticker"], round(anomaly["record_score"], 5))
                discord_alert(
                    timestamp, anomaly["ticker"], round(anomaly["record_score"], 5)
                )
        sleep(5)


if __name__ == "__main__":
    main()
