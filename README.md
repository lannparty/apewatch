# apewatch
Stream Reddit posts and comments containing stock tickers to Elasticsearch for anomlaly detection and alert to discord webhook.

## Find Investing Subreddits
`python3 no_brakes/subreddits.py`

## Stream submissions
`python3 no_brakes/submissions.py`

## Stream comments
`python3 no_brakes/comments.py`

## Generate client id and secret
https://www.reddit.com/prefs/apps

Put config.py in no_brakes
```
CLIENT_ID = ""
CLIENT_SECRET = ""
USERNAME = ""
PASSWORD = ""
```

## PROD
```
docker-compose -f docker-compose.yaml -f docker-compose-prod.yaml build
docker-compose -f docker-compose.yaml -f docker-compose-prod.yaml down
docker-compose -f docker-compose.yaml -f docker-compose-prod.yaml up -d
```

## TODO
- Alert off of growth of most mentioned tickers.
- Scrape Twitter
- auto Update Tickers
- Add Reddit submissions
- add poster age
