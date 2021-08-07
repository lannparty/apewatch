#!/bin/bash

TICKERS=$(curl -s -XPOST -H "Content-Type: application/json" localhost:9200/.ml-anomalies-shared/_doc/_search -d @anomaly.json |jq -r '.hits.hits[] |._source |select(.result_type=="record")|[.ticker[0], .record_score] | @tsv' |tee ticker-anomoly-`date +%s` |grep -v -E 'AMC|GME|PLTR|RKT|TSLA|ARE|DD|GO|IRS' |awk '{print $1}' |tr "\n" ",")

curl -XPOST -H "Content-Type: application/json" -d '{"username": "anomoly", "content": "'"$TICKERS"'"}' https://discord.com/api/webhooks/817952131561685043/VigUOFFTsFjXr3p46mzL-AsSTQrMy341vLn8twHOi5Xjpnl4m2RhJ31a921HV3e3h_We
